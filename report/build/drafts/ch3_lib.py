"""Helpers that turn a focus-area record into Chapter 3 content blocks (six-part template).

Each entry: kicker, h3 focus-area name, lead topline, then the five h4 parts
(Hypothesis and disposition; Evidence; Recommendation; Benchmark precedent; Link forward).
"""
import json
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'ch3')

EVIDENCE_COLS = [
    {"header": "Finding", "width": 2.2, "align": "left"},
    {"header": "Figure", "width": 4.0, "align": "left"},
    {"header": "Source", "width": 1.6, "align": "left"},
]
ACTION_COLS = [
    {"header": "Who acts", "width": 1.2, "align": "left"},
    {"header": "Action", "width": 4.6, "align": "left"},
    {"header": "Lead and partners", "width": 2.0, "align": "left"},
]


def theme(number, name, paras, pagebreak=True):
    blocks = [{"type": "pagebreak"}] if pagebreak else []
    blocks.append({"type": "h3", "text": f"{number} {name}"})
    blocks += [{"type": "p", "text": t} for t in paras]
    return blocks


def entry(fa, pagebreak=True):
    b = [{"type": "pagebreak"}] if pagebreak else []
    b.append({"type": "kicker", "text": fa["kicker"]})
    b.append({"type": "h3", "text": fa["name"]})
    b.append({"type": "lead", "text": fa["topline"]})
    b.append({"type": "h4", "text": "Hypothesis and disposition"})
    b += [{"type": "p", "text": t} for t in fa["hypothesis"]]
    b.append({"type": "h4", "text": "Evidence"})
    b += [{"type": "p", "text": t} for t in fa.get("evidence_intro", [])]
    b.append({"type": "table", "caption": fa["evidence_caption"], "source": fa["evidence_source"],
              "columns": EVIDENCE_COLS, "rows": fa["evidence_rows"], "boldFirstCol": True})
    b += fa.get("evidence_figures", [])
    b += [{"type": "p", "text": t} for t in fa.get("evidence_after", [])]
    b.append({"type": "h4", "text": "Recommendation"})
    b += [{"type": "p", "text": t} for t in fa["recommendation"]]
    b.append({"type": "grid", "columns": ACTION_COLS, "rows": fa["actions"]})
    b.append({"type": "h4", "text": "Benchmark precedent"})
    b.append({"type": "p", "text": fa["benchmark"]})
    b.append({"type": "h4", "text": "Link forward"})
    b.append({"type": "p", "text": fa["link"]})
    return b


def write(filename, section_id, title, blocks):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, filename)
    with open(path, 'w') as f:
        json.dump({"id": section_id, "title": title, "blocks": blocks}, f, indent=1, ensure_ascii=False)
        f.write('\n')
    return path
