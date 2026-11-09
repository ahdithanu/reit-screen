"""Verification. Writes raw diffs to verification.md. Sets claims.checked=yes only on a match against filing text.

Never edits metrics or buckets.
"""
import json
import re
from html import unescape

import event_reader
import ladder_extract
import synthesize
from common import PROC, RAW, ROOT, fetched_at_of, html_to_text, latest_cached, safe_key


def latest_cached_archive(key):
    return latest_cached("archives", safe_key(key))

LTAGS = [t for _, t in ladder_extract.LADDER]
FRAME_PERIOD = "CY2025Q4I"


def _fmt(v):
    return "n/a" if v is None else f"{v:,.0f}"


# ------------------------------------------------------------ 1. control
def control(flags, cfg):
    c = cfg["pipeline_control"]
    hit = [f for f in flags.values() if f["name"] == cfg["names"][c["cik"]]["label"]]
    if not hit:
        return False, ["OPI not in this run"]
    got = hit[0]["bucket"]
    return got == c["expected_bucket"], [f"expected {c['expected_bucket']}, got **{got}** ({hit[0]['why']})"]


# ------------------------------------------------------------ 2. cross-extraction
resolved = []  # cross-check rows that differed only because side A read 10-K facts only (fixed: frames selection rule)


def cross_extract(fx, names, cf_paths, cfg):
    frames = {}
    for tag in LTAGS + [ladder_extract.CASH_TAG, ladder_extract.DEBT_TAG]:
        r = fx.frame(tag, FRAME_PERIOD)
        frames[tag] = (json.loads(open(r["path"], "rb").read()) if r["path"] else None, r["error"], r["url"])
    rows, diffs = [], []
    for d in names:
        for tag in LTAGS + [ladder_extract.CASH_TAG, ladder_extract.DEBT_TAG]:
            if cf_paths[d["cik"]] is None:
                a = (None, "companyfacts not fetched")
            else:
                a10k = ladder_extract.value_at(cf_paths[d["cik"]], tag, cfg["ladder_period_end"])
                av, aacc, aform = ladder_extract.value_at_frames_rule(cf_paths[d["cik"]], tag, cfg["ladder_period_end"])
                a = (av, aacc if av is None else f"{aacc} ({aform})")
                if a10k[0] is None and av is not None:  # the 10-K-only rule found nothing; record the earlier artifact
                    resolved.append((d["label"], tag, a10k, (av, aacc, aform)))
            fr, err, _ = frames[tag]
            b = None
            if fr is not None:
                m = [x for x in fr.get("data", []) if str(x["cik"]) == str(int(d["cik"]))]
                b = (float(m[0]["val"]), m[0]["accn"]) if m else (None, "cik not in frame")
            else:
                b = (None, f"frame fetch failed: {err}")
            same = "both missing" if (a[0] is None and b[0] is None) else ("yes" if a[0] == b[0] else "**NO**")
            rows.append((d["label"], tag, a, b, same))
            if same == "**NO**":
                diffs.append((d["label"], tag, a, b))
    return rows, diffs


# ------------------------------------------------------------ 3. spot check vs 10-K text
def _attrs(s):
    return {k.lower(): v for k, v in re.findall(r'([\w:.-]+)="([^"]*)"', s)}


def _num(txt, a):
    fmt = a.get("format", "")
    t = unescape(re.sub(r"<[^>]+>", "", txt)).strip()
    if "zero" in fmt or t in ("-", "—", "–"):
        return 0.0, t
    n = float(re.sub(r"[^\d.]", "", t))
    v = n * 10 ** int(a.get("scale", "0"))
    return (-v if a.get("sign") == "-" else v), t


def spot_check(fx, d, cfg):
    lad = d["ladder"]
    acc = next((f["accession"] for f in lad.values() if f["accession"]), None)
    if not acc:
        return {"status": "not done", "reason": "n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)"}
    sub = json.loads(open(d["sub_path"], "rb").read())["filings"]["recent"]
    try:
        i = sub["accessionNumber"].index(acc)
    except ValueError:
        return {"status": "not done", "reason": f"accession {acc} not in submissions recent list"}
    doc = sub["primaryDocument"][i]
    r = fx.archive(d["cik"], acc, doc)
    if r["path"] is None:
        return {"status": "not done", "reason": f"10-K fetch failed: {r['error']}", "url": r["url"]}
    html = open(r["path"], "rb").read().decode("utf-8", errors="replace")
    ctx = {}
    for m in re.finditer(r'<(?:xbrli:)?context\b[^>]*?\bid="([^"]+)"[^>]*>(.*?)</(?:xbrli:)?context>', html, re.S | re.I):
        inst = re.search(r"<(?:xbrli:)?instant>\s*([^<\s]+)", m.group(2), re.I)
        mem = re.findall(r"<(?:xbrldi:)?explicitMember\b[^>]*dimension=\"([^\"]+)\"[^>]*>\s*([^<\s]+)", m.group(2), re.I)
        ctx[m.group(1)] = {"instant": inst.group(1) if inst else None, "dims": bool(re.search(r"segment", m.group(2), re.I)),
                           "members": "; ".join(f"{dm.split(':')[-1]}={mv.split(':')[-1]}" for dm, mv in mem)}
    found, dimensioned = {}, []
    for m in re.finditer(r"<ix:nonfraction\b([^>]*)>(.*?)</ix:nonfraction>", html, re.S | re.I):
        a = _attrs(m.group(1))
        tag = a.get("name", "").split(":")[-1]
        if tag not in LTAGS:
            continue
        c = ctx.get(a.get("contextref"), {})
        if c.get("instant") != cfg["ladder_period_end"]:
            continue
        val, shown = _num(m.group(2), a)
        if c.get("dims"):
            dimensioned.append((tag, a.get("contextref") + " [" + c.get("members", "") + "]", shown, val))
            continue
        found.setdefault(tag, []).append({"pos": m.start(), "shown": shown, "scale": a.get("scale", "0"), "value": val})
    # the table holding the dimensionless ladder facts
    table_txt, printed_total = [], None
    scales = [x["scale"] for v in found.values() for x in v]
    major = max(set(scales), key=scales.count) if scales else None
    if found:
        pos = min(v[0]["pos"] for v in found.values())
        t0 = html.rfind("<table", 0, pos)
        t1 = html.find("</table>", pos)
        if t0 != -1 and t1 != -1:
            ladder_pos = {x["pos"] for v in found.values() for x in v}
            VAL = re.compile(r"^\(?[\d,.]+\)?$|^[—–-]$")
            YEAR = re.compile(r"^(19|20)\d\d$")

            def label_idx(cells):
                # the row label is the first non-empty cell unless that cell is a value (a bare year like "2027" counts as a label)
                i = next((i for i, t in enumerate(cells) if t and t != "$"), None)  # a currency-symbol cell is never a label
                return i if i is not None and (not VAL.match(cells[i]) or YEAR.match(cells[i])) else None

            ordinals, trs, last_ladder_tr = [], list(re.finditer(r"<tr\b.*?</tr>", html[t0:t1], re.S | re.I)), None
            parsed = []
            for ti_, trm in enumerate(trs):
                raw = list(re.finditer(r"<t[dh]\b.*?</t[dh]>", trm.group(0), re.S | re.I))
                cells = [html_to_text(c.group(0)).replace("\u200b", "").strip() for c in raw]
                li = label_idx(cells)
                parsed.append((cells, li))
                k = -1
                for ci, c in enumerate(raw):
                    if ci != li and VAL.match(cells[ci]):
                        k += 1
                        absolute = t0 + trm.start() + c.start()
                        if any(absolute <= lp < absolute + len(c.group(0)) for lp in ladder_pos):
                            ordinals.append(k)
                            last_ladder_tr = ti_
                shown = [c for c in cells if c and c not in ("$",)]
                if shown:
                    table_txt.append(" | ".join(shown))
            # printed total = the first row with values directly below the last ladder row, if it is labelled "Total..." or unlabelled
            # (a subtotal under the year rows). Rows further down (e.g. net of issuance costs) are never used.
            if ordinals and last_ladder_tr is not None:
                ordn = max(set(ordinals), key=ordinals.count)
                for cells, li in parsed[last_ladder_tr + 1:]:
                    vals = [c for i, c in enumerate(cells) if i != li and VAL.match(c)]
                    if not vals:
                        continue
                    label = cells[li] if li is not None else "(unlabelled subtotal row)"
                    if (li is None or label.lower().startswith("total")) and len(vals) > ordn and re.search(r"\d", vals[ordn]):
                        n = float(re.sub(r"[^\d.]", "", vals[ordn])) * 10 ** int(major)
                        printed_total = {"label": label, "shown": vals[ordn], "scale": major, "value": n, "column_ordinal": ordn}
                    break
    rows = []
    for short, tag in ladder_extract.LADDER:
        ext = lad[short]["value"]
        f = found.get(tag)
        if not f:
            rows.append((short, tag, ext, None, None, "not tagged (dimensionless) in 10-K text"))
            continue
        vals = {x["value"] for x in f}
        doc_v = f[0]["value"]
        note = "" if len(vals) == 1 else f"tag appears {len(f)}x with values {sorted(vals)}"
        if f[0]["scale"] != major:
            alt = float(re.sub(r"[^\d.]", "", f[0]["shown"]) or 0) * 10 ** int(major)
            note += (f"SCALE MISMATCH: tagged scale {f[0]['scale']} while the other ladder cells in this table use scale {major}; "
                     f"if read at the table's scale the value would be {alt:,.0f}. Value NOT changed (filer's tag kept).")
        rows.append((short, tag, ext, doc_v, f"{f[0]['shown']} (scale {f[0]['scale']})", note))
    # 2027 dimensional split (INFERRED: column meaning taken from the filer's XBRL member names)
    split = []
    for t, cref, shown, v in dimensioned:
        if not t.endswith("InYearTwo"):
            continue
        mem = cref.split("[", 1)[1].rstrip("]")
        instrument = re.search(r"(DebtInstrumentAxis|LongtermDebtTypeAxis|ShortTermDebtTypeAxis|LineOfCreditFacilityAxis)=([^;]+)", mem)
        if instrument:
            kind = "instrument"
            member = instrument.group(2)
            unsecured = bool(re.search(r"Credit|Revolv|TermLoan|Unsecured|SeniorNotes|LineOfCredit", member))
        elif re.search(r"JointVenture|EquityMethod|Unconsolidated", mem):
            kind, member, unsecured = "jv_share", mem, None
        else:
            kind, member, unsecured = "other", mem, None
        split.append({"kind": kind, "member": member, "unsecured_bank_or_notes": unsecured, "shown": shown, "value": v, "context": cref})
    return {"status": "done", "url": r["url"], "rows": rows, "table": table_txt, "dimensioned": dimensioned,
            "printed_total": printed_total, "split_2027": split, "accession": acc}


# ------------------------------------------------------------ 5. quotes
def recheck_quotes(fx, d, cfg, offline):
    out = []
    for e in d["events"]:
        if not event_reader.needs_document(e):
            continue
        if offline:
            key = safe_key(f"{int(d['cik'])}_{e['accession'].replace('-', '')}_{e['primary_doc']}")
            copies = sorted((RAW / "archives").glob(f"{key}__*"))
            if len(copies) >= 2:
                p = copies[0]
                how = f"re-fetched earlier ({fetched_at_of(copies[-1])}); compared with original fetch {fetched_at_of(copies[0])} from cache"
            else:
                p, how = e.get("doc_path"), "offline, only one cached copy: NOT re-fetched"
        else:
            r = fx.archive(d["cik"], e["accession"], e["primary_doc"], force=True)
            p, how = r["path"], "re-fetched"
        q2, g2 = event_reader.extract_quote(e, p, cfg["events"]["quote_chars"])
        in_text = bool(e.get("quote")) and p is not None and e["quote"] in html_to_text(open(p, "rb").read().decode("utf-8", errors="replace"))
        out.append({"claim_id": e.get("claim_id"), "item": e["item_code"], "filed": e["filed"], "url": e["filing_url"],
                    "match": bool(e.get("quote")) and q2 == e["quote"], "in_text": in_text, "how": how,
                    "refetched": how.startswith("re-fetched"),
                    "gap": e.get("quote_gap") or g2})
    return out


# ------------------------------------------------------------ driver
def claim(claims, cid, text, url, tag_type, checked, note):
    claims[:] = [c for c in claims if c["claim_id"] != cid]
    claims.append({"claim_id": cid, "claim": text, "source_url": url, "tag_type": tag_type, "checked": checked, "note": note})


def run(fx, cfg, names, flags, conflicts, cf_paths, subs, claims, case_files, offline=False):
    L = ["# verification.md", "", f"Run as_of {cfg['as_of']}. Names in this run: " + ", ".join(d["label"] for d in names) + ".",
         "Raw diffs are printed in full, not summarized.", ""]
    ok, msg = control(flags, cfg)
    L += ["## 1. Pipeline control (OPI must be ACT NOW)", "", f"**{'PASS' if ok else 'FAIL'}**: " + msg[0], ""]

    rows, diffs = cross_extract(fx, names, cf_paths, cfg)
    L += ["## 2. Cross-extraction: companyfacts (A) vs frames " + FRAME_PERIOD + " (B)", "",
          "Checks the plumbing (two SEC endpoints over the same filings), not the filer.", "",
          "| name | tag | A value | A accn / reason | B value | B accn / reason | same |", "|---|---|---:|---|---:|---|---|"]
    for n, t, a, b, s in rows:
        L.append(f"| {n} | {t.replace('LongTermDebtMaturitiesRepaymentsOfPrincipal', 'LTDMat…')} | {_fmt(a[0])} | {a[1]} | {_fmt(b[0])} | {b[1]} | {s} |")
    L += ["", f"**Differences: {len(diffs)}**", "",
          "Side A uses the frames selection rule: the most recently filed 10-K or 10-Q fact for the instant. "
          "Until 2026-11-09 side A read 10-K facts only; rows that differed only because of that are listed under Conflicts and gaps as RESOLVED.", ""]
    for n, t, a, b in diffs:
        L.append(f"- {n} / {t}: A={_fmt(a[0])} ({a[1]}) vs B={_fmt(b[0])} ({b[1]})")
    L.append("")

    L += ["## 3. Spot check against 10-K text", ""]
    claim_by_id = {c["claim_id"]: c for c in claims}
    not_done, spot_results = [], {}
    for d in names:
        if d["cik"] not in cfg["spot_check_ciks"]:
            continue
        sc = spot_check(fx, d, cfg)
        L.append(f"### {d['label']}")
        if sc["status"] != "done":
            L += [f"NOT DONE: {sc['reason']}", ""]
            not_done.append(d["label"])
            continue
        L += [f"Source: {sc['url']}", "", "Method: the inline-XBRL facts rendered *inside the 10-K document* "
              "(dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.", "",
              "| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |", "|---|---|---:|---:|---|---:|---|"]
        tk = d["ticker"]
        for short, tag, ext, docv, shown, note in sc["rows"]:
            diff = None if (ext is None or docv is None) else ext - docv
            L.append(f"| {short} | {tag.replace('LongTermDebtMaturitiesRepaymentsOfPrincipal', '…')} | {_fmt(ext)} | {_fmt(docv)} | {shown or 'n/a'} | {_fmt(diff)} | {note} |")
            if "SCALE MISMATCH" in note:
                conflicts.append({"name": d["label"], "tag": tag, "value_a": ext, "value_b": note.split("would be ")[1].split(".")[0],
                                  "reason": "filer tagged scale differs from the rest of its own 10-K table; kept as tagged"})
            if diff == 0 and ext is not None and "SCALE MISMATCH" not in note:
                c = claim_by_id.get(f"{tk}.ladder_{short}")
                if c:
                    c["checked"] = "yes"; c["note"] += "; matched 10-K text (verify.py §3)"
        L += ["", "Table as rendered in the 10-K (cells joined with |; '$' cells dropped):", "", "```"] + sc["table"][:60] + ["```", ""]
        pt = sc["printed_total"]
        lsum = sum(f["value"] for f in d["ladder"].values() if f["value"] is not None)
        if pt:
            L += [f"Printed total in the table ('{pt['label']}', ladder column): {pt['shown']} (scale {pt['scale']}) = {_fmt(pt['value'])}; "
                  f"six tagged buckets sum to {_fmt(lsum)}; diff {_fmt(lsum - pt['value'])}.", ""]
            missing_b = [k for k, f in d["ladder"].items() if f["value"] is None]
            if missing_b and lsum == pt["value"]:
                L += [f"NOTE: bucket(s) {', '.join(missing_b)} are not tagged, and the filer's own printed total equals the sum of the tagged buckets. "
                      "So in the filer's table the missing bucket(s) add nothing, and the upper-bound 2027 share equals the printed-table share. "
                      "The data stays missing (no imputation) and the scoring is unchanged.", ""]
                claim(claims, f"{tk}.ub_equals_printed", f"{d['label']}: printed 10-K total {_fmt(pt['value'])} = sum of tagged buckets; "
                      f"missing {', '.join(missing_b)} add nothing in the filer's table, so the upper-bound 2027 share is the table share",
                      sc["url"], "checked", "yes", "verify.py §3")
            claim(claims, f"{tk}.printed_total", f"{d['label']} 10-K maturity table printed total = ${pt['value']/1e6:,.1f}M", sc["url"],
                  "measured", "yes", "read from 10-K table text (verify.py §3)")
        else:
            L += ["Printed total: NOT FOUND. The row directly below the year rows is neither labelled 'Total' nor an unlabelled subtotal with a number in the ladder column. Not guessed.", ""]
        if sc["split_2027"]:
            L += ["2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):", "",
                  "| kind | member | unsecured bank/notes? | shown | USD |", "|---|---|---|---:|---:|"]
            for x in sc["split_2027"]:
                L.append(f"| {x['kind']} | {x['member']} | {x['unsecured_bank_or_notes']} | {x['shown']} | {_fmt(x['value'])} |")
            L.append("")
            uns = [x for x in sc["split_2027"] if x["kind"] == "instrument" and x["unsecured_bank_or_notes"]]
            if uns:
                tot = sum(x["value"] for x in uns)
                claim(claims, f"{tk}.wall_2027_unsecured_split",
                      f"{d['label']}: ${tot/1e6:,.1f}M of the 2027 bucket is tagged to " + " + ".join(x["member"] for x in uns),
                      sc["url"], "inferred", "no", "column mapping from XBRL member names; a human must confirm against the printed table header")
            for x in sc["split_2027"]:
                if x["kind"] == "jv_share" and x["value"]:
                    claim(claims, f"{tk}.jv_debt_2027", f"{d['label']}: share of joint-venture debt due 2027 = ${x['value']/1e6:,.1f}M "
                          "(CONTEXT ONLY, not in the wall)", sc["url"], "inferred", "no", f"member {x['member']}")
        spot_results[d["cik"]] = {**sc, "ladder_sum": lsum, "ticker": tk, "name": d["label"]}
        if sc["dimensioned"]:
            L += [f"Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): {len(sc['dimensioned'])}", ""]
            for t, cref, shown, v in sc["dimensioned"][:30]:
                L.append(f"- {t.replace('LongTermDebtMaturitiesRepaymentsOfPrincipal', '…')} ctx={cref} shown={shown} → {_fmt(v)}")
            L.append("")
    done = [spot_results[c]["name"] for c in spot_results]
    others = [d["label"] for d in names if d["cik"] not in cfg["spot_check_ciks"]]
    L += [f"**Ladders checked number by number against 10-K text: {', '.join(done) or 'none'}.**", "",
          f"Not checked against 10-K text (companyfacts vs frames only): {', '.join(others + not_done) or 'none'}.", ""]
    (PROC / "filing_text_checks.json").write_text(json.dumps(spot_results, indent=1, default=str))

    # §3b filing window (report v1 review item 1)
    fw = cfg.get("checks", {}).get("filing_window")
    if fw:
        dw = next((d for d in names if d["cik"] == fw["cik"]), None)
        L += [f"## 3b. Filing list check: {dw['label'] if dw else fw['cik']}, all forms, {fw['from']} to {fw['to']}", "", f"Question: {fw['reason']}", ""]
        if dw:
            rec = json.loads(open(dw["sub_path"], "rb").read())["filings"]["recent"]
            hits = [(rec["filingDate"][i], f, rec["items"][i], rec["accessionNumber"][i]) for i, f in enumerate(rec["form"])
                    if fw["from"] <= rec["filingDate"][i] <= fw["to"]]
            L += [f"Source: {event_reader.submissions_url(dw['cik'])} (cached {fetched_at_of(dw['sub_path'])})", "",
                  "| filed | form | items | accession |", "|---|---|---|---|"] + [f"| {a} | {b} | {c or 'none'} | {e} |" for a, b, c, e in hits]
            k8 = [h for h in hits if h[1].startswith("8-K")]
            y8 = [(rec["filingDate"][i], rec["items"][i]) for i, f in enumerate(rec["form"]) if f.startswith("8-K") and rec["filingDate"][i] >= cfg["events_since"]]
            L += ["", f"**Result: {len(hits)} filings in the window, {len(k8)} of them 8-K.** All 2026 8-Ks with their items: " + "; ".join(f"{a} [{b}]" for a, b in y8) + ".",
                  "The exhibits of the earnings 8-Ks (items 2.02/7.01) are searched in §3d below.", ""]
            claim(claims, f"{dw['ticker']}.no_8k_in_window", f"{dw['label']} filed {len(k8)} 8-K(s) between {fw['from']} and {fw['to']}; "
                  f"forms in window: {', '.join(sorted({h[1] for h in hits}))}", event_reader.submissions_url(dw["cik"]), "checked", "yes",
                  "EDGAR submissions filing list (verify.py §3b); earnings-8-K exhibits searched separately in §3d")
    # §3d exhibit search (earnings 8-K exhibits), verbatim sentence hits only
    xs = cfg.get("checks", {}).get("exhibit_search")
    if xs:
        dx = next((d for d in names if d["cik"] == xs["cik"]), None)
        L += [f"## 3d. Exhibit search: {dx['label'] if dx else xs['cik']} 8-Ks with item(s) {', '.join(xs['items'])} since {xs['since']}", "",
              f"Question: {xs['reason']}", f"Pattern (case-insensitive): `{xs['pattern']}`", ""]
        if dx:
            rec = json.loads(open(dx["sub_path"], "rb").read())["filings"]["recent"]
            k8 = [(rec["filingDate"][i], rec["accessionNumber"][i], rec["primaryDocument"][i]) for i, f in enumerate(rec["form"])
                  if f.startswith("8-K") and rec["filingDate"][i] >= xs["since"] and any(it in rec["items"][i].split(",") for it in xs["items"])]
            total_hits = 0
            for filed, acc, prim in sorted(k8):
                ix = fx.archive(dx["cik"], acc, "index.json")
                if not ix["path"]:
                    L += [f"### 8-K filed {filed} ({acc})", f"Filing index NOT fetched: {ix['error']} ({ix['url']}). Check not done for this filing.", ""]
                    continue
                items = json.loads(open(ix["path"], "rb").read()).get("directory", {}).get("item", [])
                # exhibits = every .htm document in the filing except the 8-K cover (primary document), XBRL viewer pages (R1.htm) and index pages
                exs = [it["name"] for it in items if it["name"].lower().endswith((".htm", ".html")) and it["name"] != prim
                       and not re.match(r"^R\d+\.htm$", it["name"]) and "index" not in it["name"].lower()]
                L += [f"### 8-K filed {filed} ({acc}): documents searched {', '.join(exs) or 'NONE found'} (cover {prim} excluded)", ""]
                for ex in exs:
                    r = fx.archive(dx["cik"], acc, ex)
                    if not r["path"]:
                        L += [f"- {ex}: fetch FAILED: {r['error']}. Not searched.", ""]
                        continue
                    txt = html_to_text(open(r["path"], "rb").read().decode("utf-8", errors="replace"))
                    hits = []
                    for m in re.finditer(xs["pattern"], txt, re.I):
                        s0 = txt.rfind(". ", 0, m.start()); s1 = txt.find(". ", m.end())
                        sent = txt[s0 + 2 if s0 != -1 else 0: s1 + 1 if s1 != -1 else len(txt)]
                        if sent not in hits:
                            hits.append(sent)
                    total_hits += len(hits)
                    for h in hits:  # sentences that describe a refinancing become claims (verbatim)
                        if re.search(r"refinanc|extended|bifurcat", h, re.I) and not any(c_["claim"] == h for c_ in claims):
                            n_ = sum(1 for c_ in claims if c_["claim_id"].startswith(f"{dx['ticker']}.exhibit_refi"))
                            claim(claims, f"{dx['ticker']}.exhibit_refi{n_}", h, r["url"], "measured", "no",
                                  f"verbatim sentence from exhibit {ex} to the 8-K filed {filed} (items {', '.join(xs['items'])}); verify.py §3d")
                    L.append(f"- {ex} ({r['url']}): **{len(hits)} matching sentence(s)**")
                    for h in hits[: xs["max_hits_per_doc"]]:
                        L.append(f"  - \u201c{h[:700]}\u201d")
                    if len(hits) > xs["max_hits_per_doc"]:
                        L.append(f"  - (+{len(hits) - xs['max_hits_per_doc']} more not printed)")
                    L.append("")
            L += [f"**Total matching sentences across {len(k8)} earnings 8-K(s): {total_hits}.**", ""]

    # §3c SLG column-mapping arithmetic (report v1 review item 6): term-loan column of the 10-Q maturity table
    try:
        ce = json.loads((PROC / "case_evidence.json").read_text())
    except FileNotFoundError:
        ce = {}
    mt = (ce.get("SLG", {}).get("tenq", {}) or {}).get("maturity_table") or []
    if mt and "1040971" in spot_results:
        L += ["## 3c. SLG column mapping: arithmetic confirmation (stays INFERRED until signed off)", ""]
        hdr = [h.strip() for h in mt[0].split("|")]
        ti = next((i for i, h in enumerate(hdr) if "Term Loan" in h), None)
        rows_v = [[c.strip() for c in r.split("|")] for r in mt[1:]]
        def val(x):
            return 0.0 if x in ("—", "-", "–") else float(x.replace(",", ""))
        # a labelled row has one more cell than the header; the unlabelled total row has exactly as many (a year label like "2027" looks numeric)
        year_rows = [r for r in rows_v if len(r) == len(hdr) + 1]
        total_row = next((r for r in rows_v if len(r) == len(hdr)), None)
        if ti is not None and total_row and year_rows and len(year_rows) + 1 == len(rows_v):
            parts = [(r[0], val(r[ti + 1])) for r in year_rows if val(r[ti + 1])]
            tot = val(total_row[ti])
            ok_sum = sum(v for _, v in parts) == tot
            L += [f"10-Q header column {ti + 1} = '{hdr[ti]}'. Non-zero cells: " + ", ".join(f"{a}: {v:,.0f}" for a, v in parts) +
                  f". Sum = {sum(v for _, v in parts):,.0f}; printed column total = {tot:,.0f}; **{'equal' if ok_sum else 'NOT equal'}**.", ""]
            p0 = next((c for c in claims if c["claim_id"] == "SLG.10q_2027_p0"), {}).get("claim", "")
            want = {"$100.0 million term loan": "100,000", "$300.0 million term loan": "300,000", "$750.0 million term loan": "750,000"}
            txt_ok = all(k in p0 for k in want) and all(any(f"{v:,.0f}" == w for _, v in parts) for w in want.values())
            L += [f"10-Q text names Term B $100.0M, Term A $300.0M, Term C $750.0M: **{'matches the column cells' if txt_ok else 'does NOT match'}**.", ""]
            tl = [x for x in spot_results["1040971"]["split_2027"] if x["member"] == "TermLoanMember"]
            k_ok = bool(tl) and tl[0]["value"] == 1_050_000_000
            kd = next((c["claim"] for c in claims if c["claim_id"].startswith("SLG.10k_2027_date") and "$1.05 billion term loan" in c["claim"]), "")
            L += [f"10-K 2027 cell tagged TermLoanMember = {_fmt(tl[0]['value']) if tl else 'missing'}; 10-K text: "
                  f"'{kd[:160]}…' → **{'consistent: Term Loan A $1.05B due May 15, 2027' if (k_ok and 'May 15, 2027' in kd) else 'NOT confirmed'}**.", ""]
            claim(claims, "SLG.mapping_check", f"SL Green column mapping, arithmetic: 10-Q term-loan column total {tot:,.0f} = "
                  + " + ".join(f"{v:,.0f}" for _, v in parts) + f" ({'equal' if ok_sum else 'NOT equal'}); "
                  f"10-K 2027 term-loan cell {_fmt(tl[0]['value']) if tl else 'missing'} = Term Loan A $1.05B due May 15, 2027 ({'yes' if k_ok else 'no'})",
                  spot_results["1040971"]["url"], "inferred", "no", "arithmetic confirms the mapping; stays inferred until a human signs off (signoff.csv)")
        else:
            L += ["Could not parse the 10-Q maturity table into aligned columns; mapping NOT confirmed.", ""]

    L += ["## 4. Control total", "", "Primary: the 10-K table's printed Total (spot-checked names only). Secondary: LongTermDebt.", "",
          "| name | ladder sum | 10-K printed total | diff | LongTermDebt @2025-12-31 | diff | latest LongTermDebt (end) | diff |",
          "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for d in names:
        vals = [f["value"] for f in d["ladder"].values()]
        s = sum(v for v in vals if v is not None) if any(v is not None for v in vals) else None
        ye = ladder_extract.value_at(cf_paths[d["cik"]], ladder_extract.DEBT_TAG, cfg["ladder_period_end"])[0] if cf_paths[d["cik"]] else None
        lt = d["debt"]["value"]
        pt = (spot_results.get(d["cik"]) or {}).get("printed_total")
        ptv = pt["value"] if pt else None
        L.append(f"| {d['label']} | {_fmt(s)}{' (incomplete)' if None in vals else ''} | {_fmt(ptv) if pt else 'not checked'} | {_fmt(None if s is None or ptv is None else s - ptv)} | {_fmt(ye)} | {_fmt(None if s is None or ye is None else s - ye)} | "
                 f"{_fmt(lt)} ({d['debt']['period_end'] or d['debt']['gap_reason']}{', STALE' if d['debt']['value'] is not None and d['debt']['gap_reason'] else ''}) | {_fmt(None if s is None or lt is None else s - lt)} |")
    L += ["", "Differences are expected (unamortized discounts and issuance costs, fair-value hedges, tag scope). Not forced to match.", ""]

    case = [c for c in case_files]
    L += ["## 5. Quotes verbatim (re-fetch and re-match), case-file names: " + ", ".join(d["label"] for d in names if d["cik"] in case), "",
          "| claim | item | filed | exact re-extract | substring of fresh text | how | gap |", "|---|---|---|---|---|---|---|"]
    for d in [n for n in names if n["cik"] in case]:
        for q in recheck_quotes(fx, d, cfg, offline):
            L.append(f"| {q['claim_id']} | {q['item']} | {q['filed']} | {'yes' if q['match'] else '**NO**'} | {'yes' if q['in_text'] else '**NO**'} | {q['how']} | {q['gap'] or ''} |")
            c = claim_by_id.get(q["claim_id"])
            if c and q["match"] and q["in_text"] and q["refetched"]:
                c["checked"] = "yes"; c["note"] += "; quote re-fetched and matched verbatim (verify.py §5)"
    L.append("")

    L += ["## 6. Override quotes: is each quote verbatim in the filing behind its claim_id?", "",
          "| name | claim_id | quote found in filing text | filing |", "|---|---|---|---|"]
    ev_by_claim = {e.get("claim_id"): e for d in names for e in d["events"] if e.get("claim_id")}
    for ov in synthesize.read_overrides().values():
        e = ev_by_claim.get(ov.get("claim_id"))
        doc, url = (e or {}).get("doc_path"), (e or {}).get("filing_url")
        if not e:  # a non-8-K evidence claim (e.g. a 10-Q extract): open the cached filing named by its source_url
            cl = claim_by_id.get(ov.get("claim_id"))
            m = re.search(r"/data/(\d+)/(\d{18})/([^/]+)$", (cl or {}).get("source_url", ""))
            if m:
                url = cl["source_url"]
                doc = latest_cached_archive(f"{m.group(1)}_{m.group(2)}_{m.group(3)}")
        found = bool(doc) and ov["quote"] in html_to_text(open(doc, "rb").read().decode("utf-8", errors="replace"))
        L.append(f"| {ov['name']} | {ov.get('claim_id')} | {'yes' if found else '**NO**'} | {url or 'claim not found'} |")
    L.append("")

    # §7 10-Q ladder calendar mapping: overlapping years against the 10-K (display-only data, never scored)
    L += ["## 7. 10-Q ladder: calendar-year mapping check", "",
          "10-Q tags are read as: RemainderOfFiscalYear = rest of the current year, InNextTwelveMonths = next year, InYearTwo = the year after, and so on.",
          "If that mapping is right, years with no refinancing activity carry the same principal in both filings. Raw values below ($), no pass/fail threshold.", "",
          "| name | 10-Q period | year | 10-K value | 10-Q value | equal |", "|---|---|---|---:|---:|---|"]
    n_eq = n_cmp = 0
    kmap = {"2027": "y2_2027", "2028": "y3_2028", "2029": "y4_2029", "2030": "y5_2030"}
    for d in names:
        q = d.get("qladder") or {}
        if not q.get("buckets"):
            L.append(f"| {d['label']} | n/a | n/a | n/a | n/a | {q.get('gap_reason', 'not extracted')} |")
            continue
        for b_ in q["buckets"]:
            if b_["label"] in kmap:
                kv, qv = d["ladder"][kmap[b_["label"]]]["value"], b_["fact"]["value"]
                eq = kv is not None and qv is not None and abs(kv - qv) < 1
                n_cmp += int(kv is not None and qv is not None); n_eq += int(eq)
                L.append(f"| {d['label']} | {q['period_end']} | {b_['label']} | {_fmt(kv)} | {_fmt(qv)} | {'yes' if eq else 'no'} |")
    L += ["", f"**{n_eq} of {n_cmp} overlapping year values are equal.** Unequal values are expected where debt was refinanced, repaid or drawn after year-end.", ""]

    L += ["## Conflicts and gaps", ""]
    for c in conflicts:
        L.append(f"- CONFLICT {c['name']} / {c['tag']}: kept {c['value_a']}, others {c['value_b']}. {c['reason']}")
    for name, tag, a10k, (av, aacc, aform) in resolved:
        L.append(f"- RESOLVED (plumbing: period-selection) {name} / {tag}: raw row before the fix: A=n/a ({a10k[1]}) vs B={av:,.0f} ({aacc}). "
                 f"Evidence: companyfacts holds this {cfg['ladder_period_end']} value only as a comparative in 10-Q filings ({aform} {aacc} is the latest), "
                 f"and the frames API takes the latest filing for the instant. Fix: side A now applies the same rule; the values agree.")
    for d in names:
        for k, f in list(d["ladder"].items()) + [("latest_cash", d["cash"]), ("latest_debt", d["debt"])]:
            if f["gap_reason"] and f["value"] is None:
                L.append(f"- GAP {d['label']} / {k}: {f['gap_reason']}. Action: left as missing.")
            elif f["gap_reason"]:
                L.append(f"- FALLBACK {d['label']} / {k}: {f['gap_reason']} (end {f['period_end']}). Action: older value kept and flagged, not replaced.")
        if d["ev_gap"]:
            L.append(f"- GAP {d['label']} / events: {d['ev_gap']}")
        for e in d["events"]:
            if event_reader.needs_document(e) and not e.get("quote"):
                L.append(f"- GAP {d['label']} / quote {e['item_code']} {e['filed']}: {e.get('quote_gap')}")
        if d["drawdown"]["gap_reason"]:
            L.append(f"- GAP {d['label']} / price: {d['drawdown']['gap_reason']}. Market view not scored; name left out of the sector median.")
    L.append("")
    (ROOT / "verification.md").write_text("\n".join(L))
    def _section_table(title_prefix):
        i = next((k for k, x in enumerate(L) if x.startswith(title_prefix)), None)
        if i is None:
            return [], []
        tbl = []
        for x in L[i + 1:]:
            if x.startswith("## "):
                break
            if x.startswith("|"):
                tbl.append([c.strip() for c in x.strip("|").split("|")])
        return (tbl[0], [r for r in tbl[2:]]) if len(tbl) >= 2 else ([], [])
    ctl_hdr, ctl_rows = _section_table("## 4. Control total")
    ci = next((k for k, x in enumerate(L) if x.startswith("## Conflicts and gaps")), len(L))
    conflict_lines = [x[2:] for x in L[ci + 1:] if x.startswith("- ")]
    same_counts = {"same": sum(1 for r in rows if r[4] == "yes"), "both_missing": sum(1 for r in rows if r[4] == "both missing")}
    (PROC / "verification_summary.json").write_text(json.dumps({
        "control_hdr": ctl_hdr, "control_rows": ctl_rows, "conflict_lines": conflict_lines, **same_counts,
        "resolved_cross": [{"name": n, "tag": tg, "a_before": "n/a", "a_before_reason": a10k[1], "b": av, "b_accn": aacc, "b_form": aform,
                            "a_source": "https://data.sec.gov/api/xbrl/companyfacts/", "b_source": f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tg}/USD/CY2025Q4I.json"}
                           for n, tg, a10k, (av, aacc, aform) in resolved],
        "control_pass": ok, "control_msg": msg[0], "cross_pairs": len(rows), "cross_diffs": len(diffs),
        "spot_checked": {spot_results[c]["ticker"]: {"rows_equal": sum(1 for r in spot_results[c]["rows"] if r[2] is not None and r[2] == r[3]),
                                                     "rows": len(spot_results[c]["rows"]),
                                                     "printed_total": (spot_results[c].get("printed_total") or {}).get("value"),
                                                     "ladder_sum": spot_results[c]["ladder_sum"], "url": spot_results[c]["url"]}
                         for c in spot_results},
        "not_spot_checked": others + not_done, "conflicts": conflicts, "offline": offline}, indent=1, default=str))
    synthesize.write_claims(claims)
    print("\n".join(L[:12]))
    return ok
