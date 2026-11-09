# REIT borrower screen for syndicate lenders

Live dashboard: deployed from `public/` on Vercel. A GitHub Actions job (`.github/workflows/refresh.yml`) re-runs the pipeline every weekday after the US close, proves it re-runs offline with zero network calls, and commits the refreshed outputs; Vercel redeploys on each push. The job fails, and nothing is deployed, if the OPI pipeline control fails.

What a regional-bank participant in listed office and retail REIT credit facilities cannot see, built only from public data (SEC EDGAR XBRL and filings, FRED, Yahoo prices). It is deterministic Python with no LLM calls in the data path. Every number carries its provenance.

## Run

Python 3.11+ (needs `tomllib`), plus `requests` and `pandas`.

```bash
export SEC_USER_AGENT="Your Name your.email@example.com"
```

```bash
python run.py --names all
```

Daily refresh, as the scheduled job runs it:

```bash
python run.py --names all --as-of today
```

Re-run from the cache with no network:

```bash
python run.py --offline --names all
```

Other flags:
- `--cached`: online, but reuses cached files.
- `--names subset`: OPI, SLG and CBL only (the step-2 checkpoint).
- `--no-verify`: skips verification.

The run stops with an error if the OPI pipeline control does not land in ACT NOW.

## Outputs
| file | what |
|---|---|
| `report.html`, `public/index.html` | the dashboard (one self-contained page, no external requests; `public/` is what Vercel serves, with `public/data/` holding the CSVs and verification.md) |
| `design/template.html` | the page design; `report.py` fills its data block. `design/build_template.py` rebuilds it from the reviewed design |
| `data/processed/metrics.csv` | one row per name: every metric, period end, gap reason, code bucket, override, flip test |
| `claims.csv` | `claim_id, claim, source_url, tag_type, checked, note`; every number in the report cites one |
| `verification.md` | control, companyfacts vs frames diffs, 10-K table spot checks, control totals, quote re-checks, conflicts and gaps |
| `ai_log.md` | where the AI was wrong, how it was caught, and what was checked |
| `data/raw/` | timestamped raw responses plus `manifest.csv` (url, status, sha256) |
| `data/processed/` | events.csv, flags.json, case_evidence.json, filing_text_checks.json, overlay_result.csv |

## Human inputs
- `config.toml`: every threshold, each labelled as an assumption with a reason.
- `overrides.csv`: human decisions (`name, bucket, reason, quote, claim_id`). They are shown beside the code bucket and never replace it.
- `private_overlay_example.csv`: SYNTHETIC lender data. `overlay.py` joins it locally and can only escalate a bucket.

Module contracts are in `SKILLS.md`.
