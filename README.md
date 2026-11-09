# REIT borrower screen for syndicate lenders

What a regional-bank participant in listed office and retail REIT credit facilities cannot see, built only from public data (SEC EDGAR XBRL and filings, FRED, Yahoo prices). It is deterministic Python with no LLM calls in the data path. Every number carries its provenance.

- Live page: https://reit-screen.vercel.app (served from `public/`, frozen at the 2026-11-09 run)
- What is solid, what is unchecked, what could not be verified: [SUMMARY.md](SUMMARY.md)

## Reproduce offline (the submitted run, zero network calls)

Python 3.11+ (needs `tomllib`).

```bash
pip install -r requirements.txt
```

Download the filing cache from the release and extract it at the repo root. It recreates `data/raw/`, 14.8 MB compressed.

```bash
gh release download cache-2026-11-09 --repo ahdithanu/reit-screen -p raw_cache_2026-11-09.tar.gz
```

```bash
tar -xzf raw_cache_2026-11-09.tar.gz
```

Check that the archive is intact. It should print `3550390d601a513c029d863e4af2a2f0572e4ceaf64603d9735d83c3e567cdd3`.

```bash
shasum -a 256 raw_cache_2026-11-09.tar.gz
```

```bash
python run.py --offline --names all
```

The run ends with `network calls this run: 0`. It rebuilds `report.html`, `public/index.html`, `claims.csv`, `verification.md`, the source list and everything in `data/processed/` from the cache, and stops with an error if the OPI pipeline control does not land in ACT NOW. The only differences from the committed files are the "refreshed" timestamp and the download times in the claim notes.

## Run online (fresh data)

```bash
export SEC_USER_AGENT="Your Name your.email@example.com"
```

```bash
python run.py --names all --as-of today
```

Other flags:
- `--cached`: online, but reuses cached files.
- `--names subset`: OPI, SLG and CBL only (the step-2 checkpoint). `--names all` is the 24 names in config.toml.
- `--no-verify`: skips verification.

The scheduled weekday refresh in `.github/workflows/refresh.yml` is switched off, so the live page stays fixed at the submitted run. To turn it back on, uncomment the `schedule` lines and push. Manual runs ("Run workflow" in GitHub Actions) still work.

## Outputs
| file | what |
|---|---|
| `report.html`, `public/index.html` | the dashboard: one self-contained page with no external requests. `public/` is what Vercel serves; `public/data/` holds the CSVs, the source list and verification.md |
| `source_list.md`, `source_list.csv` | the key claims behind the memo, each with its claim_id, source, fact or inference, and checked flag |
| `data/processed/metrics.csv` | one row per name: every metric, period end, gap reason, code bucket, override, flip test |
| `claims.csv` | `claim_id, claim, source_url, tag_type, checked, note`; every number in the report cites one |
| `verification.md` | control, companyfacts vs frames diffs, 10-K and 10-Q text checks, control totals, quote re-checks, conflicts and gaps |
| `ai_log.md` | where the AI was wrong, how it was caught, and what was checked |
| `SUMMARY.md` | plain-language summary of what is solid, unchecked and unverifiable |
| `design/template.html` | the page design; `report.py` fills its data block. `design/build_template.py` rebuilds it from the reviewed design |
| `data/raw/` | not in git; timestamped raw responses plus `manifest.csv` (url, status, sha256). Restore from the release above |

## Human inputs
- `config.toml`: every threshold and the decision-maker persona, each labelled as an assumption with a reason.
- `overrides.csv`: human decisions (`name, bucket, reason, quote, claim_id`). They are shown beside the code bucket and never replace it.
- `signoff.csv`: claim ids a human has reviewed. The page shows "human reviewed" only for these.
- `private_overlay_example.csv`: SYNTHETIC lender data. `overlay.py` joins it locally and can only escalate a bucket.

Module contracts are in `SKILLS.md`.
