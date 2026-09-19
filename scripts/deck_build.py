#!/usr/bin/env python3
"""
Build the PowerPoint versions of the EY response to CI RFP 0032026.

Two decks, mirroring the two submission PDFs and kept as separate files for
the same reason: the technical proposal is evaluated first and separately, so
no price, rate or fee may appear in it.

    python3 scripts/deck_build.py              # build both
    python3 scripts/deck_build.py technical    # build one

Both start from the bundled EY master template in assets/pptx. Structural work
(duplicating the template slides each deck needs, then setting the slide order)
happens first and in the package; content is filled afterwards with python-pptx.
That order matters: duplicating a slide after editing it clones the edit.

The deck content lives in scripts/deck_content.py.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "assets" / "pptx" / "ey-master-template.pptx"
BUILD = ROOT / "build"
WORK = ROOT / "build" / "deck-work"
ADD_SLIDE = Path("/mnt/skills/public/pptx/scripts/add_slide.py")
CLEAN = Path("/mnt/skills/public/pptx/scripts/clean.py")

# EY palette, from the template theme. Used only where a value must be written
# explicitly; everything else inherits from the layout.
EY_YELLOW = "FFE600"
EY_BLACK = "1A1A24"
EY_GREY_01 = "747480"

FOOTER = "Draft, not for distribution"
DECK_DATE = "19 September 2026"

# Guidance text boxes the template ships on some example slides. They carry no
# placeholder, so they survive duplication and have to be removed by content.
GUIDANCE_MARKERS = (
    "Copying legacy content",
    "REMOVE THIS SLIDE",
    "Add a background image",
    "For slides 9-16",
)


# ----------------------------------------------------------------- structure ---

def unpack(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(src) as z:
        z.extractall(dest)


def slide_rid_map(unpacked: Path) -> dict[str, str]:
    """slideN.xml -> rId, from the presentation relationships."""
    rels = (unpacked / "ppt" / "_rels" / "presentation.xml.rels").read_text(encoding="utf-8")
    return {
        slide: rid
        for rid, slide in re.findall(
            r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels
        )
    }


def duplicate(unpacked: Path, source: str) -> str:
    """Duplicate a template slide and return the new slideN.xml name."""
    out = subprocess.run(
        [sys.executable, str(ADD_SLIDE), str(unpacked), source],
        capture_output=True, text=True, check=True,
    ).stdout
    m = re.search(r"(slide\d+\.xml)\s+from", out)
    if not m:
        raise SystemExit(f"add_slide.py gave no new slide name:\n{out}")
    return m.group(1)


def set_order(unpacked: Path, slides: list[str]) -> None:
    """Rewrite <p:sldIdLst> to exactly these slides, in this order."""
    rids = slide_rid_map(unpacked)
    missing = [s for s in slides if s not in rids]
    if missing:
        raise SystemExit(f"no relationship for: {missing}")
    entries = "".join(
        f'<p:sldId id="{256 + i}" r:id="{rids[s]}"/>' for i, s in enumerate(slides)
    )
    path = unpacked / "ppt" / "presentation.xml"
    xml = path.read_text(encoding="utf-8")
    xml = re.sub(
        r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{entries}</p:sldIdLst>", xml, flags=re.S
    )
    path.write_text(xml, encoding="utf-8")


def pack(unpacked: Path, out: Path) -> None:
    subprocess.run([sys.executable, str(CLEAN), str(unpacked)], check=True,
                   capture_output=True)
    if out.exists():
        out.unlink()
    subprocess.run(["zip", "-Xrq", str(out.resolve()), "."], cwd=unpacked, check=True)


def build_skeleton(plan: list[dict], out: Path) -> None:
    """Duplicate what the plan needs, set the order, and pack."""
    work = WORK / out.stem
    unpack(TEMPLATE, work)

    used: dict[str, int] = {}
    order: list[str] = []
    for spec in plan:
        base = spec["base"]
        used[base] = used.get(base, 0) + 1
        order.append(base if used[base] == 1 else duplicate(work, base))

    set_order(work, order)
    pack(work, out)


# ------------------------------------------------------------------- content ---

def placeholder(slide, idx: int):
    for shape in slide.shapes:
        if shape.is_placeholder and shape.placeholder_format.idx == idx:
            return shape
    return None


def by_name(slide, needle: str):
    for shape in slide.shapes:
        if needle.lower() in shape.name.lower():
            return shape
    return None


def strip_guidance(slide) -> None:
    for shape in list(slide.shapes):
        if shape.has_text_frame and any(m in shape.text_frame.text for m in GUIDANCE_MARKERS):
            shape._element.getparent().remove(shape._element)


def set_runs(shape, text: str) -> None:
    """Replace a placeholder's text, keeping the first run's formatting."""
    tf = shape.text_frame
    para = tf.paragraphs[0]
    if para.runs:
        para.runs[0].text = text
        for extra in para.runs[1:]:
            extra._r.getparent().remove(extra._r)
    else:
        para.text = text
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)


def highlight_if_placeholder(run) -> None:
    """Mark [[TO CONFIRM: ...]] in EY Yellow, as the two PDFs do.

    Yellow highlights rather than decorates, which is exactly the job here:
    an unresolved input is the thing a reviewer must see.
    """
    if "[[TO CONFIRM" not in run.text:
        return
    from pptx.oxml.ns import qn

    rPr = run._r.get_or_add_rPr()
    hl = rPr.makeelement(qn("a:highlight"), {})
    clr = rPr.makeelement(qn("a:srgbClr"), {"val": EY_YELLOW})
    hl.append(clr)
    rPr.append(hl)


def no_bullet(para) -> None:
    """Suppress the layout's bullet on one paragraph."""
    from pptx.oxml.ns import qn

    pPr = para._p.get_or_add_pPr()
    for tag in ("a:buChar", "a:buAutoNum", "a:buNone"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    pPr.append(pPr.makeelement(qn("a:buNone"), {}))


def set_body(shape, lines: list, *, size: int | None = None,
             space_after: int = 6) -> None:
    """Fill a body placeholder.

    Each line is either a string at level 0, or a (level, text) pair. An empty
    placeholder inherits its font and bullet from the layout by level, which is
    how the EY template is built to work, so nothing is styled here beyond an
    optional size override for dense slides.
    """
    tf = shape.text_frame
    tf.word_wrap = True
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    first = tf.paragraphs[0]
    for run in list(first.runs):
        run._r.getparent().remove(run._r)

    for i, line in enumerate(lines):
        level, text = line if isinstance(line, tuple) else ("t", line)
        para = first if i == 0 else tf.add_paragraph()
        # "t" is the topline and "h" a column heading. Neither takes a bullet:
        # the topline is the slide's thesis, not one item among several.
        para.level = 0 if level in ("t", "h") else level
        if level in ("t", "h"):
            no_bullet(para)
        run = para.add_run()
        run.text = text
        run.font.bold = level == "h"
        if size:
            run.font.size = Pt(size)
        highlight_if_placeholder(run)
        para.space_after = Pt(space_after)


def add_source(slide, text: str) -> None:
    """Source citation, 8pt EY Grey 01, bottom left, as the brand requires."""
    from pptx.dml.color import RGBColor

    box = slide.shapes.add_textbox(Inches(0.53), Inches(6.72), Inches(12.28), Inches(0.28))
    box.name = "Source citation"
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    run = tf.paragraphs[0].add_run()
    run.text = text
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor.from_string(EY_GREY_01)


def set_chrome(slide) -> None:
    """Footer and date, where the layout carries them."""
    for idx_name, value in (("FOOTER", FOOTER), ("DATE", DECK_DATE)):
        for shape in slide.shapes:
            if not shape.is_placeholder:
                continue
            if str(shape.placeholder_format.type).startswith(idx_name):
                set_runs(shape, value)


def fit_table(shape, rows: int, cols: int, widths: list[float]) -> None:
    """Trim the template's 10x13 table to size and set column widths."""
    table = shape.table
    tbl = table._tbl
    for tr in list(tbl.findall(".//{*}tr"))[rows:]:
        tbl.remove(tr)
    grid = tbl.find("{*}tblGrid")
    for gc in list(grid)[cols:]:
        grid.remove(gc)
    for tr in tbl.findall(".//{*}tr"):
        for tc in list(tr.findall("{*}tc"))[cols:]:
            tr.remove(tc)
    total = sum(widths)
    for col, w in zip(table.columns, widths):
        col.width = Emu(int(12.28 * 914400 * w / total))
    # A small nominal height; PowerPoint grows a row to fit its wrapped text.
    for i, row in enumerate(table.rows):
        row.height = Inches(0.34 if i else 0.30)


def fill_table(shape, data: list[list[str]], size: int = 11,
               aligns: list[str] | None = None) -> None:
    """Fill a table, writing the text colour explicitly.

    The template's cells inherit `schemeClr val="dk1"`, and masters 1 to 3 swap
    dk1 and lt1, so an inherited body run renders white on a white cell and
    disappears. Every run therefore carries an explicit EY Confident Black.
    """
    from pptx.dml.color import RGBColor
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

    table = shape.table
    for r, row in enumerate(data):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.07)
            cell.margin_top = cell.margin_bottom = Inches(0.045)
            cell.vertical_anchor = MSO_ANCHOR.TOP if r else MSO_ANCHOR.BOTTOM
            tf = cell.text_frame
            tf.word_wrap = True
            for extra in tf.paragraphs[1:]:
                extra._p.getparent().remove(extra._p)
            para = tf.paragraphs[0]
            for run in list(para.runs):
                run._r.getparent().remove(run._r)
            para.alignment = (
                PP_ALIGN.RIGHT if aligns and aligns[c] == "r" else PP_ALIGN.LEFT
            )
            run = para.add_run()
            run.text = value
            run.font.size = Pt(size)
            run.font.bold = r == 0 or value.lower().startswith("total")
            run.font.color.rgb = RGBColor.from_string(EY_BLACK)
            highlight_if_placeholder(run)


# -------------------------------------------------------------- slide kinds ---

def fill_cover(slide, spec) -> None:
    strip_guidance(slide)
    title = placeholder(slide, 0)
    set_runs(title, spec["title"])
    if spec.get("title_size"):
        for run in title.text_frame.paragraphs[0].runs:
            run.font.size = Pt(spec["title_size"])
    set_runs(placeholder(slide, 1), spec["subtitle"])
    body = placeholder(slide, 10)
    if body is not None:
        set_runs(body, spec.get("date", DECK_DATE))


def fill_section(slide, spec) -> None:
    strip_guidance(slide)
    set_runs(placeholder(slide, 0), spec["title"])
    eyebrow = placeholder(slide, 13)
    if eyebrow is not None:
        set_runs(eyebrow, spec.get("eyebrow", ""))
    set_chrome(slide)


def fill_contents(slide, spec) -> None:
    strip_guidance(slide)
    set_runs(placeholder(slide, 0), spec["title"])
    set_body(placeholder(slide, 15), spec["left"], size=spec.get("size"))
    set_body(placeholder(slide, 21), spec["right"], size=spec.get("size"))
    set_chrome(slide)


def fill_content(slide, spec) -> None:
    strip_guidance(slide)
    set_runs(placeholder(slide, 0), spec["title"])
    set_body(placeholder(slide, 16), spec["body"], size=spec.get("size"))
    if spec.get("source"):
        add_source(slide, spec["source"])
    set_chrome(slide)


def fill_columns(slide, spec) -> None:
    strip_guidance(slide)
    set_runs(placeholder(slide, 0), spec["title"])
    for idx, column in zip(spec["idx"], spec["columns"]):
        set_body(placeholder(slide, idx), column, size=spec.get("size"))
    if spec.get("source"):
        add_source(slide, spec["source"])
    set_chrome(slide)


def fill_keynumbers(slide, spec) -> None:
    strip_guidance(slide)
    set_runs(placeholder(slide, 0), spec["title"])
    for idx, (number, _) in zip((13, 14, 15), spec["numbers"]):
        set_body(placeholder(slide, idx), [number], size=spec.get("number_size"))
    for idx, (_, caption) in zip((16, 17, 18), spec["numbers"]):
        set_body(placeholder(slide, idx), [caption], size=spec.get("size"))
    if spec.get("source"):
        add_source(slide, spec["source"])
    set_chrome(slide)


def fill_statement(slide, spec) -> None:
    strip_guidance(slide)
    for shape in slide.shapes:
        if shape.is_placeholder and shape.has_text_frame and shape.text_frame.text:
            if str(shape.placeholder_format.type).startswith("TITLE"):
                set_runs(shape, spec["text"])
                if spec.get("size"):
                    for run in shape.text_frame.paragraphs[0].runs:
                        run.font.size = Pt(spec["size"])
    set_chrome(slide)


def fill_table_slide(slide, spec) -> None:
    strip_guidance(slide)
    set_runs(placeholder(slide, 0), spec["title"])
    shape = next(s for s in slide.shapes if s.has_table)
    data = spec["table"]
    fit_table(shape, len(data), len(data[0]), spec["widths"])
    fill_table(shape, data, size=spec.get("size", 11), aligns=spec.get("aligns"))
    if spec.get("source"):
        add_source(slide, spec["source"])
    set_chrome(slide)


# Runs on the template boilerplate that must be filled, matched on their own
# text. The member firm name and the document codes cannot be invented, so they
# carry the same placeholder marker as the two PDFs.
BOILERPLATE_RUNS = [
    ("Optional sector or service line descriptor", "descriptor"),
    ("© 2024 [member firm name]", "copyright"),
    ("XXXXX-", "doc_code"),
    ("XXXGbl", None),
    ("ED MMYY", "ed_code"),
    ("Optional environmental statement", None),
    ("Required legal disclaimer", None),
]


def fill_boilerplate(slide, spec) -> None:
    strip_guidance(slide)
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                for marker, key in BOILERPLATE_RUNS:
                    if marker in run.text:
                        run.text = spec[key] if key else ""
                        break


FILLERS = {
    "cover": fill_cover,
    "section": fill_section,
    "contents": fill_contents,
    "content": fill_content,
    "columns": fill_columns,
    "keynumbers": fill_keynumbers,
    "statement": fill_statement,
    "table": fill_table_slide,
    "boilerplate": fill_boilerplate,
}


def fill(out: Path, plan: list[dict]) -> None:
    prs = Presentation(str(out))
    for slide, spec in zip(prs.slides, plan):
        FILLERS[spec["kind"]](slide, spec)
    prs.save(str(out))


# ---------------------------------------------------------------------- main ---

def build(name: str, plan: list[dict], out: Path) -> None:
    BUILD.mkdir(exist_ok=True)
    build_skeleton(plan, out)
    fill(out, plan)
    prs = Presentation(str(out))
    print(f"{name:<10} {out.name}  {len(prs.slides)} slides")


def main() -> None:
    from deck_content import DECKS

    wanted = sys.argv[1:] or list(DECKS)
    sys.setrecursionlimit(10000)
    for key in wanted:
        if key not in DECKS:
            raise SystemExit(f"unknown deck '{key}'; choose from {list(DECKS)}")
        deck = DECKS[key]
        build(key, deck["plan"], BUILD / deck["file"])


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
