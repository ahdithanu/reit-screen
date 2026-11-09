"""Private-data overlay. Joins a lender's own file (here a SYNTHETIC example) to the public screen, LOCALLY.

No network, no model. It can only escalate a bucket, and it writes overlay_bucket next to the code bucket.
"""
import csv
import datetime as dt

from common import PROC, ROOT

UP = {"ROUTINE": "WATCH", "WATCH": "ACT NOW"}


def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month) + (b.day - a.day) / 31


def run(cfg, rows):
    oc = cfg["overlay"]
    path = ROOT / oc["file"]
    if not path.exists():
        return []
    asof = dt.date.fromisoformat(cfg["as_of"])
    private = {r["ticker"]: r for r in csv.DictReader(open(path, newline=""))}
    out = []
    for r in rows:
        p = private.get(r["ticker"])
        if not p:
            continue
        reasons = []
        head = float(p["covenant_headroom_pct"])
        if head < oc["covenant_headroom_min_pct"]:
            reasons.append(f"covenant headroom {head:.1f}% < {oc['covenant_headroom_min_pct']:.0f}%")
        mat = dt.date.fromisoformat(p["own_facility_maturity"])
        m = months_between(asof, mat)
        if m <= oc["own_facility_months"]:
            reasons.append(f"own facility matures {mat} ({m:.1f} months after as_of, within {oc['own_facility_months']})")
        new = UP.get(r["bucket"], r["bucket"]) if reasons else r["bucket"]
        out.append({"name": r["name"], "ticker": r["ticker"], "code_bucket": r["bucket"], "overlay_bucket": new,
                    "flipped": new != r["bucket"], "reasons": "; ".join(reasons) or "no overlay trigger",
                    "internal_rating": p["internal_rating"], "covenant_headroom_pct": head,
                    "undrawn_revolver_musd": p["undrawn_revolver_musd"], "own_facility_maturity": p["own_facility_maturity"],
                    "data_label": "SYNTHETIC"})
    with open(PROC / "overlay_result.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]) if out else ["name"])
        w.writeheader(); w.writerows(out)
    return out
