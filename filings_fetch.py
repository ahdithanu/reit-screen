"""Skill 1: filings_fetch. Downloads and caches raw responses. Never interprets them.

The only module that touches the network. In offline mode it serves the newest cached copy
and refuses to fetch.
"""
import csv
import hashlib
import os
import re
import sys
import time

import requests

from common import RAW, cik10, latest_cached, fetched_at_of, safe_key, utc_stamp

ALLOWED = [
    r"^https://data\.sec\.gov/api/xbrl/companyfacts/CIK\d{10}\.json$",
    r"^https://data\.sec\.gov/api/xbrl/frames/us-gaap/[A-Za-z]+/USD/CY\d{4}(Q[1-4]I?)?\.json$",
    r"^https://data\.sec\.gov/submissions/CIK\d{10}\.json$",
    r"^https://www\.sec\.gov/Archives/edgar/data/\d+/\d{18}/[^/]+$",
    r"^https://fred\.stlouisfed\.org/graph/fredgraph\.csv\?id=(DGS10|SOFR)$",
    r"^https://query1\.finance\.yahoo\.com/v8/finance/chart/[A-Z.\-]+\?range=1y&interval=1d$",
]
# Yahoo and FRED get a generic client name, never the SEC contact.
GENERIC_UA = "Mozilla/5.0 (compatible; reit-credit-screen/0.1; research script)"
MANIFEST = RAW / "manifest.csv"
# A filing document at a given accession never changes, so it is downloaded once (verify.py re-fetches quotes with force=True).
IMMUTABLE = {"archives"}


class Fetcher:
    def __init__(self, cfg, offline=False, prefer_cache=False):
        self.offline = offline
        self.prefer_cache = prefer_cache
        self.retries = cfg["sec"]["retries"]
        self.backoff = cfg["sec"]["backoff_seconds"]
        self.min_interval = 1.0 / cfg["sec"]["max_requests_per_second"]
        self._last_sec = 0.0
        self.ua = os.environ.get("SEC_USER_AGENT", "").strip()
        self.network_calls = 0

    def _require_ua(self):
        if not self.ua:
            sys.exit('SEC_USER_AGENT is not set. Run:  export SEC_USER_AGENT="Your Name your.email@example.com"\n'
                     "(or use --offline to run from the cache)")

    def _throttle(self):
        wait = self._last_sec + self.min_interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._last_sec = time.monotonic()

    def _manifest(self, row):
        RAW.mkdir(parents=True, exist_ok=True)
        new = not MANIFEST.exists()
        with open(MANIFEST, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["fetched_at", "source", "key", "url", "status", "bytes", "sha256", "path", "error"])
            if new:
                w.writeheader()
            w.writerow(row)

    def get(self, source, key, url, ext, sec, force=False):
        """Returns {path, fetched_at, url, error}. path is None on failure (a recorded gap)."""
        if not any(re.match(p, url) for p in ALLOWED):
            raise ValueError(f"URL not in the source table: {url}")
        key = safe_key(key)
        cached = latest_cached(source, key)
        if self.offline:
            if cached:
                return {"path": cached, "fetched_at": fetched_at_of(cached), "url": url, "error": None}
            return {"path": None, "fetched_at": None, "url": url, "error": "offline and no cached copy"}
        if cached and not force and (self.prefer_cache or source in IMMUTABLE):
            return {"path": cached, "fetched_at": fetched_at_of(cached), "url": url, "error": None}

        headers = {"User-Agent": GENERIC_UA}
        if sec:
            self._require_ua()
            headers = {"User-Agent": self.ua, "Accept-Encoding": "gzip, deflate"}
        err, status = None, None
        for attempt in range(self.retries):
            if sec:
                self._throttle()
            self.network_calls += 1
            try:
                r = requests.get(url, headers=headers, timeout=45)
            except requests.RequestException as e:
                err, status = f"{type(e).__name__}: {e}", None
            else:
                status = r.status_code
                if status == 200:
                    stamp = utc_stamp()
                    d = RAW / source
                    d.mkdir(parents=True, exist_ok=True)
                    path = d / f"{key}__{stamp}.{ext}"
                    n = 1
                    while path.exists():  # never overwrite
                        path = d / f"{key}__{stamp}_{n}.{ext}"
                        n += 1
                    path.write_bytes(r.content)
                    self._manifest({"fetched_at": stamp, "source": source, "key": key, "url": url, "status": 200,
                                    "bytes": len(r.content), "sha256": hashlib.sha256(r.content).hexdigest(),
                                    "path": str(path.relative_to(RAW)), "error": ""})
                    return {"path": path, "fetched_at": stamp, "url": url, "error": None}
                err = f"HTTP {status}"
                if status not in (429, 500, 502, 503, 504):
                    break
            time.sleep(self.backoff * (2 ** attempt))
        self._manifest({"fetched_at": utc_stamp(), "source": source, "key": key, "url": url, "status": status or "",
                        "bytes": 0, "sha256": "", "path": "", "error": err})
        if cached:  # fall back to the newest cached copy; its own fetched_at stays on every value read from it
            return {"path": cached, "fetched_at": fetched_at_of(cached), "url": url,
                    "error": f"{err}; fell back to cached copy fetched {fetched_at_of(cached)}"}
        return {"path": None, "fetched_at": None, "url": url, "error": err}

    # ---- source-specific URL builders (no interpretation) ----
    def companyfacts(self, cik):
        c = cik10(cik)
        return self.get("companyfacts", f"CIK{c}", f"https://data.sec.gov/api/xbrl/companyfacts/CIK{c}.json", "json", True)

    def submissions(self, cik):
        c = cik10(cik)
        return self.get("submissions", f"CIK{c}", f"https://data.sec.gov/submissions/CIK{c}.json", "json", True)

    def frame(self, tag, period):
        return self.get("frames", f"{tag}_{period}",
                        f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/{period}.json", "json", True)

    def archive(self, cik, accession, doc, force=False):
        acc = accession.replace("-", "")
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}"
        return self.get("archives", f"{int(cik)}_{acc}_{doc}", url, "html", True, force=force)

    def fred(self, series):
        return self.get("fred", series, f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}", "csv", False)

    def yahoo(self, ticker):
        return self.get("yahoo", ticker,
                        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1y&interval=1d", "json", False)


def archive_url(cik, accession, doc):
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession.replace('-', '')}/{doc}"
