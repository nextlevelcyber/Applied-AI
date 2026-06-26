import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "L7-students" / "CIS4044-N-Example.db"
RESULTS_PATH = Path(__file__).resolve().parents[1] / "results" / "student_average_marks.txt"


query = """
SELECT
    s.id,
    s.first_name,
    s.last_name,
    AVG(sm.mark) AS average_mark
FROM students AS s
JOIN "students-modules" AS sm
    ON s.id = sm.student_id
GROUP BY s.id, s.first_name, s.last_name
ORDER BY s.id;
"""

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    rows = conn.execute(query).fetchall()

lines = [
    f"{row['id']} {row['first_name']} {row['last_name']}: {row['average_mark']:.2f}"
    for row in rows
]

RESULTS_PATH.parent.mkdir(exist_ok=True)
RESULTS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
