"""Builds source_list.csv and source_list.md from claims.csv. Every line cites an existing claim_id;
the claim wording is the memo's, corrected where the ledger says otherwise. Nothing is invented."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = {c["claim_id"]: c for c in csv.DictReader(open(ROOT / "claims.csv", newline=""))}
TYPE = {"measured": "fact", "checked": "fact", "inferred": "inference", "assumed": "inference"}

LINES = [  # (memo item, claim wording, claim_id) -- max 22 lines
    (1, "SLG FY2025 10-K: 2027 maturities $2,569.3M", "SLG.ladder_y2_2027"),
    (1, "SLG FY2025 10-K: 2027 maturities are 63.5% of the six-bucket ladder", "SLG.wall_2027_share"),
    (2, "SLG 10-Q filed 2026-11-05: consolidated 2027 maturities $1,157.4M (row in $ thousands: 1,157,413)", "SLG.10q_table_r2"),
    (3, "SLG facility amended and restated March 18, 2026: revolver to June 2030 (as-of-right extensions to June 2031), Term C $750M to June 2031, Term A $300M May 2027, Term B $100M November 2026", "SLG.10q_2027_p0"),
    (4, "SLG filed no 8-K between 2026-03-10 and 2026-03-31", "SLG.no_8k_in_window"),
    (5, "SLG column mapping between the 10-K and 10-Q tables (arithmetic ties; tagged inferred, human signed off 2026-11-09)", "SLG.mapping_check"),
    (6, "JBGS 2027 share 26.6% (computed as an upper bound: after-2030 bucket untagged)", "JBGS.wall_2027_share"),
    (6, "JBGS 10-K printed total equals the tagged buckets, so the 26.6% upper bound is the table share", "JBGS.ub_equals_printed"),
    ("6, 7", "JBGS 10-Q (2026-09-30): revolver ($690.0M) matures August 2030; $200.0M Tranche A-1 term loan matures January 2027", "JBGS.10q_2027_p0"),
    ("8, 17", "JBGS stock closed 33.4% below its 52-week high (2026-11-06); prices are from the unofficial Yahoo chart API", "JBGS.drawdown_52w"),
    (8, "JBGS drawdown is +19.6 points vs the office median (24-name peer group; was +20.4 with 12 names)", "JBGS.rel_drawdown"),
    (9, "ESRT Series B senior unsecured notes $125.0M due 3/27/2027 (filing cell 125,000, $ thousands)", "ESRT.10q_debtrow0"),
    (9, "ESRT 2027 share 6.7% of the FY2025 ladder", "ESRT.wall_2027_share"),
    (10, "ESRT latest 10-Q is period 2026-06-30: no 10-Q for period 2026-09-30 on EDGAR at the run date", "ESRT.no_10q_2026-09-30"),
    (11, "CBL 57.6% of the FY2025 ladder was due in 2026", "CBL.y1_2026_share"),
    (11, "CBL mis-scaled 2027 tag caught by the scale check (printed total vs bucket sum)", "CBL.scale_mismatch"),
    (12, "BXP has no tagged FY2025 ladder, so it is CAN'T CALL", "BXP.bucket"),
    (13, "OPI is a pipeline test, not a finding: the 8-K filed 2026-06-23 reports the Chapter 11 plan Effective Date (human override, signed off 2026-11-09)", "OPI.override"),
    (14, "Cross-extraction: 192 value pairs, 0 differences; one resolved period-selection artifact (Tanger / LongTermDebt) and its fix", "XCHK.cross_extraction"),
    (15, "Bucket thresholds are assumptions in config.toml (e.g. 30% 2027 share = watch)", "CFG.filings_risk.wall_share_watch"),
    (16, "Decision-maker persona is an assumption, not validated by a practitioner", "CFG.persona"),
    (18, "Human review: counted from signoff.csv against the ledger", "REVIEW.signoff_count"),
]
UNSOURCED = []
MERGED = ["items 6 and 7 share one 10-Q claim (JBGS.10q_2027_p0)", "items 8 and 17 share one price claim (JBGS.drawdown_52w)",
          "dropped to stay at 22: the JBGS 8-K line (JBGS.ev02.1.01, the quote does not state the 2030 date) and the separate OPI 8-K line (OPI.ev10.1.03, cited inside OPI.override)"]

rows = []
for item, text, cid in LINES:
    c = C[cid]  # KeyError here means the claim_id does not exist: fail loudly
    src = c["source_url"] or f"derived, no direct URL ({c['note']})"
    if cid == "REVIEW.signoff_count":
        text = c["claim"]  # the count itself, as measured this run
    rows.append({"item": item, "claim": text, "claim_id": cid, "source_url": src, "type": TYPE[c["tag_type"]], "checked": c["checked"]})
assert len(rows) <= 22
with open(ROOT / "source_list.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["claim", "claim_id", "source_url", "type", "checked"])
    w.writeheader()
    w.writerows({k: r[k] for k in ("claim", "claim_id", "source_url", "type", "checked")} for r in rows)
md = ["# Source list", "", "From claims.csv. type: fact = measured or checked (read from a source); inference = inferred or assumed. "
      "checked: verified against filing text (yes/no).", "", "| # | claim | claim_id | source | type | checked |", "|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['item']} | {r['claim']} | `{r['claim_id']}` | {r['source_url']} | {r['type']} | {r['checked']} |")
md += ["", "## UNSOURCED (no claim_id in claims.csv; no line written)", ""] + ([f"- {i}. {t}: {why}" for i, t, why in UNSOURCED] or ["- none"])
md += ["", "## Merged or dropped to fit 22 lines", ""] + [f"- {m}" for m in MERGED]
(ROOT / "source_list.md").write_text("\n".join(md) + "\n")
for name in ("source_list.csv", "source_list.md"):  # site copy
    (ROOT / "public" / "data").mkdir(parents=True, exist_ok=True)
    (ROOT / "public" / "data" / name).write_text((ROOT / name).read_text())
n_fact = sum(1 for r in rows if r["type"] == "fact")
print(f"lines: {len(rows)} | fact: {n_fact} | inference: {len(rows) - n_fact} | checked=yes: {sum(1 for r in rows if r['checked'] == 'yes')}")
