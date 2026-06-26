import csv
import json
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)

tickets = [
    {"id": 1, "category": "setup", "hours": 1.5, "resolved": True},
    {"id": 2, "category": "python", "hours": 2.0, "resolved": True},
    {"id": 3, "category": "python", "hours": 3.5, "resolved": False},
    {"id": 4, "category": "database", "hours": 4.0, "resolved": False},
    {"id": 5, "category": "setup", "hours": 1.0, "resolved": True},
]

category_hours = {}
for ticket in tickets:
    category = ticket["category"]
    category_hours[category] = category_hours.get(category, 0) + ticket["hours"]

open_tickets = [ticket for ticket in tickets if not ticket["resolved"]]

csv_path = RESULTS / "week4_ticket_summary.csv"
with csv_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["category", "hours"])
    for category, hours in sorted(category_hours.items()):
        writer.writerow([category, hours])

result = {
    "ticket_count": len(tickets),
    "open_ticket_count": len(open_tickets),
    "category_hours": category_hours,
    "summary_csv": str(csv_path),
}

(RESULTS / "week4_consolidation_results.json").write_text(
    json.dumps(result, indent=2),
    encoding="utf-8",
)

print(json.dumps(result, indent=2))
