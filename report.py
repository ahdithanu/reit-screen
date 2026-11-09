"""report.py: builds the dashboard (report.html and public/index.html) from processed outputs only.

The page design lives in design/template.html. This module fills its embedded data block (D).
It never computes a new metric: every number comes from metrics.csv, flags.json, claims.csv,
case_evidence.json, filing_text_checks.json, verification_summary.json or overlay_result.csv.
Narrative sentences are generated from those values, and a sentence is left out (or replaced by
a neutral one) when the evidence it depends on is missing. Citations are written as [[claim_id]]
and rendered as clickable tags by the page.
"""
import calendar
import csv
import datetime as dt
import json
import re
import shutil
from html import escape as E

from common import PROC, ROOT

BUCKETS = ["ACT NOW", "WATCH", "CAN'T CALL", "ROUTINE"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def _csv(path):
    return list(csv.DictReader(open(path, newline=""))) if path.exists() else []


def _pct(v):
    return "gap" if v in ("", None) else f"{float(v) * 100:.1f}%"


def _num(v, f="{:,.1f}"):
    return "gap" if v in ("", None) else f.format(float(v))


def _month_add(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return dt.date(y, m, 1)


def musd_from_thousands(cell):
    """A filing cell in $ thousands (e.g. '125,000') as $ millions text ('125.0'). Display only."""
    return f"{float(cell.replace(',', '')) / 1000:,.1f}"


EMPTY_CELLS = ("\u2014", "\u2013")  # em and en dash: the filer's empty-cell marker


def display_table_row(raw):
    """A verbatim filing-table row with empty cells shown as n/a. The raw row stays in the ledger (claims.csv)."""
    return " | ".join("n/a" if c.strip() in EMPTY_CELLS else c.strip() for c in raw.split("|"))


# ---------------------------------------------------------------- dated maturities from verbatim 10-Q text
AMT = r"\$([\d,]+(?:\.\d+)?) (million|billion)"
MON = r"(" + "|".join(MONTHS) + r") (\d{4})"


def _sentences(text):
    parts = re.split(r"(?<=[.;])\s+|\s*•\s*", text)
    return [p.strip() for p in parts if p.strip()]


def extract_clocks(tk, claims, ev, as_of):
    """Deterministic: amount + instrument + month/year (or exact m/d/yyyy) stated in one verbatim 10-Q sentence or table row."""
    tq = ev.get("tenq", {})
    period = f"10-Q, period {tq.get('period')}, filed {tq.get('filed')}"
    out = []
    for cid in sorted(k for k in claims if k.startswith(f"{tk}.10q_2027_p")):
        for sent in _sentences(claims[cid]["claim"]):
            for m in re.finditer(AMT + r" ([^$]{0,60}?(?:term loan|notes|mortgage|loan))[^$]{0,120}?(?:maturity of|maturing in|matures in|maturity is for [^$]*? in) " + MON, sent, re.I):
                name = re.search(r'\((?:or the )?"([^"]+)"\)', sent[m.start():m.end() + 40])
                what = (name.group(1) if name else m.group(3)).replace(" Loans", " loan").strip()
                amt = f"${m.group(1)}{'M' if m.group(2).lower() == 'million' else 'B'}"
                out.append({"tk": tk, "what": what, "amt": amt, "mon": m.group(4), "yr": int(m.group(5)), "exact": None,
                            "cid": cid, "quote": sent, "period": period})
            m2 = re.search(r"maturity is for " + AMT + r" in " + MON, sent)
            if m2:
                out.append({"tk": tk, "what": "Next mortgage maturity", "amt": f"${m2.group(1)}M", "mon": m2.group(3), "yr": int(m2.group(4)),
                            "exact": None, "cid": cid, "quote": sent, "period": period})
    for cid in sorted(k for k in claims if k.startswith(f"{tk}.10q_debtrow")):
        cells = [c.strip() for c in claims[cid]["claim"].split("|")]
        d = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", cells[-1]) if cells else None
        if d and len(cells) > 1 and re.match(r"^[\d,]+$", cells[1]):
            amt = f"${musd_from_thousands(cells[1])}M"
            out.append({"tk": tk, "what": cells[0], "amt": amt, "mon": MONTHS[int(d.group(1)) - 1], "yr": int(d.group(3)),
                        "exact": f"{d.group(3)}-{int(d.group(1)):02d}-{int(d.group(2)):02d}", "cid": cid,
                        "quote": f"{cells[0]}: {amt}, matures {cells[-1]}", "label": "From the 10-Q debt table, amount converted from $ thousands to $M,",
                        "period": period})
    seen, res = set(), []
    for e in out:
        key = (e["amt"], e["mon"], e["yr"])
        if key in seen:
            continue
        seen.add(key)
        mi = MONTHS.index(e["mon"]) + 1
        e["m0"] = f"{e['yr']}-{mi:02d}-01"
        e["m1"] = f"{e['yr']}-{mi:02d}-{calendar.monthrange(e['yr'], mi)[1]:02d}"
        e["when"] = (dt.date.fromisoformat(e["exact"]).strftime("%-m/%-d/%Y") if e["exact"] else f"{e['mon']} {e['yr']}")
        res.append(e)
    return res


# ---------------------------------------------------------------- build D
def limits_lines(vs, n_review, n_claims, lc):
    """Plain-sentence limits, every number derived from the run."""
    out = [
        "The decision-maker persona (a credit officer at a bank in syndicated unsecured REIT loans) is an assumption. No credit practitioner has validated it.",
        "Every bucket threshold is an assumption, set in config.toml with a one-line reason.",
        "Prices come from the unofficial Yahoo chart API (daily closes, not adjusted for dividends). It can change or block requests at any time.",
        "There is no interest coverage ratio, because InterestExpense is not tagged consistently, and no undrawn revolver data, because it is not tagged. Liquidity from cash alone understates the picture.",
        "Ladders are as of the FY2025 10-K (2025-12-31) unless a 10-Q ladder is shown. 10-Q ladders are display only and never scored.",
        f"{lc['k_label']}. {lc['q_label']}.",
        f"{n_review} of {n_claims} claims are human reviewed (listed in signoff.csv)."
        + (" No claim is human signed off." if n_review == 0 else " Every other claim is machine-extracted or machine-checked only."),
        "The ladder does not separate secured property-level mortgages from unsecured debt, and does not show extension options. A large wall is not the same as refinancing risk for the unsecured facility.",
    ]
    diffs = vs.get("cross_diffs", 0)
    line = f"The cross-extraction compared {vs['cross_pairs']} value pairs (companyfacts against the SEC frames API) and found {diffs} difference{'s' if diffs != 1 else ''}."
    for r in vs.get("resolved_cross", []):
        line += (f" One earlier difference was a plumbing artifact (period selection), now fixed: {E(r['name'])} reports its 2025-12-31 {E(r['tag'])} only as a "
                 f"comparative in its 10-Qs, which a 10-K-only reader missed. Raw row before the fix: "
                 f"<code>{E(r['name'])} | {E(r['tag'])} | A = n/a ({E(r['a_before_reason'])}) | B = {r['b']:,.0f} ({E(r['b_accn'])}, {E(r['b_form'])})</code>.")
    out.append(line)
    return out


def review_line(n, m):
    return f"{n} of {m} claims human reviewed" + (" (none yet)" if n == 0 else "")


def build_data(cfg):
    rows = _csv(PROC / "metrics.csv")
    flags = json.load(open(PROC / "flags.json"))
    claims_rows = _csv(ROOT / "claims.csv")
    claims = {}
    for c in claims_rows:
        rec = {"claim": c["claim"], "src": c["source_url"], "tag": c["tag_type"], "checked": c["checked"] == "yes", "note": c["note"]}
        if re.search(r"\.10q_(table_r|debtrow)\d+$", c["claim_id"]):  # a filing-table row: n/a for empty cells on screen, raw kept
            rec["raw"] = c["claim"]
            rec["claim"] = display_table_row(c["claim"])
        claims[c["claim_id"]] = rec
    events = _csv(PROC / "events.csv")
    case = json.load(open(PROC / "case_evidence.json"))
    spot = json.load(open(PROC / "filing_text_checks.json"))
    vs = json.load(open(PROC / "verification_summary.json"))
    ovl = _csv(PROC / "overlay_result.csv")
    overrides = _csv(ROOT / "overrides.csv")
    signoff = [r for r in _csv(ROOT / "signoff.csv") if r.get("claim_id")]
    as_of = dt.date.fromisoformat(cfg["as_of"])
    by_t = {r["ticker"]: r for r in rows}
    name_t = {r["name"]: r["ticker"] for r in rows}
    ctl = next(r["ticker"] for r in rows if r["cik"] == cfg["pipeline_control"]["cik"])
    case_order = sorted([t for t in by_t if by_t[t]["case_file"] == "True"], key=lambda t: int(by_t[t]["priority_rank"]))
    has = lambda cid, *ph: cid in claims and all(p in claims[cid]["claim"] for p in ph)

    # ---- overrides, with their evidence lists
    ov_out = []
    for o in overrides:
        t = name_t.get(o["name"])
        if not t:
            continue
        ev_ids = [o.get("claim_id")] + [k for k in claims if k.startswith(f"{t}.ev") and k.endswith(("2.03", "1.03"))][:2]
        sup = [k for k in (f"{t}.mapping_check", f"{t}.y1_2026_share", f"{t}.latest_debt", f"{t}.latest_cash", f"{t}.printed_total",
                           f"{t}.10q_table_r2", f"{t}.exhibit_refi2") if k in claims]
        short = o["bucket"].split("(")[0].strip()
        if "reason changed" in o["bucket"]:
            short += ", reason changed"
        ov_out.append({**o, "ticker": t, "short": short, "ev": list(dict.fromkeys(i for i in ev_ids if i)), "sup": sup})

    # ---- screen rows
    screen = []
    order = [by_t[ctl]] + sorted([r for r in rows if r["ticker"] != ctl], key=lambda r: int(r["priority_rank"]))
    for r in order:
        t = r["ticker"]
        fl = [f["flag"] for f in flags["names"][t]["flags"] if f["flag"] not in ("wall_share_upper_bound_below_watch", "refinancing_tag")]
        if r["wall_2027_share_is_upper_bound"] == "True":
            fl.append("2027 share is an upper bound")
        ladder_gap = next((r[k] for k in r if k.startswith("ladder_") and k.endswith("_gap") and r[k]), "")
        gaps = [g for g in (r["price_gap"], ladder_gap) if g]
        sh = "gap" if r["wall_2027_share"] == "" else _pct(r["wall_2027_share"]) + (" (UB)" if r["wall_2027_share_is_upper_bound"] == "True" else "")
        screen.append({
            "rank": "test" if t == ctl else r["priority_rank"], "ticker": t, "name": r["name"], "sector": r["segment"], "code": r["bucket"],
            "override": r["override_bucket"] or None, "wall": [_num(r["wall_2027_musd"], "{:,.0f}"), sh, f"{t}.ladder_y2_2027"],
            "sh26": [_pct(r["y1_2026_share"])], "dd": [_pct(r["drawdown_52w"]),
                                                       "gap" if r["rel_drawdown"] == "" else f"{float(r['rel_drawdown']) * 100:+.1f} pts", f"{t}.drawdown_52w"],
            "pts": f"{r['filings_risk']} / {r['market_view'] if r['market_view'] != '' else '–'}",
            "wallcash": _num(r["wall_to_cash_display_only"], "{:,.1f}x"), "flags": fl, "gap": gaps, "refi": bool(r["refinancing_tag"]),
            "disagreement": r["disagreement"] or None,
            "wallq": (f"10-Q {r['q_period_end']}: {_pct(r['q_2027_share'])}" + (" (UB)" if r["q_2027_share_is_upper_bound"] == "True" else "")
                      + ("" if r["q_mapping_confirmed"] == "True" else ", year mapping unconfirmed") if r["q_2027_share"] != ""
                      else ("10-Q ladder: not tagged" if r["q_gap"] else "")),
            "wallq_cid": f"{t}.q_wall_2027_share" if r["q_2027_share"] != "" else None,
            "secured": (f"secured {_pct(r['secured_share'])} of debt ({r['secured_period_end']})" if r["secured_share"] != "" else None),
            "wall_gap": ("rolling-window maturity tags, not a dated ladder (not used, so CAN'T CALL)" if "Rolling" in ladder_gap
                         else ladder_gap or ("2027 bucket missing" if r["wall_2027_share"] == "" else "")),
            "dd_gap": r["price_gap"] or "price data missing"})

    # ---- ladders and case files
    def ladder(t):
        r = by_t[t]
        keys = [("y1_2026", "2026"), ("y2_2027", "2027"), ("y3_2028", "2028"), ("y4_2029", "2029"), ("y5_2030", "2030"), ("after_2030", "Later")]
        return [{"label": lab, "claim": f"{t}.ladder_{k}", "v": None if r[f"ladder_{k}_musd"] == "" else float(r[f"ladder_{k}_musd"]),
                 "note": r[f"ladder_{k}_gap"]} for k, lab in keys]

    ladders, cases = {}, {}
    for t in case_order:
        r, f, ev = by_t[t], flags["names"][t], case.get(t, {})
        ladders[t] = ladder(t)
        det = f.get("detail") or {}
        s = det.get("series") or []
        pts = []
        if len(s) > 1:
            ys = [p[1] for p in s]
            lo, hi = min(ys), max(ys)
            pts = [[round(i / (len(ys) - 1) * 360, 1), round(60 - (y - lo) / ((hi - lo) or 1) * 60, 1)] for i, y in enumerate(ys)]
        pricenote = (f"{s[0][0]} → {s[-1][0]}: high {det['high_close']:.2f} on {det['high_date']}, last {det['last_close']:.2f}. Unofficial (Yahoo). [[{t}.drawdown_52w]]"
                     if s else "No price series (gap).")
        blocks = []
        q8 = [e for e in events if e["name"] == r["name"] and e["class"] != "other"]
        blocks.append({"h": "2026 8-K items (verbatim, first 400 characters)", "items": [
            {"type": "quote", "meta": f"{e['form']} filed {e['filed']}, item {e['item_code']} ({e['class']})", "href": e["filing_url"],
             "cid": e["claim_id"], "text": e["quote"] or f"quote missing: {e['quote_gap']}"} for e in q8]
            or [{"type": "p", "html": "No 2026 negative or financing 8-K items.", "cls": ["small"]}]})
        tq = ev.get("tenq", {})
        items = [{"type": "quote", "meta": "", "href": None, "cid": f"{t}.10q_2027_p{i}", "text": p} for i, p in enumerate(tq.get("paragraphs", []))]
        for i, row in enumerate(tq.get("debt_rows_2027", [])):
            c_ = [x.strip() for x in row.split("|")]
            amt = f"${musd_from_thousands(c_[1])}M" if len(c_) > 1 and re.match(r"^[\d,]+$", c_[1]) else "amount not stated"
            items.append({"type": "p", "cls": None, "html": f"<b>10-Q debt table row</b> (amount converted from $ thousands): {E(c_[0])}, {amt}"
                                                            + (f", matures {E(c_[-1])}" if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", c_[-1]) else "")
                                                            + f". The filing's own row is in the claims ledger [[{t}.10q_debtrow{i}]]."})
        if tq.get("maturity_table"):
            items += [{"type": "p", "html": "10-Q maturity table, verbatim rows, $ thousands:", "cls": ["small"]},
                      {"type": "pre", "text": "\n".join(tq["maturity_table"])}]
        blocks.append({"h": f"Latest 10-Q on 2027 debt (filed {tq.get('filed', '?')}, period {tq.get('period', '?')})",
                       "items": items or [{"type": "p", "html": "No 10-Q paragraph matched.", "cls": ["small"]}]})
        tk_ = ev.get("tenk", {})
        blocks.append({"h": "Dated 2027 maturities in the FY2025 10-K text", "items": [{"type": "ul", "li": [
            f"<b>{E(x['date'])}</b>: “{E(x['sentence'])}” [[{t}.10k_2027_date{i}]]" for i, x in enumerate(tk_.get("dates", []))]
            or ["No dated 2027 debt sentence found in the 10-K text."]}]})
        fl_ = f["flip"]
        fitems = []
        if fl_ and fl_.get("nearest"):
            n = fl_["nearest"]
            fitems.append({"type": "p", "html": f"Nearest threshold: <code>{E(n['threshold'])}</code>, now {n['current']}. This name sits at {n['metric_value']:.4g}, "
                                                f"so the threshold would have to move <b>{n['distance_pct'] * 100:.1f}%</b> to change the bucket to {E(n['new_bucket'])}. "
                                                f"[[CFG.{n['threshold'].rsplit('.', 1)[0]}]]", "cls": None})
            fitems.append({"type": "p", "html": f"<b>New fact that would flip it:</b> {E(fl_['words'])}", "cls": None})
            if len(fl_["rows"]) > 1:
                fitems.append({"type": "p", "html": "Other moves that flip it: " + "; ".join(
                    f"{E(x['threshold'])} by {x['distance_pct'] * 100:.1f}% → {E(x['new_bucket'])}" for x in fl_["rows"][1:]), "cls": ["small", "muted"]})
        else:
            fitems.append({"type": "p", "html": E((fl_ or {}).get("words", "not computed")), "cls": None})
        blocks.append({"h": "Flip test", "items": fitems})
        sc = vs["spot_checked"].get(t)
        li = [f"Ladder checked number by number against the 10-K table by code: {sc['rows_equal']}/{sc['rows']} equal; printed total "
              f"{_num(sc['printed_total'], '{:,.0f}')} vs bucket sum {_num(sc['ladder_sum'], '{:,.0f}')}" + (f" [[{t}.printed_total]]" if f"{t}.printed_total" in claims else "") + "."
              if sc else "<b>Ladder NOT checked against 10-K text.</b>",
              "8-K quotes re-fetched from sec.gov and matched verbatim by code.",
              "10-Q passages and 10-K dated sentences are verbatim extracts. Claude (AI) read them while building this. <b>No human has signed them off yet.</b>"]
        for k, txt in ((f"{t}.mapping_check", "Column-mapping arithmetic (stays inferred until signed off)"),
                       (f"{t}.ub_equals_printed", None), (f"{t}.wall_2027_unsecured_split", "2027 split by instrument, inferred from XBRL member names"),
                       (f"{t}.jv_debt_2027", "JV debt due 2027, context only, never in the wall")):
            if k in claims:
                li.append((f"{txt}: " if txt else "") + E(claims[k]["claim"]) + f" [[{k}]]")
        blocks.append({"h": "What was verified, and by whom", "items": [{"type": "ul", "li": li}]})
        cases[t] = {"blocks": blocks, "flagsline": E(f["why"]) + f" [[{r['bucket_claim_id']}]]" + (f" · disagreement: <b>{E(r['disagreement'])}</b>" if r["disagreement"] else ""),
                    "pts": pts, "pricenote": pricenote,
                    "pricestats": f"52w drawdown {_pct(r['drawdown_52w'])}; sector median {_pct(r['sector_median_drawdown'])};\n6-month return {_pct(r['return_6m_display_only'])} (display only)."}

    # ---- hero: a case file whose latest 10-Q maturity table restates the 10-K ladder year by year
    hero = None
    for t in case_order:
        mt = case.get(t, {}).get("tenq", {}).get("maturity_table") or []
        if len(mt) < 3 or f"{t}.10q_2027_p0" not in claims:
            continue
        hdr = [h.strip() for h in mt[0].split("|")]
        ti = next((i for i, h in enumerate(hdr) if h == "Total"), None)
        ji = next((i for i, h in enumerate(hdr) if "Joint Venture" in h), None)
        if ti is None:
            continue
        q10 = []
        for i, row in enumerate(mt[1:], start=1):
            c = [x.strip() for x in row.split("|")]
            if len(c) != len(hdr) + 1:
                continue
            val = lambda x: None if x in ("—", "-", "–") else int(x.replace(",", ""))
            lab = c[0].replace("Remaining ", "").replace("Thereafter", "Later")
            lab = lab + " rest" if c[0].startswith("Remaining") else lab
            q10.append({"label": lab, "claim": f"{t}.10q_table_r{i}", "total": val(c[ti + 1]), "jv": val(c[ji + 1]) if ji is not None else None})
        q27 = next((i for i, x in enumerate(q10) if x["label"] == "2027"), None)
        lad = ladder(t)
        if q27 is None or q10[q27]["total"] is None or lad[1]["v"] is None:
            continue
        para = claims[f"{t}.10q_2027_p0"]["claim"]
        ix = para.find("As of ")
        tq = case[t]["tenq"]
        amend = re.search(r"On ((?:" + "|".join(MONTHS) + r") \d{1,2}, \d{4}), the Company entered into an amended and restated credit facility", para)
        jv = q10[q27]["jv"]
        hero = {"tk": t, "year": "2027", "hot": 1, "qhot": q27, "ladder": lad, "q10": q10, "pcid": f"{t}.10q_2027_p0",
                "head": para[:ix].strip() if ix > 0 else para, "rest": para[ix:] if ix > 0 else "",
                "aria": f"{by_t[t]['name']} 2027 maturities, FY2025 10-K against the latest 10-Q",
                "caption": f"{by_t[t]['name']} principal due in 2027: FY2025 10-K against the 10-Q for {tq.get('period')}.",
                "k_caption": "FY2025 10-K ladder, $M, as of 2025-12-31", "k_cap": "$M, FY2025 10-K, as of 2025-12-31",
                "q_caption": f"10-Q ladder, period {tq.get('period')}, $M, same scale", "q_cap": f"$M, 10-Q filed {tq.get('filed')}, consolidated total column",
                "q_period": f"10-Q, period {tq.get('period')}, filed {tq.get('filed')}",
                "note": (f"2027 falls from ${lad[1]['v']:,.1f}M to ${q10[q27]['total'] / 1000:,.1f}M"
                         + (f" after the credit facility amendment of {amend.group(1)}" if amend else "") + f" [[{t}.10q_2027_p0]]. "
                         + (f"{t}'s share of joint-venture debt due 2027 is ${jv / 1000:,.1f}M and sits outside the consolidated figure [[{q10[q27]['claim']}]]." if jv else "")),
                "amend_date": amend.group(1) if amend else None}
        break

    # ---- clocks
    win_start = dt.date(as_of.year, as_of.month, 1)
    win_end = _month_add(win_start, 5) - dt.timedelta(days=1)
    labels = []
    for i in range(5):
        m = _month_add(win_start, i)
        labels.append(m.strftime("%b %Y") if i == 0 or m.month == 1 else m.strftime("%b"))
    clocks, clocks_off = [], []
    for t in case_order:
        if by_t[t]["bucket"] != "WATCH":
            continue
        for e in extract_clocks(t, claims, case.get(t, {}), as_of):
            d0 = dt.date.fromisoformat(e["exact"] or e["m1"])
            if d0 < as_of:
                continue
            (clocks if dt.date.fromisoformat(e["exact"] or e["m0"]) <= win_end else clocks_off).append(e)
    clocks_off = [e for e in clocks_off if dt.date.fromisoformat(e["m0"]) <= _month_add(win_start, 12)]
    clocks.sort(key=lambda e: e["exact"] or e["m0"])
    clock_tickers = list(dict.fromkeys(e["tk"] for e in clocks + clocks_off))

    # ---- narrative, generated with evidence guards
    live_act = [r for r in rows if r["bucket"] == "ACT NOW" and r["ticker"] != ctl]
    dis = [r for r in rows if r["disagreement"]]
    watch_cases = [t for t in case_order if by_t[t]["bucket"] == "WATCH"]
    if hero:
        hn = by_t[hero["tk"]]["name"]
        headline = (f"{hn}'s 10-K shows ${hero['ladder'][1]['v'] / 1000:.2f}B due in 2027. Its latest 10-Q shows ${hero['q10'][hero['qhot']]['total'] / 1e6:.2f}B"
                    + (f", after a credit facility amendment on {hero['amend_date']}." if hero["amend_date"] else "."))
    else:
        headline = f"{len(live_act)} live borrower(s) in ACT NOW; {len(dis)} filings-market disagreement(s)."
    finding = ("On public data, " + ("no live borrower is ACT NOW" if not live_act else ", ".join(r["ticker"] for r in live_act) + " " + ("is" if len(live_act) == 1 else "are") + " ACT NOW")
               + f"; {ctl} sits there as a pipeline test.")
    for r in dis[:1]:
        t = r["ticker"]
        finding += (f" {r['name']} is the one name where filings and market disagree ({E(r['disagreement'])}): {_pct(r['wall_2027_share'])} of its principal falls due in 2027 [[{t}.wall_2027_share]], "
                    f"and its stock trades {float(r['rel_drawdown']) * 100:+.1f} points against {r['segment']} peers [[{t}.rel_drawdown]].") if r["rel_drawdown"] != "" else ""
    answer_parts = [
        {"label": "Finding", "html": finding},
        {"label": "Recommendation", "html": (f"Keep {', '.join(watch_cases)} on WATCH and have a human read their 10-Q refinancing text." if watch_cases
                                             else "No case-file name is on WATCH.")},
        {"label": "Why now", "html": (f"Dated maturities start {clocks[0]['when']}." if clocks else "No dated maturity is named inside the next five months.")},
        {"label": "What would change it", "html": "A human reading of the filings recorded in overrides.csv, a FY2026 ladder, or the lender's own data."}]
    lede, lede_note = "", ""
    if hero:
        t = hero["tk"]
        r = by_t[t]
        lede = (f"<b>{E(r['name'])}: the annual ladder and the latest 10-Q disagree.</b> Its FY2025 10-K puts ${_num(r['wall_2027_musd'])}M, {_pct(r['wall_2027_share'])} of scheduled principal, "
                f"in 2027 [[{t}.ladder_y2_2027]] [[{t}.wall_2027_share]]" + (f", yet the stock trades only {float(r['rel_drawdown']) * 100:+.1f} pts against the {r['segment']} median [[{t}.rel_drawdown]]" if r["rel_drawdown"] != "" else "")
                + f". The latest 10-Q: “{E(hero['head'][:300])}” [[{hero['pcid']}]].")
        if f"{t}.no_8k_in_window" in claims:
            lede += f" {E(claims[t + '.no_8k_in_window']['claim'])} [[{t}.no_8k_in_window]]."
        if f"{t}.exhibit_refi2" in claims:
            lede += f" The refinancing is described in an earnings-release exhibit: “{E(claims[t + '.exhibit_refi2']['claim'])}” [[{t}.exhibit_refi2]]. An item-code screen never reads that exhibit."
        lede_note = ("Status: the 10-K ladder figures are checked against the 10-K table. The 10-Q passage and rows are verbatim extracts not yet re-checked by a human. "
                     "The code bucket is unchanged, because code never lowers a bucket from new text; a human records that call in overrides.csv.")

    whynow = []
    for t in [r["ticker"] for r in rows if r["bucket"] == "WATCH"]:
        es = [e for e in clocks + clocks_off if e["tk"] == t]
        whynow.append(f"<b>{t}</b>: " + ("; ".join(f"{E(e['what'])} {E(e['amt'])}, {E(e['when'])} [[{e['cid']}]]" for e in es)
                                         if es else "<span class='muted'>no dated maturity extracted (not a case file, or none named in the latest 10-Q)</span>"))
    rates = flags["rates_context"]
    rates_line = (f"Rates, context only and never scored: 10-year Treasury {rates['dgs10']['value']:.2f}% ({rates['dgs10']['change_12m']:+.2f} pts over 12 months) [[RATES.dgs10]], "
                  f"SOFR {rates['sofr']['value']:.2f}% [[RATES.sofr]]." if "value" in rates.get("dgs10", {}) and "value" in rates.get("sofr", {}) else "Rates: gap.")
    flipped = [o for o in ovl if o["flipped"] == "True"]
    overlay_example = (f"<b>Worked example:</b> {E(flipped[0]['name'])} is {E(flipped[0]['code_bucket'])} on public data. In the SYNTHETIC lender file: {E(flipped[0]['reasons'])}, "
                       f"so the overlay moves it to <b>{E(flipped[0]['overlay_bucket'])}</b>. [[OVL.{flipped[0]['ticker']}]]" if flipped else "In the SYNTHETIC lender file no name changes bucket.")
    n_checked = len(vs["spot_checked"])
    LADK = ["y1_2026", "y2_2027", "y3_2028", "y4_2029", "y5_2030", "after_2030"]
    k_names = [r["ticker"] for r in rows if any(r[f"ladder_{k}_musd"] != "" for k in LADK)]
    q_names = [r["ticker"] for r in rows if r["q_2027_share"] != ""]
    q_conf = [r["ticker"] for r in rows if r["q_mapping_confirmed"] == "True"]
    n_review = len([r for r in signoff if r["claim_id"] in claims])
    no_k_names = [r["ticker"] for r in rows if r["ticker"] not in k_names]
    k_checked = [t for t in vs["spot_checked"] if t in k_names]
    q_checked = [t for t in vs.get("q10_checked", []) if t in q_names]  # verify.py section 8: cell by cell against the 10-Q text
    ladder_counts = {"k_total": len(k_names), "k_checked": len(k_checked), "no_k": len(no_k_names), "no_k_names": no_k_names,
                     "k_unchecked": [t for t in k_names if t not in k_checked],
                     "q_total": len(q_names), "q_checked": len(q_checked), "q_unchecked": [t for t in q_names if t not in q_checked],
                     "q_confirmed": len(q_conf)}
    k_label = (f"{len(k_checked)} of {len(k_names)} 10-K ladders checked against filing text"
               + (f" (n/a, no tags: {', '.join(no_k_names)})" if no_k_names else ""))
    q_label = (f"{len(q_checked)} of {len(q_names)} 10-Q ladders checked against filing text"
               + (f" (not checked: {', '.join(t for t in q_names if t not in q_checked)})" if len(q_checked) < len(q_names) else ""))
    ladder_counts.update(k_label=k_label, q_label=q_label)
    tk_name = {r["ticker"]: r["name"] for r in rows}
    takeaways = {
        "hA": (("No live name is ACT NOW; " if not live_act else f"{len(live_act)} live name(s) ACT NOW; ") + f"{ctl} is there as the pipeline test."
               + (f" {dis[0]['ticker']} is the one live disagreement between filings and market." if len(dis) == 1 else f" {len(dis)} names show a filings-market disagreement." if dis else "")),
        "hB": (f"{len(clock_tickers)} WATCH case-file name(s) have a dated maturity named in their latest 10-Q: " + ", ".join(f"{e['tk']} {e['when']}" for e in clocks[:4]) + "."
               if clocks else "No dated maturity is named inside this window."),
        "hC": (f"{dis[0]['name']} is the one name where filings and market disagree." if len(dis) == 1 else f"{len(dis)} names show a disagreement." if dis else "No name shows a filings-market disagreement."),
        "hD": (f"{tk_name[hero['tk']]}'s 2027 figure falls between the 10-K and the latest 10-Q." if hero else "Case files show the evidence behind the top-ranked names."),
        "hE": f"Two SEC extractions were diffed on {vs['cross_pairs']} value pairs with {vs['cross_diffs']} difference(s); {k_label}; {q_label}; "
              + review_line(len([r for r in signoff if r["claim_id"] in claims]), len(claims)) + ".",
        "hF": (f"A lender's own file can only escalate a bucket: the SYNTHETIC sample moves {flipped[0]['ticker']} from {flipped[0]['code_bucket']} to {flipped[0]['overlay_bucket']}."
               if flipped else "A lender's own file can only escalate a bucket."),
        "hG": "This is a first read of public filings, and the limits below say where it fails."}

    th = {"wallWatch": round(cfg["filings_risk"]["wall_share_watch"]["value"] * 100), "wallSevere": round(cfg["filings_risk"]["wall_share_severe"]["value"] * 100),
          "y1": round(cfg["filings_risk"]["year1_unresolved"]["value"] * 100), "relWatch": round(cfg["market_view"]["rel_drawdown_watch"]["value"] * 100),
          "relSevere": round(cfg["market_view"]["rel_drawdown_severe"]["value"] * 100), "actF": cfg["buckets"]["act_now_filings_min"]["value"],
          "jointF": cfg["buckets"]["act_now_joint_filings_min"]["value"], "jointM": cfg["buckets"]["act_now_joint_market_min"]["value"]}
    tagcount = {}
    for c in claims.values():
        tagcount[c["tag"]] = tagcount.get(c["tag"], 0) + 1
    refreshed = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    price_as_of = max((r["price_as_of"] for r in rows if r["price_as_of"]), default=cfg["as_of"])
    return {
        "claims": claims, "overrides": ov_out, "signoff": signoff, "verification_md": (ROOT / "verification.md").read_text(),
        "as_of": cfg["as_of"], "refreshed": refreshed, "price_as_of": price_as_of, "pipeline_test": ctl,
        "eyebrow": f"Syndicate participation screen · public data only · as of {cfg['as_of']} · refreshed {refreshed}",
        "headline": headline, "lede": lede, "lede_note": lede_note, "answer_parts": answer_parts,
        "answer_html": " ".join(f"{p['label']}. {p['html']}" for p in answer_parts),
        "assume_html": "Written for a credit officer at a bank in unsecured REIT loans. That decision-maker is an assumption, not validated by any practitioner. Bucket meanings and every threshold are assumptions in config.toml.",
        "whynow": whynow, "whatchange": "<b>What would change it:</b> the flip test in each case file gives the nearest threshold and the new fact that would move it. "
                                         "Two things move calls without any threshold change: a human reading of filing text entered in overrides.csv, and a lender's own data (see section F).",
        "rates": rates_line, "screen": screen,
        "screen_foot": ("Ladder as of 2025-12-31 (FY2025 10-K). The 2026 share is the next-twelve-months bucket, mostly past now; the code never declares it resolved. "
                        "UB = upper bound: a bucket is missing, so the true share can only be lower. Prices are unofficial (Yahoo)."),
        "cases": cases, "case_order": case_order, "case_title": ", ".join(tk_name[t] for t in case_order) or "No case files",
        "ladders": ladders, "hero": hero,
        "overlay": [{"ticker": o["ticker"], "rating": o["internal_rating"], "headroom": f"{float(o['covenant_headroom_pct']):.1f}%", "undrawn": o["undrawn_revolver_musd"],
                     "matures": o["own_facility_maturity"], "bucket": f"{o['code_bucket']} → {o['overlay_bucket']}", "why": f"{o['reasons']} OVL.{o['ticker']}",
                     "claim": f"OVL.{o['ticker']}"} for o in ovl],
        "overlay_example": overlay_example, "overlay_cfg": {"headroom_min": cfg["overlay"]["covenant_headroom_min_pct"], "months": cfg["overlay"]["own_facility_months"]},
        "breaks": [x.format(n_office=sum(1 for r in rows if r["segment"] == "office"), n_retail=sum(1 for r in rows if r["segment"] == "retail"),
                            n_q=sum(1 for r in rows if r["q_2027_share"] != ""), n_qc=sum(1 for r in rows if r["q_mapping_confirmed"] == "True"),
                            n_sec=sum(1 for r in rows if r["secured_share"] != ""), n_all=len(rows), no_k=ladder_counts["no_k"]) for x in BREAKS],
        "week": WEEK, "limits": limits_lines(vs, n_review, len(claims), ladder_counts),
        "ladder_counts": ladder_counts,
        "footer": "Generated by deterministic code from cached public data (SEC EDGAR, FRED, Yahoo). No LLM calls in the data path.",
        "clocks": clocks, "clocks_off": clocks_off, "clock_tickers": clock_tickers,
        "clock_window": {"start": win_start.isoformat(), "end": win_end.isoformat(), "labels": labels},
        "clock_title": f"Dated maturities, {win_start.strftime('%B %Y')} to {win_end.strftime('%B %Y')}",
        "cross": {"pairs": vs["cross_pairs"], "diffs": vs["cross_diffs"], "same": vs.get("same", 0), "both_missing": vs.get("both_missing", 0)},
        "control": {"hdr": vs.get("control_hdr", []), "rows": vs.get("control_rows", [])},
        "ctl_note": "Differences against LongTermDebt are expected (unamortized discounts and issuance costs, fair-value hedges, tag scope). Not forced to match.",
        "conflicts": vs.get("conflict_lines", []), "control_result": vs["control_msg"].replace("**", ""), "control_pass": vs["control_pass"],
        "checked_names": ", ".join(tk_name.get(t, t) for t in vs["spot_checked"]) + ".", "checked_n": n_checked,
        "unchecked_names": ", ".join(vs["not_spot_checked"]) or "none",
        "tagcount": tagcount, "checkedcount": sum(1 for c in claims.values() if c["checked"]),
        "thresholds": th, "takeaways": takeaways,
        "review": {"n": len([r for r in signoff if r["claim_id"] in claims]), "m": len(claims)}}


BREAKS = [
    "<b>The annual ladder goes stale inside the year.</b> A facility amended mid-year (SLG, March 2026; JBGS's revolver) moves maturities that the FY2025 ladder still shows. Only 10-Q text shows the move.",
    "<b>8-K item codes miss refinancings.</b> SLG filed no 8-K item 1.01/2.03 for its March 2026 amendment; it was described in an earnings-release exhibit, which an item-code screen does not read.",
    "<b>Hard triggers cannot see an exit.</b> OPI stays ACT NOW after emerging from Chapter 11, because a 2026 item 1.03 fires either way.",
    "<b>A filer's mis-scaled tag passes every SEC endpoint.</b> CBL tagged its 2027 bucket at scale 0 instead of thousands; only the 10-K table's printed total exposed it.",
    "<b>Tags stop being filed.</b> Several names stopped tagging LongTermDebt years ago, and {no_k} of {n_all} names file no FY2025 ladder tags (CAN'T CALL). These show as stale or gap.",
    "<b>Relisted equity breaks the drawdown.</b> A short price history (OPI) makes the market view a gap. Yahoo is unofficial and can change or block at any time.",
    "<b>Sector medians are thin:</b> {n_office} office and {n_retail} retail names. One outlier moves the median.",
    "<b>Tag coverage limits the newer data.</b> {n_q} of {n_all} names tag a 10-Q ladder ({n_qc} with a calendar mapping confirmed against the 10-K), and {n_sec} tag a usable secured/unsecured split. The rest show as gaps."]
WEEK = [
    "<b>Confirm the 10-Q year mapping filer by filer</b> (it is unconfirmed where no overlapping year matches) and decide whether the newer ladder should drive buckets. Today it is display only.",
    "<b>Add the scale-mismatch and printed-total checks to every refresh alert</b>, so a new filing that breaks them is flagged the day it lands.",
    "<b>Separate secured from unsecured</b> using the debt-instrument XBRL dimensions where filers tag them.",
    "<b>Pull extension options and dated maturities for every name</b>, not only case files.",
    "<b>Have a credit practitioner review the persona and thresholds.</b> None is validated today."]
LIMITS = [
    "<b>No interest coverage ratio.</b> InterestExpense is not tagged consistently across these names.",
    "<b>No undrawn revolver data.</b> It is not tagged, so liquidity from cash alone understates the picture.",
    "<b>The ladder is as of December 31, 2025</b> (FY2025 10-K). The 2026 bucket is mostly past, and the code never declares it resolved.",
    "<b>Prices are unofficial</b> (Yahoo chart API), close prices not adjusted for dividends.",
    "<b>The persona has not been validated</b> by a practitioner. All thresholds are assumptions (config.toml).",
    "<b>The ladder does not separate secured property-level mortgages from unsecured debt, and does not show extension options.</b> A large wall is not the same as refinancing risk for the unsecured facility."]


def build(cfg):
    D = build_data(cfg)
    tpl = (ROOT / "design" / "template.html").read_text()
    blob = json.dumps(D, ensure_ascii=False).replace("</", "<\\/")  # safe inside <script>
    html = tpl.replace("__DATA__", blob, 1)
    (ROOT / "report.html").write_text(html)
    pub = ROOT / "public"
    (pub / "data").mkdir(parents=True, exist_ok=True)
    (pub / "index.html").write_text(html)
    for src, dst in (("claims.csv", "claims.csv"), ("verification.md", "verification.md"), ("data/processed/metrics.csv", "metrics.csv"),
                     ("overrides.csv", "overrides.csv"), ("signoff.csv", "signoff.csv")):
        shutil.copyfile(ROOT / src, pub / "data" / dst)
    missing = sorted({m for m in re.findall(r"\[\[([^\]]+)\]\]", blob) if m not in D["claims"]})
    if missing:
        print("report: MISSING claim ids:", missing)
    return len(D["claims"])
