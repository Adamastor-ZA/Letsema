#!/usr/bin/env python3
"""
Collect workflow agent results out of the run journal into work/analysis/*.json.

    python3 scripts/collect_analysis.py <workflow-run-dir>

Results are identified by the shape of the object each agent returned, because
the journal keys agents by content hash rather than by label.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "analysis"

# A distinctive top-level key from each workstream's schema.
SHAPES = {
    "rows": "compliance",
    "approachName": "method",
    "framingNote": "models",
    "effortModel": "cost",
    "scoringInsight": "credentials",
    "criteria": "evaluator",
    "checkpoints": "governance",
    "items": "gaps",
}


def main() -> None:
    journal = Path(sys.argv[1]) / "journal.jsonl"
    OUT.mkdir(parents=True, exist_ok=True)
    reviews = []
    saved = []
    for line in journal.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        if entry.get("type") != "result":
            continue
        result = entry.get("result")
        if not isinstance(result, dict):
            continue
        if "analysis" in result and "review" in result:
            reviews.append(result)
            continue
        for key, name in SHAPES.items():
            if key in result:
                (OUT / f"{name}.json").write_text(
                    json.dumps(result, indent=1), encoding="utf-8"
                )
                saved.append(name)
                break
    if reviews:
        (OUT / "reviews.json").write_text(json.dumps(reviews, indent=1), encoding="utf-8")
        saved.append(f"reviews({len(reviews)})")
    print("collected:", ", ".join(sorted(saved)) or "nothing")


if __name__ == "__main__":
    main()
