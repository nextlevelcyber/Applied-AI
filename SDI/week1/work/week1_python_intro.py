import json
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)

student = {
    "module": "Software for Digital Innovation",
    "week": 1,
    "topic": "Python introduction",
}

temperatures = [12.5, 14.0, 13.2, 15.1, 11.9]
average_temperature = sum(temperatures) / len(temperatures)

message = (
    f"{student['module']} Week {student['week']} covers "
    f"{student['topic']}."
)

result = {
    "message": message,
    "temperature_count": len(temperatures),
    "average_temperature": round(average_temperature, 2),
    "highest_temperature": max(temperatures),
    "lowest_temperature": min(temperatures),
}

(RESULTS / "week1_python_intro_results.json").write_text(
    json.dumps(result, indent=2),
    encoding="utf-8",
)

print(json.dumps(result, indent=2))
