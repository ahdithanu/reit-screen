# Summary: what is solid, what is unchecked, what could not be verified

Run as of 2026-11-09, 24 listed office and retail REITs, public data only (SEC EDGAR, FRED, Yahoo). The tool screens borrowers into ACT NOW, WATCH, CAN'T CALL and ROUTINE for a credit officer holding participations in their syndicated unsecured loans. That decision-maker is an assumption, and no practitioner has validated it.

## The answer
- No live borrower is ACT NOW. OPI sits there as the pipeline test: it must land in ACT NOW, and it does. Its 2026 bankruptcy filings trigger the rule even though it has since emerged.
- **SL Green is the one name where filings and market disagree.** Its FY2025 10-K shows $2.57B (63.5% of its debt) due in 2027, yet the stock trades in line with office peers. The latest 10-Q explains it: a credit facility amended on March 18, 2026 cut consolidated 2027 maturities to $1.16B. What's left is mostly property mortgages and a $300M term loan due May 2027. SLG's share of joint-venture debt due in 2027 is $2.35B, outside the consolidated figure. SLG filed no 8-K for the amendment; it appears in an earnings-release exhibit.
- WATCH: SLG, JBGS, ESRT, CBL. CAN'T CALL: BXP, VNO, DEI, HPP, KIM, MAC, SKT (no usable maturity tags). The other 12 are ROUTINE.

## Solid (checked by code against a second source or the filing text)
- **Pipeline control** passes: OPI is ACT NOW from item 1.03 and NT 10-Q filings.
- **Two SEC extractions agree.** Companyfacts against SEC frames: 192 value pairs, 0 differences. One earlier difference (Tanger LongTermDebt) was a period-selection artifact, now fixed and documented.
- **10-K ladders against the 10-K text:** 17 of 17 tagged ladders checked. 98 of 102 cells match; the other 4 are buckets the filer left untagged. 12 printed table totals equal the bucket sums, and a CBL 2027 tag at the wrong scale was caught this way. The value is kept as filed.
- **SLG's 10-Q ladder** checked cell by cell against the 10-Q text, with the calendar-year mapping confirmed from the row labels.
- **Every 8-K quote** in the case files was downloaded again and matched word for word.
- **Re-runs offline** from the cached responses with zero network calls (see README).
- **3 of 505 claims human reviewed** (signoff.csv): the SLG and OPI overrides, and the SLG table-column mapping. CBL has no override; it stays at its code bucket, WATCH.

## Unchecked (extracted but not verified against filing text, or not reviewed by a human)
- **10-Q ladders:** 6 of 7 not checked against the 10-Q text (ESRT, CBL, BRX, AKR, BDN, REG). They are display only and never scored.
- **Verbatim filing passages:** the 10-Q passages and dated 10-K sentences used in the case files were extracted by code and read by the AI. No human has signed them off.
- **Most of the ledger:** 502 of 505 claims are machine-extracted or machine-checked only.
- **Prices** come from the unofficial Yahoo chart API and are not checked against a second price source.

## Could not be verified, and why
- **Interest coverage:** InterestExpense is not tagged consistently across these filers, so no coverage ratio is computed.
- **Undrawn revolver capacity:** not tagged, so liquidity from cash alone understates the picture.
- **Seven names' ladders:** VNO, MAC and SKT do not file the standard maturity tags; BXP, HPP and KIM file none for FY2025; DEI uses rolling-window tags, which are not a dated ladder. All seven are CAN'T CALL.
- **Secured versus unsecured debt:** only 4 names tag both at a recent date, so the ladder cannot separate property mortgages from the unsecured facility a participant holds.
- **Extension options** are not visible in the tags.
- **Latest quarter:** ESRT and CBL had not filed Q3 2026 10-Qs at the run date.
- **Thresholds and persona:** all assumptions (config.toml), not calibrated against default history.

Full raw diffs: `verification.md`. Where the AI was wrong and how it was caught: `ai_log.md`. Key claims with sources: `source_list.md`.
