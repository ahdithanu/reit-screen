"""Skill 3: event_reader. Lists 2026 filings, classifies them by 8-K item code, extracts verbatim quotes.

Never summarizes, paraphrases or infers. A 1.01 is "financing activity, needs reading", nothing more.
"""
import json
import re

from common import cik10, html_to_text
from filings_fetch import archive_url


def submissions_url(cik):
    return f"https://data.sec.gov/submissions/CIK{cik10(cik)}.json"


def tickers(sub_path):
    if sub_path is None:
        return []
    return json.loads(open(sub_path, "rb").read()).get("tickers", [])


def list_events(cik, label, cfg, sub_path):
    """Returns (events, coverage_gap). One event per (filing, flagged code)."""
    ev_cfg = cfg["events"]
    since = cfg["events_since"]
    if sub_path is None:
        return [], "submissions not fetched"
    sub = json.loads(open(sub_path, "rb").read())
    r = sub["filings"]["recent"]
    n = len(r["form"])
    gap = None
    if n and min(r["filingDate"]) > since:
        gap = (f"submissions 'recent' list starts {min(r['filingDate'])}, after {since}; "
               f"older pages in filings.files not read, so early-2026 filings may be missing")
    events = []
    for i in range(n):
        filed = r["filingDate"][i]
        if filed < since:
            continue
        form, acc, doc = r["form"][i], r["accessionNumber"][i], r["primaryDocument"][i]
        items = r.get("items", [""] * n)[i] or ""
        base = {"name": label, "cik": str(cik), "form": form, "filed": filed, "accession": acc, "items": items,
                "primary_doc": doc, "filing_url": archive_url(cik, acc, doc) if doc else None}
        if form in ev_cfg["hard_trigger_forms"]:
            events.append({**base, "item_code": form, "class": "negative", "hard_trigger": True})
            continue
        if not form.startswith("8-K"):
            continue
        for code in [c.strip() for c in items.split(",") if c.strip()]:
            if code in ev_cfg["hard_trigger_items"]:
                events.append({**base, "item_code": code, "class": "negative", "hard_trigger": True})
            elif code in ev_cfg["scored_negative_items"]:
                events.append({**base, "item_code": code, "class": "negative", "hard_trigger": False})
            elif code in ev_cfg["financing_items"]:
                events.append({**base, "item_code": code, "class": "financing (needs reading)", "hard_trigger": False})
            else:
                events.append({**base, "item_code": code, "class": "other", "hard_trigger": False})
    return events, gap


def needs_document(ev):
    return ev["class"] != "other" and ev.get("primary_doc")


def extract_quote(ev, doc_path, nchars):
    """Verbatim first `nchars` characters starting at the item heading (whitespace collapsed only)."""
    if doc_path is None:
        return None, "primary document not fetched"
    text = html_to_text(open(doc_path, "rb").read().decode("utf-8", errors="replace"))
    code = ev["item_code"]
    if code.startswith("NT "):
        # The heading is "PART III — NARRATIVE". Plain "Part III of this Form" in Part II is a cross-reference.
        m = re.search(r"PART\s+III\s*[-—–:]*\s*NARRATIVE", text, re.IGNORECASE)
        if not m:
            return None, "'PART III — NARRATIVE' heading not found in NT form"
    else:
        # A heading, not a cross-reference: skip "Item 1.03 of this Report", "Item 2.03 below", "Item 1.01 above", etc.
        xref = r"(?!\s*(?:of\b|below\b|above\b|herein\b|hereof\b|and\b|or\b|is\b|are\b|,|;|\)))"
        m = re.search(r"Item\s*" + re.escape(code) + r"(?!\d)\.?" + xref, text, re.IGNORECASE)
        if not m:
            return None, f"'Item {code}' heading not found in primary document"
    return text[m.start(): m.start() + nchars], None


def counts(events):
    out = {"negative": 0, "hard_trigger": 0, "financing": 0, "other": 0, "filings_2026": len({e["accession"] for e in events})}
    for e in events:
        if e["class"] == "negative":
            out["negative"] += 1
            out["hard_trigger"] += int(e["hard_trigger"])
        elif e["class"].startswith("financing"):
            out["financing"] += 1
        else:
            out["other"] += 1
    return out


# ---------------------------------------------------------------- case-file evidence (verbatim only)
from common import html_to_blocks  # noqa: E402

MONTHS = r"(January|February|March|April|May|June|July|August|September|October|November|December)"
DEBT_RE = re.compile(r"credit facilit|revolv|term loan|senior notes|unsecured notes|notes payable|mortgage|\bloans?\b|credit agreement", re.I)
SKIP_RE = re.compile(r"\bASU\b|FASB|interest rate cap", re.I)  # accounting-standard and hedge boilerplate is not a maturity statement


def latest_form(sub_path, form):
    r = json.loads(open(sub_path, "rb").read())["filings"]["recent"]
    for i, f in enumerate(r["form"]):  # recent is newest first
        if f == form:
            return {"accession": r["accessionNumber"][i], "doc": r["primaryDocument"][i], "filed": r["filingDate"][i],
                    "period": r.get("reportDate", [None] * len(r["form"]))[i]}
    return None


def paragraphs_2027(doc_path, limit=5, min_len=60):
    """Verbatim blocks that state a 2027 maturity of a debt instrument: contain '2027', a debt word and 'matur'.
    Accounting-standard boilerplate (ASU/FASB) and rate-cap notes are skipped. First `limit` distinct blocks in document order."""
    out = []
    blocks = html_to_blocks(open(doc_path, "rb").read().decode("utf-8", errors="replace"))
    bullet = lambda x: x[:1] in "•●▪-"
    for i, b in enumerate(blocks):
        if (len(b) >= min_len and "2027" in b and DEBT_RE.search(b) and re.search(r"matur", b, re.I)
                and not SKIP_RE.search(b) and b not in out):
            if bullet(b):  # a list item: keep its lead-in sentence and sibling items so the list reads whole
                j = i
                while j > 0 and bullet(blocks[j - 1]):
                    j -= 1
                k = i
                while k + 1 < len(blocks) and bullet(blocks[k + 1]):
                    k += 1
                b = " ".join(blocks[max(j - 1, 0): k + 1])
                if b in out:
                    continue
            out.append(b)
            if len(out) >= limit:
                break
    return out


def maturity_dates_2027(doc_path, limit=8):
    """Sentences (verbatim) that contain a dated 2027 month next to debt words, with the date string extracted."""
    out, seen = [], set()
    for b in html_to_blocks(open(doc_path, "rb").read().decode("utf-8", errors="replace")):
        if "2027" not in b or not DEBT_RE.search(b):
            continue
        for m in re.finditer(MONTHS + r"(\s+\d{1,2},)?\s+2027", b):
            s0 = b.rfind(". ", 0, m.start())
            s1 = b.find(". ", m.end())
            sent = b[s0 + 2 if s0 != -1 else 0: s1 + 1 if s1 != -1 else len(b)]
            if not DEBT_RE.search(sent) or sent in seen:
                continue
            seen.add(sent)
            out.append({"date": m.group(0), "sentence": sent})
            if len(out) >= limit:
                return out
    return out


def maturity_table_rows(doc_path, max_rows=14):
    """Rows (verbatim cell text, '$' and empty cells dropped) of the first table after the phrase
    'principal maturities' in a filing. Display only; nothing is parsed into a number."""
    from common import html_to_text
    html = open(doc_path, "rb").read().decode("utf-8", errors="replace")
    m = re.search(r"principal\s+maturities", html, re.I)
    if not m:
        return None, "phrase 'principal maturities' not found"
    t0 = html.find("<table", m.end())
    t1 = html.find("</table>", t0)
    if t0 == -1 or t1 == -1:
        return None, "no table after the phrase"
    rows = []
    for tr in re.findall(r"<tr\b.*?</tr>", html[t0:t1], re.S | re.I):
        cells = [html_to_text(c).replace("​", "").strip() for c in re.findall(r"<t[dh]\b.*?</t[dh]>", tr, re.S | re.I)]
        cells = [c for c in cells if c and c != "$"]
        if cells:
            rows.append(" | ".join(cells))
    return rows[:max_rows], None


def debt_rows_2027(doc_path, limit=8):
    """Verbatim table rows whose label names a debt instrument and that contain '2027' (e.g. a 10-Q debt table)."""
    from common import html_to_text
    html = open(doc_path, "rb").read().decode("utf-8", errors="replace")
    out = []
    for tr in re.findall(r"<tr\b.*?</tr>", html, re.S | re.I):
        if "2027" not in tr:
            continue
        cells = [html_to_text(c).replace("​", "").strip() for c in re.findall(r"<t[dh]\b.*?</t[dh]>", tr, re.S | re.I)]
        cells = [c for c in cells if c and c != "$"]
        if cells and DEBT_RE.search(cells[0]) and any("2027" in c for c in cells):
            row = " | ".join(cells)
            if row not in out:
                out.append(row)
                if len(out) >= limit:
                    break
    return out
