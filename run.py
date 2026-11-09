"""Orchestrator. python run.py [--offline] [--cached] [--names subset|all]

--offline : read only data/raw/ (newest cached copy); any missing file is a recorded gap
--cached  : online, but reuse a cached copy when one exists (avoids re-hitting SEC while developing)
--names   : 'subset' = config checkpoint_subset (step 2), 'all' = the 12 names
"""
import argparse
import sys

import event_reader
import ladder_extract
import market_context
import overlay
import synthesize
import verify
from common import load_config
from filings_fetch import Fetcher


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--cached", action="store_true")
    ap.add_argument("--names", choices=["subset", "all"], default="all")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--as-of", default=None, help="YYYY-MM-DD or 'today' (UTC); default is as_of in config.toml")
    a = ap.parse_args()
    cfg = load_config()
    if a.as_of:
        import datetime as _dt
        cfg["as_of"] = _dt.datetime.now(_dt.timezone.utc).date().isoformat() if a.as_of == "today" else _dt.date.fromisoformat(a.as_of).isoformat()
    fx = Fetcher(cfg, offline=a.offline, prefer_cache=a.cached)
    allnames = cfg["names"]
    selected = cfg["checkpoint_subset"] if a.names == "subset" else list(allnames)

    # Submissions + prices for ALL 12: tickers and the sector peer median need the full peer group.
    subs, ticker, ya, price = {}, {}, {}, {}
    for cik in allnames:
        subs[cik] = fx.submissions(cik)
        ts = event_reader.tickers(subs[cik]["path"])
        ticker[cik] = ts[0] if ts else None
        ya[cik] = fx.yahoo(ticker[cik]) if ticker[cik] else {"path": None, "error": "no ticker"}
        price[cik] = market_context.price_metrics(allnames[cik]["label"], cik, ticker[cik], ya[cik]["path"], cfg)
    segments = {c: allnames[c]["segment"] for c in allnames}
    rel = market_context.relative_drawdowns({c: price[c][0]["drawdown_52w"]["value"] for c in allnames}, segments)
    rel = {c: (r, m, [ticker[p] or p for p in peers]) for c, (r, m, peers) in rel.items()}
    rates = market_context.rates_line(fx.fred("DGS10")["path"], fx.fred("SOFR")["path"], cfg)

    names, conflicts, cf_paths = [], [], {}
    for cik in selected:
        label = allnames[cik]["label"]
        cf = fx.companyfacts(cik)
        cf_paths[cik] = cf["path"]
        facts, conf, ladder, cash, debt = ladder_extract.extract(cik, label, cfg, cf["path"])
        conflicts += conf
        events, ev_gap = event_reader.list_events(cik, label, cfg, subs[cik]["path"])
        for e in events:
            if event_reader.needs_document(e):
                doc = fx.archive(cik, e["accession"], e["primary_doc"])
                e["doc_path"] = doc["path"]
                e["quote"], e["quote_gap"] = event_reader.extract_quote(e, doc["path"], cfg["events"]["quote_chars"])
                if doc["error"]:
                    e["quote_gap"] = f"fetch failed: {doc['error']}"
        (pm, detail) = price[cik]
        names.append({"cik": cik, "label": label, "segment": allnames[cik]["segment"], "ticker": ticker[cik],
                      "ladder": ladder, "cash": cash, "debt": debt, "events": events,
                      "ev_counts": event_reader.counts(events), "ev_gap": ev_gap,
                      "drawdown": pm["drawdown_52w"], "return_6m": pm["return_6m"], "rel": rel[cik],
                      "price_detail": detail, "sub_path": subs[cik]["path"]})

    rows, flags, claims, case_files = synthesize.run(names, cfg, rates)
    # case-file evidence: verbatim 10-Q paragraphs on 2027 debt, and dated 2027 maturities from the 10-K text
    import json as _json
    from common import PROC
    evidence = {}
    for d in [n for n in names if n["cik"] in case_files]:
        tk, ev = d["ticker"], {}
        q = event_reader.latest_form(d["sub_path"], "10-Q")
        if q:
            r = fx.archive(d["cik"], q["accession"], q["doc"])
            ev["tenq"] = {**q, "url": r["url"], "error": r["error"],
                          "paragraphs": event_reader.paragraphs_2027(r["path"]) if r["path"] else []}
            if r["path"]:
                ev["tenq"]["maturity_table"], ev["tenq"]["maturity_table_gap"] = event_reader.maturity_table_rows(r["path"])
                ev["tenq"]["debt_rows_2027"] = event_reader.debt_rows_2027(r["path"])
                for i, row in enumerate(ev["tenq"]["debt_rows_2027"]):
                    claims.append({"claim_id": f"{tk}.10q_debtrow{i}", "claim": row, "source_url": r["url"], "tag_type": "measured",
                                   "checked": "no", "note": f"verbatim debt-table row mentioning 2027, 10-Q filed {q['filed']} ($ thousands)"})
                for i, row in enumerate(ev["tenq"]["maturity_table"] or []):
                    claims.append({"claim_id": f"{tk}.10q_table_r{i}", "claim": row, "source_url": r["url"], "tag_type": "measured",
                                   "checked": "no", "note": f"verbatim row of the maturity table in 10-Q filed {q['filed']} (in thousands)"})
            for i, para in enumerate(ev["tenq"]["paragraphs"]):
                claims.append({"claim_id": f"{tk}.10q_2027_p{i}", "claim": para, "source_url": r["url"], "tag_type": "measured",
                               "checked": "no", "note": f"verbatim block from 10-Q filed {q['filed']} (period {q['period']})"})
        acc = next((f["accession"] for f in d["ladder"].values() if f["accession"]), None)
        k = event_reader.latest_form(d["sub_path"], "10-K")
        if k and acc and k["accession"] == acc:
            r = fx.archive(d["cik"], acc, k["doc"])
            ev["tenk"] = {**k, "url": r["url"], "error": r["error"],
                          "dates": event_reader.maturity_dates_2027(r["path"]) if r["path"] else []}
            for i, x in enumerate(ev["tenk"]["dates"]):
                claims.append({"claim_id": f"{tk}.10k_2027_date{i}", "claim": f"{x['date']}: {x['sentence']}", "source_url": r["url"],
                               "tag_type": "measured", "checked": "no", "note": "verbatim sentence from FY2025 10-K"})
        else:
            ev["tenk"] = {"error": "latest 10-K accession differs from ladder accession or not found"}
        evidence[tk] = ev
    (PROC / "case_evidence.json").write_text(_json.dumps(evidence, indent=1))
    ovl = overlay.run(cfg, rows)
    for o in ovl:
        claims.append({"claim_id": f"OVL.{o['ticker']}", "claim": f"SYNTHETIC overlay: {o['code_bucket']} -> {o['overlay_bucket']} ({o['reasons']})",
                       "source_url": "private_overlay_example.csv", "tag_type": "assumed", "checked": "no", "note": "synthetic data, local only"})
    for k, v in rates.items():
        if isinstance(v, dict) and "value" in v:
            claims.append({"claim_id": f"RATES.{k}", "claim": f"{k.upper()} = {v['value']:.2f}% on {v['date']}"
                           + (f"; 12-month change {v['change_12m']:+.2f} pts (vs {v['prior_date']})" if v.get("change_12m") is not None else ""),
                           "source_url": f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={'DGS10' if k == 'dgs10' else 'SOFR'}",
                           "tag_type": "measured", "checked": "no", "note": "context only, never scored"})
    synthesize.write_claims(claims)
    print(f"\n{'name':34} {'tkr':6} {'bucket':11} F  M   2027 share     rel dd   flags")
    for r in rows:
        tk = r["ticker"]
        sh = "gap" if r["wall_2027_share"] is None else f"{r['wall_2027_share']:.1%}{' (UB)' if r['wall_2027_share_is_upper_bound'] else ''}"
        rd = "gap" if r["rel_drawdown"] is None else f"{r['rel_drawdown']*100:+.1f}pt"
        fl = ", ".join(f["flag"] for f in flags[tk]["flags"])
        print(f"{r['name'][:34]:34} {tk:6} {r['bucket']:11} {r['filings_risk']}  {r['market_view'] if r['market_view'] is not None else '-'}   {sh:14} {rd:8} {fl}")
    if not a.no_verify:
        ok = verify.run(fx, cfg, names, flags, conflicts, cf_paths, subs, claims, case_files, offline=a.offline)
        if not ok:
            sys.exit("CONTROL FAILED: OPI is not ACT NOW. Fix the pipeline before anything else.")
    import build_site
    build_site.build_site(cfg)
    print(f"\nreport.html written. network calls this run: {fx.network_calls}")


if __name__ == "__main__":
    main()
