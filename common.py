"""Shared helpers: paths, config, the Fact record, cache lookup, HTML-to-text."""
import datetime as dt
import re
import tomllib
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"

FACT_FIELDS = ["name", "cik", "metric", "value", "unit", "source_url", "tag_or_form",
               "period_end", "filed", "accession", "fetched_at", "gap_reason"]


def load_config():
    with open(ROOT / "config.toml", "rb") as f:
        return tomllib.load(f)


def utc_stamp():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def cik10(cik):
    return f"{int(cik):010d}"


def safe_key(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


def latest_cached(source, key):
    """Newest cached file for (source, key), or None. Filenames are <key>__<UTC stamp>.<ext>."""
    d = RAW / source
    if not d.exists():
        return None
    files = sorted(p for p in d.glob(f"{key}__*") if p.is_file())
    return files[-1] if files else None


def fetched_at_of(path):
    if path is None:
        return None
    m = re.search(r"__(\d{8}T\d{6}Z)", Path(path).name)
    return m.group(1) if m else None


def fact(**kw):
    rec = dict.fromkeys(FACT_FIELDS)
    unknown = set(kw) - set(FACT_FIELDS)
    if unknown:
        raise ValueError(f"unknown fact fields {unknown}")
    rec.update(kw)
    return rec


def parse_date(s):
    return dt.date.fromisoformat(s)


class _TextExtractor(HTMLParser):
    BLOCK = {"p", "div", "br", "tr", "td", "th", "li", "table", "h1", "h2", "h3", "h4", "h5", "h6"}
    HIDDEN = {"script", "style", "ix:header", "head"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.HIDDEN:
            self.skip += 1
        if tag in self.BLOCK:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in self.HIDDEN and self.skip:
            self.skip -= 1
        if tag in self.BLOCK:
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def html_to_text(html):
    """Visible text with every whitespace run (incl. nbsp) collapsed to one space. Nothing else changes."""
    p = _TextExtractor()
    p.feed(html)
    p.close()
    return re.sub(r"\s+", " ", "".join(p.parts)).strip()


class _BlockExtractor(_TextExtractor):
    def handle_starttag(self, tag, attrs):
        if tag in self.HIDDEN:
            self.skip += 1
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.HIDDEN and self.skip:
            self.skip -= 1
        if tag in self.BLOCK:
            self.parts.append("\n")


def html_to_blocks(html):
    """Visible text split at block tags (p, div, td, ...). Whitespace collapsed inside each block only."""
    p = _BlockExtractor()
    p.feed(html)
    p.close()
    return [b for b in (re.sub(r"\s+", " ", x).strip() for x in "".join(p.parts).split("\n")) if b]
