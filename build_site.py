"""build_site.py: builds the site that Vercel serves (public/index.html, plus report.html).

Fills the dashboard template from processed outputs (report.build), then injects the page-head
tags the site needs. Reads only processed outputs; makes no network calls.

    python build_site.py
"""
from common import ROOT, load_config

NOINDEX = '<meta name="robots" content="noindex, nofollow">'


def inject_head(html):
    if NOINDEX in html:
        return html
    i = html.find("</head>")
    if i < 0:
        raise SystemExit("build_site: no </head> in the built page")
    return html[:i] + NOINDEX + "\n" + html[i:]


def build_site(cfg):
    import report
    report.build(cfg)
    for path in (ROOT / "public" / "index.html", ROOT / "report.html"):
        path.write_text(inject_head(path.read_text()))
    return ROOT / "public" / "index.html"


if __name__ == "__main__":
    out = build_site(load_config())
    print(f"build_site: wrote {out.relative_to(ROOT)} and report.html with noindex")
