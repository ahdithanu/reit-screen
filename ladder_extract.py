"""Skill 2: ladder_extract. FY2025 debt maturity ladder, latest cash and latest LongTermDebt.

Never fills a missing bucket and never substitutes another tag. Related tags the filer does
use are named in gap_reason as text only.
"""
import json
import re

from common import cik10, fact, fetched_at_of, parse_date

P = "LongTermDebtMaturitiesRepaymentsOfPrincipal"
LADDER = [  # (short name, us-gaap tag, calendar year it represents for a Dec-2025 FYE)
    ("y1_2026", P + "InNextTwelveMonths"),
    ("y2_2027", P + "InYearTwo"),
    ("y3_2028", P + "InYearThree"),
    ("y4_2029", P + "InYearFour"),
    ("y5_2030", P + "InYearFive"),
    ("after_2030", P + "AfterYearFive"),
]
CASH_TAG = "CashAndCashEquivalentsAtCarryingValue"
DEBT_TAG = "LongTermDebt"
# Named in gap reasons only; never used as values.
RELATED_HINT_TAGS = {
    CASH_TAG: ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "Cash"],
    DEBT_TAG: ["DebtInstrumentCarryingAmount", "LongTermDebtNoncurrent", "NotesPayable", "SecuredDebt",
               "UnsecuredDebt", "SeniorNotes", "DebtLongtermAndShorttermCombinedAmount"],
}
PERIODIC_FORMS = ("10-K", "10-K/A", "10-Q", "10-Q/A")


def companyfacts_url(cik):
    return f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10(cik)}.json"


def _maturity_hints(facts, period_end):
    """Names of any maturity-like tags (any taxonomy) that have a value at period_end in a 10-K."""
    hints = []
    for tax, tags in facts.items():
        for tag, body in tags.items():
            if not re.search(r"DebtMaturit|MaturitiesRepaymentsOfPrincipal", tag) or (tax == "us-gaap" and tag in {t for _, t in LADDER}):
                continue
            for vals in body.get("units", {}).values():
                if any(v.get("end") == period_end and str(v.get("form", "")).startswith("10-K") for v in vals):
                    hints.append(f"{tax}:{tag}")
                    break
    return sorted(hints)


def _usd(usg, tag):
    if tag not in usg:
        return None, "tag not reported by filer"
    units = usg[tag].get("units", {})
    if "USD" not in units:
        return None, f"no USD unit (units present: {sorted(units)})"
    return units["USD"], None


def extract(cik, label, cfg, cf_path):
    """Returns (facts, conflicts, ladder_dict). ladder_dict maps short name to fact."""
    cik = str(cik)
    url = companyfacts_url(cik)
    fetched = fetched_at_of(cf_path)
    facts_out, conflicts = [], []
    period_end, fy = cfg["ladder_period_end"], cfg["ladder_fiscal_year"]
    if cf_path is None:
        gap = "companyfacts not fetched"
        ladder = {s: fact(name=label, cik=cik, metric=f"ladder_{s}", unit="USD", source_url=url, tag_or_form=t,
                          period_end=period_end, gap_reason=gap) for s, t in LADDER}
        cash = fact(name=label, cik=cik, metric="latest_cash", unit="USD", source_url=url, tag_or_form=CASH_TAG, gap_reason=gap)
        debt = fact(name=label, cik=cik, metric="latest_debt", unit="USD", source_url=url, tag_or_form=DEBT_TAG, gap_reason=gap)
        return list(ladder.values()) + [cash, debt], conflicts, ladder, cash, debt

    data = json.loads(open(cf_path, "rb").read())
    allfacts = data.get("facts", {})
    usg = allfacts.get("us-gaap", {})
    hints = None
    ladder = {}
    for short, tag in LADDER:
        base = dict(name=label, cik=cik, metric=f"ladder_{short}", unit="USD", source_url=url, tag_or_form=tag,
                    period_end=period_end, fetched_at=fetched)
        vals, err = _usd(usg, tag)
        cands = [] if vals is None else [v for v in vals if v.get("end") == period_end and v.get("form") in ("10-K", "10-K/A")]
        if not cands:
            if hints is None:
                hints = _maturity_hints(allfacts, period_end)
            reason = err or f"no 10-K fact with end {period_end}"
            if hints:
                reason += "; filer reports related maturity tags (not used): " + ", ".join(hints[:6])
            ladder[short] = fact(**base, gap_reason=reason)
            continue
        pref = [v for v in cands if v.get("fy") == fy and v.get("fp") == "FY" and v.get("form") == "10-K"] or cands
        pref.sort(key=lambda v: (v["filed"], v.get("accn", "")))
        chosen = pref[0]
        distinct = sorted({v["val"] for v in cands})
        if len(distinct) > 1:
            conflicts.append({"name": label, "tag": tag, "value_a": chosen["val"],
                              "value_b": [d for d in distinct if d != chosen["val"]],
                              "reason": f"{len(cands)} 10-K facts for end {period_end} disagree; kept earliest original "
                                        f"10-K {chosen.get('accn')} filed {chosen['filed']}"})
        ladder[short] = fact(**base, value=float(chosen["val"]), filed=chosen["filed"], accession=chosen.get("accn"))
    facts_out.extend(ladder.values())

    def latest(tag, metric):
        base = dict(name=label, cik=cik, metric=metric, unit="USD", source_url=url, tag_or_form=tag, fetched_at=fetched)
        vals, err = _usd(usg, tag)
        vals = [] if vals is None else [v for v in vals if v.get("form") in PERIODIC_FORMS and "end" in v and "start" not in v]
        if not vals:
            present = [h for h in RELATED_HINT_TAGS.get(tag, []) if h in usg]
            reason = err or "no 10-K/10-Q instant fact"
            if present:
                reason += "; filer reports related tags (not used): " + ", ".join(present)
            return fact(**base, gap_reason=reason)
        end = max(v["end"] for v in vals)
        same = sorted([v for v in vals if v["end"] == end], key=lambda v: (v["filed"], v.get("accn", "")))
        chosen = same[0]
        distinct = sorted({v["val"] for v in same})
        if len(distinct) > 1:
            conflicts.append({"name": label, "tag": tag, "value_a": chosen["val"],
                              "value_b": [d for d in distinct if d != chosen["val"]],
                              "reason": f"facts for end {end} disagree across filings; kept first filed {chosen.get('accn')}"})
        age = (parse_date(cfg["as_of"]) - parse_date(end)).days
        stale = age > cfg["staleness"]["max_age_days"]
        base.pop("tag_or_form")
        f = fact(**base, value=float(chosen["val"]), period_end=end, filed=chosen["filed"], accession=chosen.get("accn"),
                 tag_or_form=f"{tag} ({chosen.get('form')})",
                 gap_reason=(f"STALE: latest value is {age} days old at as_of; no newer filing tagged" if stale else None))
        return f

    cash = latest(CASH_TAG, "latest_cash")
    debt = latest(DEBT_TAG, "latest_debt")
    facts_out += [cash, debt]
    return facts_out, conflicts, ladder, cash, debt


def value_at(cf_path, tag, end):
    """Companyfacts value for tag at an exact instant from a 10-K (used for cross-checks). (val, accn) or (None, reason)."""
    data = json.loads(open(cf_path, "rb").read())
    vals, err = _usd(data.get("facts", {}).get("us-gaap", {}), tag)
    if vals is None:
        return None, err
    c = sorted([v for v in vals if v.get("end") == end and "start" not in v and v.get("form") in ("10-K", "10-K/A")],
               key=lambda v: v["filed"])
    if not c:
        return None, f"no 10-K instant at {end}"
    return float(c[0]["val"]), c[0].get("accn")


# ---------------------------------------------------------------- latest 10-Q ladder (display only, never scored)
# In 10-Qs these filers label buckets relative to the CURRENT fiscal year: RemainderOfFiscalYear = rest of the
# current year, InNextTwelveMonths = next fiscal year, InYearTwo = the year after, and so on. Checked against the
# 10-K for overlapping years (verify.py section 7). Calendar years below assume a December fiscal year end.
Q_LADDER = [("rest", P + "RemainderOfFiscalYear", 0), ("y1", P + "InNextTwelveMonths", 1), ("y2", P + "InYearTwo", 2),
            ("y3", P + "InYearThree", 3), ("y4", P + "InYearFour", 4), ("y5", P + "InYearFive", 5), ("after", P + "AfterYearFive", 6)]


def extract_q(cik, label, cfg, cf_path):
    """Latest 10-Q maturity ladder after the 10-K ladder date. Returns dict with period_end, buckets {calendar label: fact}."""
    url = companyfacts_url(cik)
    out = {"period_end": None, "accession": None, "filed": None, "buckets": [], "gap_reason": None}
    if cf_path is None:
        out["gap_reason"] = "companyfacts not fetched"
        return out
    usg = json.loads(open(cf_path, "rb").read()).get("facts", {}).get("us-gaap", {})
    facts = []
    for _, tag, _ in Q_LADDER:
        for v in (usg.get(tag, {}).get("units", {}).get("USD", []) or []):
            if v.get("form") in ("10-Q", "10-Q/A") and v.get("end", "") > cfg["ladder_period_end"] and "start" not in v:
                facts.append((tag, v))
    if not facts:
        out["gap_reason"] = "no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder)"
        return out
    end = max(v["end"] for _, v in facts)
    year = int(end[:4])
    same = {}
    for tag, v in sorted(facts, key=lambda x: x[1]["filed"]):
        if v["end"] == end and tag not in same:
            same[tag] = v
    first = next(iter(same.values()))
    out.update(period_end=end, accession=first.get("accn"), filed=first.get("filed"))
    for short, tag, off in Q_LADDER:
        lab = f"{year} rest" if off == 0 else (f"{year + off}" if off < 6 else f"after {year + 5}")
        v = same.get(tag)
        out["buckets"].append({"key": short, "label": lab, "tag": tag,
                               "fact": fact(name=label, cik=str(cik), metric=f"q_ladder_{short}", unit="USD", source_url=url, tag_or_form=tag,
                                            period_end=end, filed=v and v["filed"], accession=v and v.get("accn"),
                                            value=float(v["val"]) if v else None, fetched_at=fetched_at_of(cf_path),
                                            gap_reason=None if v else f"tag not reported in the 10-Q for {end}")})
    return out


# ---------------------------------------------------------------- secured vs unsecured (display only, never scored)
def secured_split(cik, label, cfg, cf_path):
    """SecuredDebt and UnsecuredDebt at the same latest period end (10-K/10-Q). No other tag is substituted."""
    url = companyfacts_url(cik)
    res = {"period_end": None, "secured": None, "unsecured": None, "gap_reason": None, "source_url": url}
    if cf_path is None:
        res["gap_reason"] = "companyfacts not fetched"
        return res
    usg = json.loads(open(cf_path, "rb").read()).get("facts", {}).get("us-gaap", {})

    def by_end(tag):
        d = {}
        for v in usg.get(tag, {}).get("units", {}).get("USD", []) or []:
            if v.get("form") in PERIODIC_FORMS and "start" not in v:
                d.setdefault(v["end"], v)
        return d
    s, u = by_end("SecuredDebt"), by_end("UnsecuredDebt")
    common = sorted(set(s) & set(u))
    if not common:
        res["gap_reason"] = ("SecuredDebt and UnsecuredDebt are not both tagged at any common period end"
                             + ("" if (s or u) else " (neither tag reported)"))
        return res
    end = common[-1]
    age = (parse_date(cfg["as_of"]) - parse_date(end)).days
    res.update(period_end=end, secured=float(s[end]["val"]), unsecured=float(u[end]["val"]),
               accession=s[end].get("accn"), stale=age > cfg["staleness"]["max_age_days"])
    if res["stale"]:
        res["gap_reason"] = f"latest common period end {end} is {age} days old; shown as stale"
    return res
