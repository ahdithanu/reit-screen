"""Builds source_list.csv and source_list.md from claims.csv. Every line cites an existing claim_id;
the claim wording is the memo's, corrected where the ledger says otherwise. Nothing is invented."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = {c["claim_id"]: c for c in csv.DictReader(open(ROOT / "claims.csv", newline=""))}
TYPE = {"measured": "fact", "checked": "fact", "inferred": "inference", "assumed": "inference"}

LINES = [  # (claim wording, claim_id) -- max 22 lines, numbered 1..N in order
    ("SLG FY2025 10-K: 2027 maturities $2,569.3M", "SLG.ladder_y2_2027"),
    ("SLG FY2025 10-K: 2027 maturities are 63.5% of the six-bucket ladder", "SLG.wall_2027_share"),
    ("SLG 10-Q filed 2026-11-05: consolidated 2027 maturities $1,157.4M (row in $ thousands: 1,157,413)", "SLG.10q_table_r2"),
    ("SLG facility amended and restated March 18, 2026: revolver to June 2030 (as-of-right extensions to June 2031), Term C $750M to June 2031, Term A $300M May 2027, Term B $100M November 2026", "SLG.10q_2027_p0"),
    ("SLG filed no 8-K between 2026-03-10 and 2026-03-31", "SLG.no_8k_in_window"),
    ("SLG column mapping between the 10-K and 10-Q tables (arithmetic ties; tagged inferred, human signed off 2026-11-09)", "SLG.mapping_check"),
    ("SLG stock closed 15.1% below its 52-week high, +1.3 points vs the office median of 13.8% (12 office peers); prices are from the unofficial Yahoo chart API", "SLG.rel_drawdown"),
    ("JBGS 10-Q (2026-09-30): revolver ($690.0M) matures August 2030; $200.0M Tranche A-1 term loan matures January 2027", "JBGS.10q_2027_p0"),
    ("JBGS stock closed 33.4% below its 52-week high (2026-11-06); prices are from the unofficial Yahoo chart API", "JBGS.drawdown_52w"),
    ("ESRT Series B senior unsecured notes $125.0M due 3/27/2027 (filing cell 125,000, $ thousands)", "ESRT.10q_debtrow0"),
    ("ESRT latest 10-Q is period 2026-06-30: no 10-Q for period 2026-09-30 on EDGAR at the run date", "ESRT.no_10q_2026-09-30"),
    ("CBL 57.6% of the FY2025 ladder was due in 2026", "CBL.y1_2026_share"),
    ("CBL 10-Q for the period ended 2026-06-30: $180.3M of principal due in the rest of 2026 (H2 2026)", "CBL.q_ladder_rest"),
    ("CBL mis-scaled 2027 tag caught by the scale check (printed total vs bucket sum)", "CBL.scale_mismatch"),
    ("BXP has no tagged FY2025 ladder, so it is CAN'T CALL", "BXP.bucket"),
    ("OPI is a pipeline test, not a finding: the 8-K filed 2026-06-23 reports the Chapter 11 plan Effective Date (human override, signed off 2026-11-09)", "OPI.override"),
    ("Cross-extraction: 192 value pairs, 0 differences; one resolved period-selection artifact (Tanger / LongTermDebt) and its fix", "XCHK.cross_extraction"),
    (None, "VERIFY.ladders_10k_checked"),
    (None, "RUN.bucket_counts"),
    ("Bucket thresholds are assumptions in config.toml (e.g. 30% 2027 share = watch)", "CFG.filings_risk.wall_share_watch"),
    ("Decision-maker persona is an assumption, not validated by a practitioner", "CFG.persona"),
    (None, "REVIEW.signoff_count"),
]
SITE = "https://reit-screen.vercel.app/data/"
WHERE = {"config.toml": SITE + "config.toml", "overrides.csv": SITE + "overrides.csv", "signoff.csv": SITE + "signoff.csv",
         "verification.md": SITE + "verification.md", "metrics.csv": SITE + "metrics.csv"}
SOURCE_OVERRIDE = {  # source list shows the filing; the ledger keeps the human decision file
    "OPI.override": (C["OPI.ev10.1.03"]["source_url"], "decision recorded in overrides.csv: " + WHERE["overrides.csv"]),
}
INTERNAL = ["## UNSOURCED (no claim_id in claims.csv; no line written)", "", "- none", "",
            "## Merged or dropped", "",
            "- removed on review: JBGS.wall_2027_share, JBGS.ub_equals_printed, ESRT.wall_2027_share, JBGS.rel_drawdown",
            "- JBGS 10-Q and price claims each cover two memo items (JBGS.10q_2027_p0, JBGS.drawdown_52w)",
            "- not listed: the JBGS 8-K line (JBGS.ev02.1.01, the quote does not state the 2030 date) and the separate OPI 8-K line (OPI.ev10.1.03, now the source of OPI.override)"]

rows = []
for n, (text, cid) in enumerate(LINES, 1):
    c = C[cid]  # KeyError here means the claim_id does not exist: fail loudly
    if cid in SOURCE_OVERRIDE:
        url, extra = SOURCE_OVERRIDE[cid]
        src = f"{url} ({extra})"
    elif c["source_url"] in WHERE:
        src = f"{c['source_url']} ({WHERE[c['source_url']]})"
    else:
        src = c["source_url"] or f"derived, no direct URL ({c['note']})"
    if text is None:
        text = c["claim"]  # counts as measured this run, straight from the ledger
    rows.append({"item": n, "claim": text, "claim_id": cid, "source": src, "type": TYPE[c["tag_type"]], "checked": c["checked"]})
assert len(rows) <= 22
with open(ROOT / "source_list.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["claim", "claim_id", "source", "type", "checked"])
    w.writeheader()
    w.writerows({k: r[k] for k in ("claim", "claim_id", "source", "type", "checked")} for r in rows)
md = ["# Source list", "", "From claims.csv. type: fact = measured or checked (read from a source); inference = inferred or assumed. "
      "checked: verified against filing text (yes/no).", "", "| # | claim | claim_id | source | type | checked |", "|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['item']} | {r['claim']} | `{r['claim_id']}` | {r['source']} | {r['type']} | {r['checked']} |")
assert [r["item"] for r in rows] == list(range(1, len(rows) + 1))
(ROOT / "internal_notes.md").write_text("# Source list: internal notes (not published)\n\n" + "\n".join(INTERNAL) + "\n")
(ROOT / "source_list.md").write_text("\n".join(md) + "\n")
for name in ("source_list.csv", "source_list.md"):  # site copy
    (ROOT / "public" / "data").mkdir(parents=True, exist_ok=True)
    (ROOT / "public" / "data" / name).write_text((ROOT / name).read_text())
n_fact = sum(1 for r in rows if r["type"] == "fact")
print(f"lines: {len(rows)} | fact: {n_fact} | inference: {len(rows) - n_fact} | checked=yes: {sum(1 for r in rows if r['checked'] == 'yes')}")
