import json
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)


def classify_mark(mark):
    if mark < 0 or mark > 100:
        return "invalid"
    if mark >= 70:
        return "distinction"
    if mark >= 60:
        return "merit"
    if mark >= 50:
        return "pass"
    return "refer"


marks = [82, 64, 58, 47, 101, -5]
classified = [{"mark": mark, "classification": classify_mark(mark)} for mark in marks]
valid_marks = [item["mark"] for item in classified if item["classification"] != "invalid"]

result = {
    "classified_marks": classified,
    "valid_count": len(valid_marks),
    "valid_average": round(sum(valid_marks) / len(valid_marks), 2),
}

(RESULTS / "week2_flow_control_results.json").write_text(
    json.dumps(result, indent=2),
    encoding="utf-8",
)

print(json.dumps(result, indent=2))
