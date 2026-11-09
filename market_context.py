"""Skill 4: market_context. Price drawdowns and the rates context line.

Never gives a valuation view. Rates never feed a score or bucket. A missing price is a gap.
"""
import csv
import datetime as dt
import json
import statistics

from common import fact, fetched_at_of


def yahoo_url(t):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1y&interval=1d"


def price_metrics(label, cik, ticker, path, cfg):
    url = yahoo_url(ticker) if ticker else None
    base = dict(name=label, cik=str(cik), unit="ratio", source_url=url, tag_or_form="Yahoo chart close (unofficial)",
                fetched_at=fetched_at_of(path))
    def gap(reason):
        return {m: fact(**base, metric=m, gap_reason=reason) for m in ("drawdown_52w", "return_6m")}, None
    if not ticker:
        return gap("no ticker in SEC submissions")
    if path is None:
        return gap("Yahoo fetch failed (see data/raw/manifest.csv)")
    try:
        res = json.loads(open(path, "rb").read())["chart"]["result"][0]
        ts = res["timestamp"]
        closes = res["indicators"]["quote"][0]["close"]
    except Exception as e:  # unofficial API: any shape change is a gap, not a crash
        return gap(f"Yahoo response not parseable: {type(e).__name__}")
    series = [(dt.datetime.fromtimestamp(t, dt.timezone.utc).date(), c) for t, c in zip(ts, closes) if c is not None]
    dropped = len(ts) - len(series)
    if len(series) < 20:
        return gap(f"only {len(series)} closes returned")
    last_d, last_c = series[-1]
    hi_d, hi_c = max(series, key=lambda x: x[1])
    dd = 1 - last_c / hi_c
    note = f"{len(series)} closes {series[0][0]}..{last_d}; {dropped} null closes skipped (not filled)"
    coverage = (last_d - series[0][0]).days
    if coverage < cfg["market"]["min_coverage_days"]:
        out = {"drawdown_52w": fact(**base, metric="drawdown_52w", period_end=str(last_d),
                                    gap_reason=f"partial window: {len(series)} closes since {series[0][0]} ({coverage} days); "
                                               f"52-week drawdown not computable. Since-first-close drawdown {dd:.1%} shown as context only")}
    else:
        out = {"drawdown_52w": fact(**base, metric="drawdown_52w", value=dd, period_end=str(last_d), gap_reason=None)}
    target = last_d - dt.timedelta(days=cfg["market"]["return_window_days"])
    before = [x for x in series if x[0] <= target]
    if before:
        b_d, b_c = before[-1]
        out["return_6m"] = fact(**base, metric="return_6m", value=last_c / b_c - 1, period_end=str(last_d))
        r6 = {"from_date": str(b_d), "from_close": b_c}
    else:
        out["return_6m"] = fact(**base, metric="return_6m", gap_reason=f"no close on or before {target}")
        r6 = {}
    detail = {"ticker": ticker, "last_date": str(last_d), "last_close": last_c, "high_date": str(hi_d),
              "high_close": hi_c, "note": note, "series": [(str(d), c) for d, c in series], **r6}
    return out, detail


def relative_drawdowns(rows, segments):
    """rows: {cik: drawdown or None}. Returns {cik: (rel, median, peers)}. Excludes missing names from the median."""
    out = {}
    for cik, dd in rows.items():
        seg = segments[cik]
        peers = {c: v for c, v in rows.items() if segments[c] == seg and v is not None}
        if dd is None or not peers:
            out[cik] = (None, None, sorted(peers))
            continue
        med = statistics.median(peers.values())
        out[cik] = (dd - med, med, sorted(peers))
    return out


def fred_series(path):
    if path is None:
        return None
    rows = []
    with open(path, newline="") as f:
        rd = csv.reader(f)
        next(rd)
        for r in rd:
            if len(r) < 2 or r[1] in (".", ""):
                continue  # FRED marks holidays/missing with "."; skipped, not filled
            rows.append((dt.date.fromisoformat(r[0]), float(r[1])))
    return rows


def rates_line(dgs10_path, sofr_path, cfg):
    out = {"use_in_scoring": False}
    d = fred_series(dgs10_path)
    if d:
        last_d, last_v = d[-1]
        tgt = last_d - dt.timedelta(days=cfg["market"]["rates_change_days"])
        prior = [x for x in d if x[0] <= tgt]
        out["dgs10"] = {"value": last_v, "date": str(last_d), "fetched_at": fetched_at_of(dgs10_path),
                        "change_12m": (last_v - prior[-1][1]) if prior else None,
                        "prior_date": str(prior[-1][0]) if prior else None}
    else:
        out["dgs10"] = {"gap_reason": "FRED DGS10 fetch failed"}
    s = fred_series(sofr_path)
    out["sofr"] = {"value": s[-1][1], "date": str(s[-1][0]), "fetched_at": fetched_at_of(sofr_path)} if s else {"gap_reason": "FRED SOFR fetch failed"}
    return out
