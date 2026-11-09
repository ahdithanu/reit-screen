# Source list

From claims.csv. type: fact = measured or checked (read from a source); inference = inferred or assumed. checked: verified against filing text (yes/no).

| # | claim | claim_id | source | type | checked |
|---|---|---|---|---|---|
| 1 | SLG FY2025 10-K: 2027 maturities $2,569.3M | `SLG.ladder_y2_2027` | https://data.sec.gov/api/xbrl/companyfacts/CIK0001040971.json | fact | yes |
| 1 | SLG FY2025 10-K: 2027 maturities are 63.5% of the six-bucket ladder | `SLG.wall_2027_share` | derived, no direct URL (= SLG.ladder_y2_2027 / sum of ladder claims) | inference | no |
| 2 | SLG 10-Q filed 2026-11-05: consolidated 2027 maturities $1,157.4M (row in $ thousands: 1,157,413) | `SLG.10q_table_r2` | https://www.sec.gov/Archives/edgar/data/1040971/000162828026071014/slg-20260930.htm | fact | no |
| 3 | SLG facility amended and restated March 18, 2026: revolver to June 2030 (as-of-right extensions to June 2031), Term C $750M to June 2031, Term A $300M May 2027, Term B $100M November 2026 | `SLG.10q_2027_p0` | https://www.sec.gov/Archives/edgar/data/1040971/000162828026071014/slg-20260930.htm | fact | no |
| 4 | SLG filed no 8-K between 2026-03-10 and 2026-03-31 | `SLG.no_8k_in_window` | https://data.sec.gov/submissions/CIK0001040971.json | fact | yes |
| 5 | SLG column mapping between the 10-K and 10-Q tables (arithmetic ties; tagged inferred, human signed off 2026-11-09) | `SLG.mapping_check` | https://www.sec.gov/Archives/edgar/data/1040971/000162828026008669/slg-20251231.htm | inference | no |
| 6 | JBGS 2027 share 26.6% (computed as an upper bound: after-2030 bucket untagged) | `JBGS.wall_2027_share` | derived, no direct URL (= JBGS.ladder_y2_2027 / sum of ladder claims) | inference | no |
| 6 | JBGS 10-K printed total equals the tagged buckets, so the 26.6% upper bound is the table share | `JBGS.ub_equals_printed` | https://www.sec.gov/Archives/edgar/data/1689796/000110465926016450/jbgs-20251231x10k.htm | fact | yes |
| 6, 7 | JBGS 10-Q (2026-09-30): revolver ($690.0M) matures August 2030; $200.0M Tranche A-1 term loan matures January 2027 | `JBGS.10q_2027_p0` | https://www.sec.gov/Archives/edgar/data/1689796/000110465926123567/jbgs-20260930x10q.htm | fact | no |
| 8, 17 | JBGS stock closed 33.4% below its 52-week high (2026-11-06); prices are from the unofficial Yahoo chart API | `JBGS.drawdown_52w` | https://query1.finance.yahoo.com/v8/finance/chart/JBGS?range=1y&interval=1d | fact | no |
| 8 | JBGS drawdown is +19.6 points vs the office median (24-name peer group; was +20.4 with 12 names) | `JBGS.rel_drawdown` | derived, no direct URL (peers: KRC,BXP,SLG,PDM,DEI,HPP,ESRT,JBGS,CUZ,BDN,VNO,HIW) | inference | no |
| 9 | ESRT Series B senior unsecured notes $125.0M due 3/27/2027 (filing cell 125,000, $ thousands) | `ESRT.10q_debtrow0` | https://www.sec.gov/Archives/edgar/data/1541401/000154140126000033/esrt-20260630.htm | fact | no |
| 9 | ESRT 2027 share 6.7% of the FY2025 ladder | `ESRT.wall_2027_share` | derived, no direct URL (= ESRT.ladder_y2_2027 / sum of ladder claims) | inference | no |
| 10 | ESRT latest 10-Q is period 2026-06-30: no 10-Q for period 2026-09-30 on EDGAR at the run date | `ESRT.no_10q_2026-09-30` | https://data.sec.gov/submissions/CIK0001541401.json | fact | yes |
| 11 | CBL 57.6% of the FY2025 ladder was due in 2026 | `CBL.y1_2026_share` | derived, no direct URL (= CBL.ladder_y1_2026 / ladder sum) | inference | no |
| 11 | CBL mis-scaled 2027 tag caught by the scale check (printed total vs bucket sum) | `CBL.scale_mismatch` | https://www.sec.gov/Archives/edgar/data/910612/000119312526087049/cbl-20251231.htm | fact | yes |
| 12 | BXP has no tagged FY2025 ladder, so it is CAN'T CALL | `BXP.bucket` | derived, no direct URL (rules in config.toml [buckets]) | inference | no |
| 13 | OPI is a pipeline test, not a finding: the 8-K filed 2026-06-23 reports the Chapter 11 plan Effective Date (human override, signed off 2026-11-09) | `OPI.override` | overrides.csv | inference | no |
| 14 | Cross-extraction: 192 value pairs, 0 differences; one resolved period-selection artifact (Tanger / LongTermDebt) and its fix | `XCHK.cross_extraction` | https://data.sec.gov/api/xbrl/frames/us-gaap/LongTermDebt/USD/CY2025Q4I.json | fact | no |
| 15 | Bucket thresholds are assumptions in config.toml (e.g. 30% 2027 share = watch) | `CFG.filings_risk.wall_share_watch` | config.toml | inference | no |
| 16 | Decision-maker persona is an assumption, not validated by a practitioner | `CFG.persona` | config.toml | inference | no |
| 18 | 4 of 504 claims human reviewed (signoff.csv rows whose claim_id is in the ledger) | `REVIEW.signoff_count` | signoff.csv | fact | no |

## UNSOURCED (no claim_id in claims.csv; no line written)

- none

## Merged or dropped to fit 22 lines

- items 6 and 7 share one 10-Q claim (JBGS.10q_2027_p0)
- items 8 and 17 share one price claim (JBGS.drawdown_52w)
- dropped to stay at 22: the JBGS 8-K line (JBGS.ev02.1.01, the quote does not state the 2030 date) and the separate OPI 8-K line (OPI.ev10.1.03, cited inside OPI.override)
