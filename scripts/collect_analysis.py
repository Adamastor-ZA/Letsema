#!/usr/bin/env python3
"""
Collect workflow agent results out of the run journal into work/analysis/*.json.

    python3 scripts/collect_analysis.py <workflow-run-dir>
    python3 scripts/collect_analysis.py <workflow-run-dir> --reviews-only

Pass --reviews-only once the analysis files carry hand-applied corrections,
so that re-collecting the adversarial reviews cannot overwrite them.

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
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    reviews_only = "--reviews-only" in sys.argv
    journal = Path(args[0]) / "journal.jsonl"
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
        # Stage-two verify agents log either the pipeline wrapper or, when the
        # stage returns the agent result directly, the verdict object itself.
        if "analysis" in result and "review" in result:
            reviews.append(result["review"] | {"workstream": result.get("key", "?")})
            continue
        if "verdict" in result and "defects" in result:
            reviews.append(result)
            continue
        if reviews_only:
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
