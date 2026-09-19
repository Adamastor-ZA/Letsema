#!/usr/bin/env python3
"""
Build the EY response to Conservation International RFP 0032026.

Reads the Markdown working files in ./proposal, renders them through the EY
stylesheet in ./assets/ey.css and writes submission PDFs to ./build.

    python3 scripts/build.py            # build both documents
    python3 scripts/build.py technical  # build one

Edit the Markdown, re-run, re-check with scripts/qa.py. Nothing else is needed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import markdown
import yaml
from weasyprint import HTML, CSS

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
BUILD = ROOT / "build"

DOCS = {
    "technical": {
        "src": ROOT / "proposal" / "technical" / "technical_proposal.md",
        "out": BUILD / "EY_Technical_Proposal_CI_RFP_0032026.pdf",
        "html": BUILD / "technical_proposal.html",
        "body_page_cap": 5,
    },
    "cost": {
        "src": ROOT / "proposal" / "cost" / "cost_proposal.md",
        "out": BUILD / "EY_Cost_Proposal_CI_RFP_0032026.pdf",
        "html": BUILD / "cost_proposal.html",
        "body_page_cap": None,
    },
}

MD_EXTENSIONS = ["tables", "attr_list", "md_in_html", "def_list", "sane_lists"]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>{title}</title>
</head>
<body>
<section class="masthead" data-doctitle="{running_head}">
  <div class="logo-slot">EY LOGO</div>
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}</h1>
  <div class="subtitle">{subtitle}</div>
  <div class="meta">{meta}</div>
</section>
{body}
</body>
</html>
"""


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta = yaml.safe_load(text[3:end]) or {}
    return meta, text[end + 4 :].lstrip("\n")


def render_meta_line(meta: dict) -> str:
    parts = []
    for item in meta.get("meta", []):
        label, value = next(iter(item.items()))
        parts.append(f"<span><b>{label}</b> {value}</span>")
    return "".join(parts)


def mark_placeholders(html: str) -> str:
    """Wrap [[TO CONFIRM: ...]] so it is impossible to miss on the page."""
    return re.sub(
        r"\[\[TO CONFIRM:(.+?)\]\]",
        lambda m: '<span class="todo">[[TO CONFIRM:' + m.group(1) + "]]</span>",
        html,
        flags=re.S,
    )


# Matches a bare figure, a currency figure, a percentage or a range such as
# "3-5", so that a Weeks column aligns consistently with a Days column.
NUMERIC_CELL = re.compile(
    r"^(?:US\$|\$)?\s?-?[\d][\d,\.\s]*(?:-\s?\d[\d,\.]*)?"
    r"(?:%|k|m|bn|\s?days?|\s?wks?)?$", re.I
)


def _is_numeric(inner: str) -> bool:
    """True if a cell holds only a figure, ignoring any inline markup."""
    plain = re.sub(r"<[^>]+>", "", inner).strip()
    return bool(plain) and bool(NUMERIC_CELL.match(plain))


def align_numeric_cells(html: str) -> str:
    """Right-align table cells that hold a figure, a percentage or a day count."""

    def cell(m):
        tag, inner = m.group(1), m.group(2)
        if _is_numeric(inner):
            return f'<{tag} class="num">{inner}</{tag}>'
        return m.group(0)

    html = re.sub(r"<(td|th)>(.*?)</\1>", cell, html, flags=re.S)

    head = re.compile(
        r"<th>\s*((?:<[^>]+>)*\s*(?:US\$[^<]*|Total[^<]*|Days[^<]*|Rate[^<]*"
        r"|%[^<]*|Amount[^<]*|Qty[^<]*|Unit price[^<]*|Week|Share[^<]*)\s*(?:</[^>]+>)*)\s*</th>",
        re.I,
    )
    return head.sub(lambda m: f'<th class="num">{m.group(1)}</th>', html)


def tag_rows(html: str) -> str:
    """Promote rows whose first cell starts with TOTAL or SUBTOTAL."""
    def repl(m):
        row = m.group(0)
        first = re.search(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
        if not first:
            return row
        label = re.sub(r"<[^>]+>", "", first.group(1)).strip().lower()
        if label.startswith("total") or label.startswith("grand total"):
            return row.replace("<tr>", '<tr class="total">', 1)
        if label.startswith("subtotal"):
            return row.replace("<tr>", '<tr class="subtotal">', 1)
        return row

    return re.sub(r"<tr>.*?</tr>", repl, html, flags=re.S)


def build(key: str) -> tuple[int, int | None]:
    spec = DOCS[key]
    src: Path = spec["src"]
    if not src.exists():
        raise SystemExit(f"missing source: {src}")

    meta, body_md = split_front_matter(src.read_text(encoding="utf-8"))

    body_html = markdown.markdown(body_md, extensions=MD_EXTENSIONS)
    body_html = align_numeric_cells(body_html)
    body_html = tag_rows(body_html)
    body_html = mark_placeholders(body_html)

    page = PAGE_TEMPLATE.format(
        title=meta.get("title", ""),
        running_head=meta.get("running_head", meta.get("title", "")),
        eyebrow=meta.get("eyebrow", ""),
        subtitle=meta.get("subtitle", ""),
        meta=render_meta_line(meta),
        body=body_html,
    )

    # Placeholders can appear in the front matter as well as the body.
    page = mark_placeholders(page)

    BUILD.mkdir(exist_ok=True)
    spec["html"].write_text(page, encoding="utf-8")

    doc = HTML(string=page, base_url=str(ROOT)).render(
        stylesheets=[CSS(filename=str(ASSETS / "ey.css"))]
    )
    doc.write_pdf(spec["out"])

    total = len(doc.pages)
    body_pages = count_body_pages(spec["html"])
    return total, body_pages


def count_body_pages(html_path: Path) -> int | None:
    """Pages before the first annex, computed by rendering the body alone."""
    html = html_path.read_text(encoding="utf-8")
    idx = html.find('<div class="annex-start"')
    if idx == -1:
        idx = html.find('<section class="annex-start"')
    if idx == -1:
        return None
    body_only = html[:idx] + "</body></html>"
    doc = HTML(string=body_only, base_url=str(ROOT)).render(
        stylesheets=[CSS(filename=str(ASSETS / "ey.css"))]
    )
    return len(doc.pages)


def main() -> None:
    keys = sys.argv[1:] or list(DOCS)
    for key in keys:
        if key not in DOCS:
            raise SystemExit(f"unknown document '{key}'; choose from {list(DOCS)}")
        total, body = build(key)
        cap = DOCS[key]["body_page_cap"]
        line = f"{key:<10} {DOCS[key]['out'].name}  {total} pages total"
        if body is not None:
            flag = "OK" if cap is None or body <= cap else f"OVER CAP ({cap})"
            line += f", body {body} pages  [{flag}]"
        print(line)


if __name__ == "__main__":
    main()
