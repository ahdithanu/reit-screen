"""Skill 5: synthesize. Scores, buckets, flags, disagreement and the flip test, from config.toml only.

Never fetches, never reads raw files, never uses rates, never lets an 8-K lower a bucket,
never edits the code bucket from an override.
"""
import copy
import csv
import json

from common import PROC, ROOT

M = 1e6


# ---------------------------------------------------------------- scoring core (pure)
def scoring_inputs(d, cfg):
    """Reduce one name's facts to the numbers the rules look at. No thresholds here."""
    lad = {k: f["value"] for k, f in d["ladder"].items()}
    present = {k: v for k, v in lad.items() if v is not None}
    total = sum(present.values()) if present else None
    complete = len(present) == 6
    y2, y1 = lad.get("y2_2027"), lad.get("y1_2026")
    share = y2 / total if (y2 is not None and total) else None
    y1_share = y1 / total if (y1 is not None and total) else None
    evs = d["events"]
    return {
        "complete": complete, "total": total, "y2": y2, "y1": y1,
        "share": share, "share_is_ub": (share is not None and not complete),
        "y1_share": y1_share,
        "hard": [e for e in evs if e["class"] == "negative" and e["hard_trigger"]],
        "scored_neg": [e for e in evs if e["class"] == "negative" and not e["hard_trigger"]],
        "financing": [e for e in evs if e["class"].startswith("financing")],
        "rel_dd": d["rel"][0],
    }


def score(x, cfg):
    fr, mv, bk, dg = cfg["filings_risk"], cfg["market_view"], cfg["buckets"], cfg["disagreement"]
    flags, cant = [], None
    # filings risk
    F = 0
    if x["share"] is None:
        cant = "2027 share not computable: YearTwo bucket missing or no ladder"
    elif x["share_is_ub"]:
        if x["share"] >= fr["wall_share_watch"]["value"]:
            cant = (f"2027 share upper bound {x['share']:.1%} (buckets missing) is at or above "
                    f"wall_share_watch {fr['wall_share_watch']['value']:.0%}; true share unknown")
        else:
            flags.append(("wall_share_upper_bound_below_watch", 0))
    else:
        if x["share"] >= fr["wall_share_severe"]["value"]:
            F += fr["wall_share_severe"]["points"]; flags.append(("wall_share_severe", fr["wall_share_severe"]["points"]))
        elif x["share"] >= fr["wall_share_watch"]["value"]:
            F += fr["wall_share_watch"]["points"]; flags.append(("wall_share_watch", fr["wall_share_watch"]["points"]))
    neg_pts = min(len(x["scored_neg"]) * fr["negative_event"]["points_per_filing"], fr["negative_event"]["cap"])
    if neg_pts:
        F += neg_pts; flags.append(("scored_negative_events", neg_pts))
    y1_flag = x["y1_share"] is not None and x["y1_share"] >= fr["year1_unresolved"]["value"]
    if y1_flag:
        flags.append(("year1_unresolved", 0))
    high_wall = any(s is not None and s >= fr["wall_share_watch"]["value"] for s in (x["share"], x["y1_share"]))
    words = [w.lower() for w in fr["refinancing_tag"]["debt_words"]]
    debt_fin = [e for e in x["financing"] if not e.get("quote") or any(w in e["quote"].lower() for w in words)]
    refi_tag = fr["refinancing_tag"]["text"] if (high_wall and debt_fin) else None
    # market view
    Mv = None
    if x["rel_dd"] is not None:
        Mv = 0
        if x["rel_dd"] >= mv["rel_drawdown_severe"]["value"]:
            Mv = mv["rel_drawdown_severe"]["points"]; flags.append(("rel_drawdown_severe", Mv))
        elif x["rel_dd"] >= mv["rel_drawdown_watch"]["value"]:
            Mv = mv["rel_drawdown_watch"]["points"]; flags.append(("rel_drawdown_watch", Mv))
    else:
        flags.append(("market_data_gap", 0))
    # disagreement
    disagree = None
    if Mv is not None:
        if (F >= dg["filings_high_min"] or x["hard"]) and Mv <= dg["market_calm_max"]:
            disagree = "filings say risk, market is calm"
        elif Mv >= dg["market_high_min"] and F <= dg["filings_clean_max"] and not x["hard"]:
            disagree = "market is selling off, filings are clean"
    if disagree:
        flags.append(("disagreement", 0))
    # bucket
    if x["hard"]:
        bucket, why = "ACT NOW", "hard trigger: " + ", ".join(sorted({e["item_code"] for e in x["hard"]}))
    elif cant:
        bucket, why = "CAN'T CALL", cant
    elif F >= bk["act_now_filings_min"]["value"]:
        bucket, why = "ACT NOW", f"filings_risk {F} >= {bk['act_now_filings_min']['value']}"
    elif Mv is not None and F >= bk["act_now_joint_filings_min"]["value"] and Mv >= bk["act_now_joint_market_min"]["value"]:
        bucket, why = "ACT NOW", f"filings_risk {F} and market_view {Mv} both at joint minimums"
    elif F == 0 and Mv == 0 and not y1_flag and not disagree:
        bucket, why = "ROUTINE", "no flags"
    else:
        reasons = [f for f, _ in flags if f != "wall_share_upper_bound_below_watch"]
        bucket, why = "WATCH", "flags: " + ", ".join(reasons) if reasons else "WATCH"
    return {"filings_risk": F, "market_view": Mv, "bucket": bucket, "why": why, "flags": flags,
            "disagreement": disagree, "refinancing_tag": refi_tag, "year1_unresolved": y1_flag, "debt_financing": debt_fin}


# ---------------------------------------------------------------- flip test
FLIP_THRESHOLDS = [
    ("filings_risk.wall_share_watch.value", "share", float),
    ("filings_risk.wall_share_severe.value", "share", float),
    ("filings_risk.year1_unresolved.value", "y1_share", float),
    ("market_view.rel_drawdown_watch.value", "rel_dd", float),
    ("market_view.rel_drawdown_severe.value", "rel_dd", float),
    ("buckets.act_now_filings_min.value", "F", int),
    ("buckets.act_now_joint_filings_min.value", "F", int),
    ("buckets.act_now_joint_market_min.value", "M", int),
]
FLIP_WORDS = {
    "share": "A 2026 financing 8-K that extends or repays 2027 maturities (read by a human, entered in overrides.csv), "
             "or a FY2026 10-K ladder whose 2027 share crosses the threshold.",
    "y1_share": "A human reading the 2026 financing 8-Ks and recording in overrides.csv that 2026 maturities were refinanced or repaid.",
    "rel_dd": "The stock's 52-week drawdown moving across the threshold relative to its sector median.",
    "F": "One more (or one fewer) scored filings point, e.g. a 2.06 impairment 8-K or a change in the 2027 share band.",
    "M": "A change in the market band, i.e. the sector-relative drawdown crossing 15 or 25 points.",
}


def _get(cfg, path):
    for p in path.split("."):
        cfg = cfg[p]
    return cfg


def _set(cfg, path, v):
    ps = path.split(".")
    for p in ps[:-1]:
        cfg = cfg[p]
    cfg[ps[-1]] = v


def flip_test(x, cfg, base):
    if base["bucket"] not in ("ACT NOW", "WATCH"):
        return None
    if x["hard"]:
        return {"nearest": None, "rows": [], "words": "Hard trigger: no threshold move changes this. Only a reversal of the "
                "event (e.g. emergence from Chapter 11, a late filing cured and the trigger removed by rule change) would."}
    rows = []
    for path, key, kind in FLIP_THRESHOLDS:
        t = _get(cfg, path)
        m = {"F": base["filings_risk"], "M": base["market_view"]}.get(key, x.get(key))
        if m is None:
            continue
        if kind is float:
            new = m + 1e-9 if m >= t else m
        else:
            new = m + 1 if m >= t else m
        c2 = copy.deepcopy(cfg)
        _set(c2, path, new)
        b2 = score(x, c2)["bucket"]
        if b2 != base["bucket"]:
            rows.append({"threshold": path, "current": t, "metric": key, "metric_value": m, "moved_to": new,
                         "distance_pct": abs(new - t) / abs(t) if t else None, "new_bucket": b2})
    rows.sort(key=lambda r: r["distance_pct"] if r["distance_pct"] is not None else 9e9)
    nearest = rows[0] if rows else None
    return {"nearest": nearest, "rows": rows,
            "words": FLIP_WORDS[nearest["metric"]] if nearest else "No single threshold move changes this bucket."}


# ---------------------------------------------------------------- outputs
def _musd(v):
    return None if v is None else round(v / M, 1)


def read_overrides():
    p = ROOT / "overrides.csv"
    if not p.exists():
        return {}
    with open(p, newline="") as f:
        return {r["name"].strip(): r for r in csv.DictReader(f) if r.get("name", "").strip()}


def run(names, cfg, rates):
    """names: list of per-name dicts assembled by run.py. Writes metrics.csv, events.csv, flags.json, claims.csv."""
    PROC.mkdir(parents=True, exist_ok=True)
    overrides = read_overrides()
    claims, rows, flags_out, ev_rows = [], [], {}, []

    def claim(cid, text, url, tag_type, note=""):
        claims.append({"claim_id": cid, "claim": text, "source_url": url or "", "tag_type": tag_type, "checked": "no", "note": note})
        return cid

    # assumptions (thresholds) as claims
    for path, _, _ in FLIP_THRESHOLDS:
        node = _get(cfg, path.rsplit(".", 1)[0])
        claim(f"CFG.{path.rsplit('.', 1)[0]}", f"{path} = {node['value']}: {node.get('reason', '')}", "config.toml", "assumed")

    for d in names:
        tk = d["ticker"] or f"CIK{d['cik']}"
        x = scoring_inputs(d, cfg)
        res = score(x, cfg)
        flip = flip_test(x, cfg, res)
        ids = {}
        for k, f in d["ladder"].items():
            if f["value"] is not None:
                ids[k] = claim(f"{tk}.ladder_{k}", f"{d['label']} {f['tag_or_form']} = ${_musd(f['value'])}M at {f['period_end']}",
                               f["source_url"], "measured", f"accn {f['accession']} filed {f['filed']}")
            else:
                ids[k] = claim(f"{tk}.ladder_{k}", f"{d['label']} {f['tag_or_form']} at {f['period_end']}: MISSING ({f['gap_reason']})",
                               f["source_url"], "measured", "gap")
        for key, f in (("cash", d["cash"]), ("debt", d["debt"])):
            ids[key] = claim(f"{tk}.latest_{key}",
                             f"{d['label']} {f['tag_or_form']} = ${_musd(f['value'])}M at {f['period_end']}" if f["value"] is not None
                             else f"{d['label']} {f['tag_or_form']}: MISSING ({f['gap_reason']})",
                             f["source_url"], "measured", f"accn {f['accession']} filed {f['filed']}" + (f"; {f['gap_reason']}" if f['gap_reason'] and f['value'] is not None else ""))
        if x["share"] is not None:
            ids["share"] = claim(f"{tk}.wall_2027_share",
                                 f"{d['label']} 2027 maturities are {x['share']:.1%} of the {'buckets present (UPPER BOUND)' if x['share_is_ub'] else 'six-bucket total'}",
                                 "", "inferred", f"= {ids['y2_2027']} / sum of ladder claims")
        if x["y1_share"] is not None:
            ids["y1_share"] = claim(f"{tk}.y1_2026_share", f"{d['label']} 2026 maturities were {x['y1_share']:.1%} of the ladder"
                                    + (" (UPPER BOUND)" if x["share_is_ub"] else ""), "", "inferred", f"= {ids['y1_2026']} / ladder sum")
        dd, r6 = d["drawdown"], d["return_6m"]
        ids["dd"] = claim(f"{tk}.drawdown_52w", f"{tk} closed {dd['value']:.1%} below its 52-week high on {dd['period_end']}" if dd["value"] is not None
                          else f"{tk} drawdown: MISSING ({dd['gap_reason']})", dd["source_url"], "measured" if dd["value"] is not None else "measured", "unofficial source")
        if x["rel_dd"] is not None:
            ids["rel"] = claim(f"{tk}.rel_drawdown", f"{tk} drawdown is {x['rel_dd']*100:+.1f} pts vs the {d['segment']} median "
                               f"({d['rel'][1]:.1%}, {len(d['rel'][2])} peers)", "", "inferred", "peers: " + ",".join(d["rel"][2]))
        ev_ids = []
        for j, e in enumerate(d["events"]):
            if e["class"] == "other":
                continue
            cid = claim(f"{tk}.ev{j:02d}.{e['item_code'].replace(' ', '_')}",
                        f"{d['label']} filed {e['form']} on {e['filed']} with item {e['item_code']}"
                        + (f': "{e["quote"]}"' if e.get("quote") else f" (quote MISSING: {e.get('quote_gap')})"),
                        e.get("filing_url"), "measured", f"class={e['class']}")
            e["claim_id"] = cid
            ev_ids.append(cid)
        for e in d["events"]:
            ev_rows.append({k: e.get(k) for k in ("name", "cik", "form", "filed", "accession", "item_code", "class",
                                                  "hard_trigger", "filing_url", "quote", "quote_gap", "claim_id")})
        bid = claim(f"{tk}.bucket", f"{d['label']}: code bucket {res['bucket']} ({res['why']})", "", "inferred",
                    "rules in config.toml [buckets]")
        flag_list = []
        for fl, pts in res["flags"]:
            inputs, cids = [], []
            if fl.startswith("wall_share"):
                inputs = [("wall_2027_share", x["share"], cfg["filings_risk"]["wall_share_watch"]["value"],
                           cfg["filings_risk"]["wall_share_severe"]["value"])]
                cids = [ids.get("share"), ids["y2_2027"], "CFG.filings_risk.wall_share_watch"]
            elif fl == "year1_unresolved":
                inputs = [("y1_2026_share", x["y1_share"], cfg["filings_risk"]["year1_unresolved"]["value"])]
                cids = [ids.get("y1_share"), ids["y1_2026"], "CFG.filings_risk.year1_unresolved"]
            elif fl.startswith("rel_drawdown"):
                inputs = [("rel_drawdown", x["rel_dd"], cfg["market_view"]["rel_drawdown_watch"]["value"])]
                cids = [ids.get("rel"), ids["dd"], "CFG.market_view.rel_drawdown_watch"]
            elif fl == "scored_negative_events":
                inputs = [("scored_negative_items", len(x["scored_neg"]), None)]
                cids = [e.get("claim_id") for e in x["scored_neg"]]
            elif fl == "disagreement":
                inputs = [("filings_risk", res["filings_risk"], None), ("market_view", res["market_view"], None)]
                cids = [ids.get("share"), ids.get("rel")]
            elif fl == "market_data_gap":
                inputs = [("drawdown_52w", None, None)]
                cids = [ids["dd"]]
            flag_list.append({"flag": fl, "points": pts, "inputs": inputs, "claim_ids": [c for c in cids if c]})
        if res["refinancing_tag"]:
            flag_list.append({"flag": "refinancing_tag", "points": 0, "text": res["refinancing_tag"],
                              "inputs": [("debt_financing_items_2026", len(res["debt_financing"]), None)],
                              "claim_ids": [e.get("claim_id") for e in res["debt_financing"]]})
        # ---- latest 10-Q ladder and secured split: DISPLAY ONLY, they never enter score()
        q = d.get("qladder") or {"buckets": [], "gap_reason": "not extracted"}
        qv = {b_["label"]: b_["fact"]["value"] for b_ in q["buckets"]}
        q_present = [v for v in qv.values() if v is not None]
        q27_label = str(int(cfg["ladder_period_end"][:4]) + 2)
        q_confirmed = False
        q27 = qv.get(q27_label)
        q_total = sum(q_present) if q_present else None
        q_share = q27 / q_total if (q27 is not None and q_total) else None
        q_ub = q_share is not None and len(q_present) < len(qv)
        for b_ in q["buckets"]:
            f_ = b_["fact"]
            claim(f"{tk}.q_ladder_{b_['key']}", f"{d['label']} 10-Q ({q['period_end']}) {f_['tag_or_form']} [{b_['label']}] = "
                  + (f"${_musd(f_['value'])}M" if f_["value"] is not None else f"MISSING ({f_['gap_reason']})"), f_["source_url"], "measured",
                  f"accn {f_['accession']} filed {f_['filed']}; 10-Q labels mapped to calendar years (verify.py section 7)")
        # mapping is confirmed for this filer only if an overlapping year carries the same non-zero principal in 10-K and 10-Q
        kmap = {"2027": "y2_2027", "2028": "y3_2028", "2029": "y4_2029", "2030": "y5_2030"}
        q_confirmed = any(qv.get(yr) not in (None, 0) and d["ladder"][k]["value"] not in (None, 0) and abs(qv[yr] - d["ladder"][k]["value"]) < 1
                          for yr, k in kmap.items())
        # both shares must be exact (an upper bound cannot show a move) and the filer's 10-Q mapping must be confirmed
        qt = d.get("q10_text") or {}
        if qt.get("status") == "done" and qt.get("mapping_ok"):
            q_confirmed = True  # confirmed directly from the 10-Q row labels (verify.py section 8)
        if q_share is not None:
            claim(f"{tk}.q_wall_2027_share", f"{d['label']} latest 10-Q ({q['period_end']}): {q27_label} maturities are {q_share:.1%} of the 10-Q ladder"
                  + (" (UPPER BOUND, buckets missing)" if q_ub else "")
                  + ("; calendar year mapping confirmed (equal overlapping year, or 10-Q row labels)" if q_confirmed else "; calendar mapping UNCONFIRMED for this filer (no overlapping year matches the 10-K)"),
                  "", "inferred", "display only, never scored")
        moved = (q_confirmed and not q_ub and not x["share_is_ub"] and q_share is not None and x["share"] is not None
                 and abs(q_share - x["share"]) >= cfg["display_only"]["ladder_moved_pts"])
        if moved:
            flag_list.append({"flag": "ladder_moved_since_10k", "points": 0,
                              "inputs": [("wall_2027_share_10k", x["share"], None), ("wall_2027_share_10q", q_share, cfg["display_only"]["ladder_moved_pts"])],
                              "claim_ids": [ids.get("share"), f"{tk}.q_wall_2027_share"]})
        sec = d.get("secured") or {}
        sec_ok = sec.get("secured") is not None and not sec.get("stale") and sec["secured"] > 0 and sec["unsecured"] > 0
        if sec.get("secured") is not None and not sec_ok and not sec.get("stale"):
            sec["gap_reason"] = "one of SecuredDebt / UnsecuredDebt is tagged as 0, which conflicts with a mixed stack; not shown"
        sec_share = (sec["secured"] / (sec["secured"] + sec["unsecured"])) if sec_ok else None
        if sec.get("secured") is not None:
            claim(f"{tk}.secured_split", f"{d['label']} SecuredDebt ${_musd(sec['secured'])}M and UnsecuredDebt ${_musd(sec['unsecured'])}M at {sec['period_end']}"
                  + (f": {sec_share:.1%} secured" if sec_share is not None else f" (NOT SHOWN: {sec.get('gap_reason')})"),
                  sec["source_url"], "measured", f"accn {sec.get('accession')}; display only, never scored")
        ov = overrides.get(d["label"]) or overrides.get(tk) or {}
        if ov:
            claim(f"{tk}.override", f"HUMAN OVERRIDE for {d['label']}: {ov['bucket']}. {ov['reason']}", "overrides.csv",
                  ov.get("tag_type") or "inferred", f"evidence claim {ov.get('claim_id')}; quote: {ov.get('quote', '')[:200]}")
        flags_out[tk] = {"name": d["label"], "bucket": res["bucket"], "why": res["why"], "bucket_claim": bid,
                         "filings_risk": res["filings_risk"], "market_view": res["market_view"],
                         "disagreement": res["disagreement"], "flags": flag_list, "flip": flip,
                         "override": ov or None, "event_claims": ev_ids, "detail": d.get("price_detail")}
        lf = d["ladder"]
        row = {"name": d["label"], "ticker": tk, "cik": d["cik"], "segment": d["segment"],
               "ladder_period_end": cfg["ladder_period_end"]}
        for k, f in lf.items():
            row[f"ladder_{k}_musd"] = _musd(f["value"])
            row[f"ladder_{k}_gap"] = f["gap_reason"] or ""
        row.update({
            "ladder_accession": next((f["accession"] for f in lf.values() if f["accession"]), ""),
            "ladder_complete": x["complete"], "ladder_sum_musd": _musd(x["total"]),
            "wall_2027_musd": _musd(x["y2"]), "wall_2027_share": None if x["share"] is None else round(x["share"], 4),
            "wall_2027_share_is_upper_bound": x["share_is_ub"],
            "y1_2026_musd": _musd(x["y1"]), "y1_2026_share": None if x["y1_share"] is None else round(x["y1_share"], 4),
            "year1_question": ("2026 maturities: financing 8-K items seen (" + ", ".join(f"{e['item_code']} {e['filed']}" for e in x["financing"]) + "); NOT declared resolved")
                              if x["financing"] else "2026 maturities: no 1.01/2.03 8-K item in 2026; NOT declared resolved",
            "latest_cash_musd": _musd(d["cash"]["value"]), "latest_cash_period_end": d["cash"]["period_end"],
            "latest_cash_gap": d["cash"]["gap_reason"] or "",
            "latest_debt_musd": _musd(d["debt"]["value"]), "latest_debt_period_end": d["debt"]["period_end"],
            "latest_debt_gap": d["debt"]["gap_reason"] or "",
            "wall_to_cash_display_only": (round(x["y2"] / d["cash"]["value"], 1) if x["y2"] is not None and d["cash"]["value"] else None),
            "events_2026_filings": d["ev_counts"]["filings_2026"], "events_negative": d["ev_counts"]["negative"],
            "events_hard_trigger": d["ev_counts"]["hard_trigger"], "events_financing": d["ev_counts"]["financing"],
            "events_gap": d["ev_gap"] or "",
            "drawdown_52w": None if dd["value"] is None else round(dd["value"], 4), "price_as_of": dd["period_end"],
            "price_gap": dd["gap_reason"] or "",
            "sector_median_drawdown": None if d["rel"][1] is None else round(d["rel"][1], 4),
            "rel_drawdown": None if x["rel_dd"] is None else round(x["rel_dd"], 4),
            "return_6m_display_only": None if r6["value"] is None else round(r6["value"], 4),
            "filings_risk": res["filings_risk"], "market_view": res["market_view"],
            "bucket": res["bucket"], "bucket_why": res["why"],
            "override_bucket": ov.get("bucket", ""), "override_reason": ov.get("reason", ""), "override_claim_id": ov.get("claim_id", ""),
            "disagreement": res["disagreement"] or "", "refinancing_tag": res["refinancing_tag"] or "",
            "nearest_flip_threshold": flip["nearest"]["threshold"] if flip and flip["nearest"] else "",
            "nearest_flip_distance_pct": round(flip["nearest"]["distance_pct"] * 100, 1) if flip and flip["nearest"] else "",
            "bucket_claim_id": bid,
            "q_period_end": q.get("period_end") or "", "q_2027_musd": _musd(q27), "q_2027_share": None if q_share is None else round(q_share, 4),
            "q_2027_share_is_upper_bound": q_ub, "q_mapping_confirmed": q_confirmed if q["buckets"] else "", "q_gap": q.get("gap_reason") or "", "ladder_moved_since_10k": moved,
            "secured_musd": _musd(sec.get("secured")), "unsecured_musd": _musd(sec.get("unsecured")),
            "secured_share": None if sec_share is None else round(sec_share, 4), "secured_period_end": sec.get("period_end") or "",
            "secured_gap": sec.get("gap_reason") or "",
        })
        rows.append(row)

    order = {b: i for i, b in enumerate(["ACT NOW", "WATCH", "CAN'T CALL", "ROUTINE"])}
    ctl = cfg["pipeline_control"]["cik"]
    ranked = sorted([r for r in rows if not (cfg["case_files"]["exclude_pipeline_control"] and r["cik"] == ctl)],
                    key=lambda r: (order[r["bucket"]], not r["disagreement"], -(r["filings_risk"] + (r["market_view"] or 0)),
                                   -(r["wall_2027_share"] or 0)))
    case_files = [r["cik"] for r in ranked[: cfg["case_files"]["count"]]]
    for i, r in enumerate(ranked):
        r["priority_rank"] = i + 1
    for r in rows:
        r.setdefault("priority_rank", "pipeline test")
        r["case_file"] = r["cik"] in case_files
    with open(PROC / "metrics.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    with open(PROC / "events.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ev_rows[0]) if ev_rows else ["name"])
        w.writeheader(); w.writerows(ev_rows)
    with open(PROC / "flags.json", "w") as f:
        json.dump({"rates_context": rates, "case_files": case_files, "names": flags_out}, f, indent=1, default=str)
    write_claims(claims)
    return rows, flags_out, claims, case_files


def write_claims(claims):
    with open(ROOT / "claims.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["claim_id", "claim", "source_url", "tag_type", "checked", "note"])
        w.writeheader(); w.writerows(claims)
