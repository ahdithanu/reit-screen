# SKILLS.md: module contracts

What this tool is for: a credit officer at a regional bank that holds participations in the syndicated unsecured facilities of listed office and retail REITs. Each quarter they decide which borrowers move to **ACT NOW** (enhanced monitoring), which stay on **WATCH**, and which are **CAN'T CALL** because public data is too thin. *That persona is an assumption. No practitioner has validated it.*

The data path has five skills. Each one is a single Python module with a written contract. `run.py` calls them in order. Two downstream stages, `verify.py` and `report.py`, read what the skills produce and never feed anything back into them.

```
filings_fetch ──► data/raw/  (timestamped cache, the only network boundary)
     │
     ├──► ladder_extract ──┐
     ├──► event_reader ────┼──► synthesize ──► data/processed/metrics.csv, claims.csv
     └──► market_context ──┘                         │
                                                     ├──► verify.py  ──► verification.md
                                                     └──► report.py  ──► report.html
```

## Rules every module follows

1. **No LLM calls**, anywhere in the data path. Every output comes from deterministic code reading cached files.
2. **No imputation.** A missing value becomes a `Fact` with `value=None` and a `gap_reason`. No gap is ever filled, interpolated, carried forward or replaced with a nearby tag.
3. **Provenance travels with the value.** Each fact is one record:
   `{name, cik, metric, value, unit, source_url, tag_or_form, period_end, filed, accession, fetched_at, gap_reason}`.
   That record goes into `metrics.csv` and `claims.csv` exactly as created, never rebuilt later from the report.
4. **Only `filings_fetch` touches the network.** All other modules read `data/raw/` only. `--offline` makes `filings_fetch` read the newest cached copy and refuse any network call.
5. **Python 3 standard library plus `requests` and `pandas` only.** Rules live in `config.toml`, read with stdlib `tomllib` (Python 3.11+). There is no custom parser.
6. **Human decisions live in `overrides.csv`** (`name, bucket, reason, quote, claim_id`). Code reads it and shows the override **beside** the code bucket. It never replaces the code bucket and never writes to the file.

---

## 1. `filings_fetch`: get and cache, never interpret

**Does:** downloads every raw input and writes it to `data/raw/<source>/<key>__<UTC timestamp>.<ext>`. Each fetch adds a line to `data/raw/manifest.csv` with url, status, bytes, sha256 and fetched_at.

**Inputs:** the CIK list from `config.toml`, plus document URLs requested by `event_reader` (8-K primary documents) and `verify.py` (10-K documents for the spot checks).

**Sources:**
| source key | URL |
|---|---|
| `companyfacts` | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` |
| `frames` | `https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/{period}.json` (cross-checks) |
| `submissions` | `https://data.sec.gov/submissions/CIK##########.json` |
| `archives` | `https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{doc}` |
| `fred` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10`, `id=SOFR` |
| `yahoo` | `https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?range=1y&interval=1d` |

**Outputs:** the cached files and the manifest. Its return value is only `{key: path_or_None, error}`.

**Behaviour:**
- Reads `SEC_USER_AGENT` from the environment and stops with a clear message if it is unset. It sends that header on every SEC and Archives request.
- Global limiter of at most 8 requests per second to SEC hosts. Retries 429 and 5xx with exponential backoff (3 tries), then records a failure.
- A failed Yahoo or FRED fetch is recorded in the manifest as a gap. It never raises.

**Must never:** parse a value, choose a period, filter filings, rename a field, or overwrite an existing cache file. A newer timestamp sits beside the old one. It also never fetches a URL that is missing from the source table above.

---

## 2. `ladder_extract`: debt maturity ladder, cash and debt

**Does:** reads cached company facts and returns, for each name:
- **Ladder (FY2025 10-K, period end 2025-12-31):** the six us-gaap tags
  `LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths`, `...InYearTwo`, `...InYearThree`, `...InYearFour`, `...InYearFive`, `...AfterYearFive`.
  It takes only the fact where `form == 10-K`, `fy == 2025`, `fp == FY` and `end == 2025-12-31`. If the 2025-12-31 value appears in more than one filing, it keeps the earliest original 10-K and records the duplicate in `conflicts`.
- **`latest_cash`:** `CashAndCashEquivalentsAtCarryingValue`, the most recent `end` date from any 10-K or 10-Q.
- **`latest_debt`:** `LongTermDebt`, chosen the same way.
- **`ladder_complete`:** true only if all six buckets exist.
- **`stale` flag:** set when the latest cash or debt `end` is older than `staleness.max_age_days` from `as_of`.

**Inputs:** `data/raw/companyfacts/*`, `config.toml`. For the cross-check: `data/raw/frames/*`.

**Outputs:** a list of `Fact` records per name, plus a `conflicts` list `{name, tag, value_a, value_b, reason}`.

**Must never:**
- fill a missing bucket, whether with zero, a derived amount, or the difference between LongTermDebt and the other buckets
- swap in another tag silently, such as `LongTermDebtMaturitiesRepaymentsOfPrincipalRemainderOfFiscalYear`, `...YearTwoAndThree`, `DebtInstrumentCarryingAmount` or a company extension tag. If one of those exists, it goes into `gap_reason` as text ("filer uses X instead") and the bucket stays `None`.
- mix units. Anything other than USD is a gap.
- read 8-Ks, prices or rates.

---

## 3. `event_reader`: 2026 filings and verbatim quotes

**Does:**
1. From cached submissions, lists every filing with `filingDate >= events_since` (2026-01-01). It records form, date, accession and the `items` string.
2. Sorts each one into a class using config only:
   - **negative:** 8-K items `1.03, 2.04, 2.06, 3.01`, and forms `NT 10-K`, `NT 10-Q`
   - **financing (needs reading):** 8-K items `1.01, 2.03`
   - **other:** everything else. It is counted and never scored.
3. Asks `filings_fetch` for the primary document of every negative or financing 8-K. Then, from the cached HTML, it removes tags (stdlib `html.parser`), collapses whitespace, finds the first heading matching `Item\s*{code}` after the cover page, and stores the **first 400 characters after that heading, verbatim**, together with the filing URL. If no heading is found, it stores `quote=None` with `gap_reason="item heading not found in primary document"`.
   NT forms have no item heading. For those, the quote is the first 400 characters of the Part III narrative. If that cannot be found, it is recorded as a gap.

**Inputs:** `data/raw/submissions/*`, `data/raw/archives/*`, `config.toml`.

**Outputs:** `events` records `{name, form, filed, accession, items, class, item_code, quote, quote_url, gap_reason}` and a count per name and class.

**Case-file evidence (same contract):** for the three case-file names, the module also extracts:
- verbatim 10-Q blocks that state a 2027 debt maturity (ASU/FASB boilerplate is skipped; a list item keeps its lead-in and sibling items)
- the verbatim rows of the 10-Q table after the phrase "principal maturities"
- verbatim 10-K sentences that carry a dated 2027 month next to debt words

All of this is display only and never parsed into a score.

**Must never:** summarize, paraphrase, shorten in the middle, translate or "clean" a quote apart from the whitespace collapse. It never infers meaning: a 1.01 is never labelled "refinancing", only "financing activity, needs reading". It never decides whether a 2026 maturity was dealt with.

---

## 4. `market_context`: prices and rates, context only

**Does:**
- **Per name** (ticker taken from the submissions `tickers` field, never hard-coded): from cached Yahoo daily closes, `drawdown_52w = 1 - last_close / max(close over the window)` and `return_6m = last_close / close_on_or_before(last_date - 182d) - 1`. Each one records the as-of date and the price dates it used.
- **Sector-relative drawdown:** `rel_drawdown = drawdown_52w - median(drawdown_52w of the same segment within the 12 names)`. The median and the peers used are recorded. A name with no price data is left out of the median. The market score uses only `rel_drawdown`. The absolute drawdown and the 6-month return are display only. The peer group is always all 12 names, even during the three-name checkpoint run.
- **Rates line:** DGS10 latest level, change over 12 months (latest minus value on or before the date 365 days earlier), and SOFR latest level, each with its observation date.

**Inputs:** `data/raw/yahoo/*`, `data/raw/fred/*`, `data/raw/submissions/*` for tickers.

**Outputs:** `Fact` records for drawdown and 6-month return per name, plus one `rates` record.

**Must never:** offer a view on valuation, describe a price as cheap or rich, adjust prices for dividends beyond what Yahoo returns as `close`, or fill price gaps. Rates **never** feed a score or bucket. They appear in the report as context only. A Yahoo failure becomes a recorded gap with the HTTP status or parse error.

---

## 5. `synthesize`: scores, buckets, disagreement and flip test

**Does:** using only the rules in `config.toml`:
- **`filings_risk` score**, built from wall_2027 share and scored negative events. Wall-to-cash is computed and **shown only, for 0 points**, because year-end cash leaves out revolver capacity.
- **Missing ladder bucket:** the 2027 share is computed over the buckets present and labelled an **upper bound**, since a missing bucket can only lower it. If the upper bound is below `wall_share_watch`, the name scores 0 and stays callable. Otherwise it is CAN'T CALL.
- **`year1_unresolved` flag** (0 points): set when 30% or more of the stack was due in 2026. It keeps the name out of ROUTINE, because code cannot tell whether 2026 was dealt with.
- **`market_view` score**, from the sector-relative drawdown only.
- **Bucket:** four buckets, in this order:
  1. Any **hard-trigger** event (1.03, 2.04, 3.01, NT 10-K, NT 10-Q) → ACT NOW.
  2. Otherwise, 2027 share not computable → CAN'T CALL. The flag names the missing input.
  3. Otherwise ACT NOW if `filings_risk >= act_now_filings_min`, or if both scores reach the joint minimums.
  4. Otherwise **ROUTINE** if there are no flags at all and market data is present.
  5. Otherwise WATCH.
- **Refinancing tag:** high-wall names (2027 or 2026 share at or above the watch threshold) with a 2026 item 1.01 or 2.03 get "refinancing evidence present: read before acting". The tag never changes a bucket.
- **Overrides:** reads `overrides.csv` and writes `override_bucket`, `override_reason` and `override_claim_id` next to `bucket`. It never edits `bucket`.
- **Disagreement flag:** "filings say risk, market is calm" when `filings_risk >= hi` (or a hard trigger fired) and `market_view <= calm`. "market is selling off, filings are clean" when the reverse holds. A name with a missing market input gets no disagreement flag; it gets a gap marker instead.
- **Flip test:** for each ACT NOW and WATCH name, and for each numeric threshold, it moves that one threshold to the name's own metric value (just across the boundary), re-runs the bucket rules, and keeps the move only if the bucket changes. It reports `distance_pct = |metric - threshold| / threshold` and names the nearest threshold. Hard triggers are not numeric and are reported as "only a reversal of the event flips this". A plain-language flip fact comes from a fixed template keyed on the nearest driver.
- **Every flag** lists its inputs (metric, value, threshold) and the `claim_id`s that support it.

**Inputs:** outputs of skills 2–4, plus `config.toml`.

**Outputs:** `data/processed/metrics.csv` (one row per name, every metric with period end and gap reason), `claims.csv` (`claim_id, claim, source_url, tag_type, checked, note`) and `data/processed/flags.json`.

**Must never:** fetch anything, read raw files, use a threshold that is missing from `config.toml`, use rates, use financing 8-Ks to lower a score (they are evidence for a human reader, not a score input), or overrule a CAN'T CALL with a judgement call. `checked` in claims.csv is written as `no` and only `verify.py` may change it to `yes`.

---

## Downstream stages (not skills, same discipline)

**`verify.py`:** runs these checks:
- the OPI control
- cross-extraction (companyfacts compared with frames)
- the 10-K text spot check on SLG, CBL and SPG: the iXBRL cells in the 10-K table, a scale-mismatch check, and the **printed table Total, which is the primary control total** (LongTermDebt is secondary)
- the 2027 split by XBRL dimension, tagged *inferred*, and JV debt shown as *context only*
- quote re-fetch for the case-file names
- override quotes matched against the filing behind their claim_id It writes the raw diffs to `verification.md` and sets `checked=yes` only for claims it actually matched against filing text. It never edits metrics.

**`report.py`:** reads processed outputs only and writes one self-contained `report.html` with inline CSS and inline SVG charts, no external requests. Every number on the page cites a `claim_id`. It never computes a new metric. Any number it needs must already be in `metrics.csv`. It shows the code bucket and any human override side by side. Its Limits section must include:
- no interest coverage (interest expense is tagged inconsistently)
- no undrawn revolver data
- the ladder is as of 2025-12-31
- prices are unofficial (Yahoo)
- the persona has not been validated by a practitioner
- **the ladder does not separate secured property-level mortgages from unsecured debt, and does not show extension options, so a large wall is not the same as refinancing risk for the unsecured facility**

**`private_overlay_example.csv` and `overlay.py`:** a SYNTHETIC lender file (internal_rating, covenant_headroom, undrawn_revolver, own_facility_maturity). It is joined locally on ticker. Under the `[overlay]` rules it can only escalate a bucket, and it writes `overlay_bucket` beside the code bucket. It is never sent to any API or model.
