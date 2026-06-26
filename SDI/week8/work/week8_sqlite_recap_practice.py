import sqlite3
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)
DB_PATH = RESULTS / "week8_recap_practice.db"
SUMMARY_PATH = RESULTS / "week8_sqlite_recap_summary.txt"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS departments")
    cursor.execute("DROP TABLE IF EXISTS projects")
    cursor.execute(
        """
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY,
            department_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            budget REAL NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
        """
    )
    cursor.executemany(
        "INSERT INTO departments VALUES (?, ?)",
        [(1, "Operations"), (2, "Analytics"), (3, "Support")],
    )
    cursor.executemany(
        "INSERT INTO projects VALUES (?, ?, ?, ?)",
        [
            (1, 1, "Workflow review", 15000),
            (2, 2, "Dashboard pilot", 22000),
            (3, 2, "Data quality review", 12000),
            (4, 3, "Helpdesk triage", 9000),
        ],
    )

    rows = cursor.execute(
        """
        SELECT d.name, COUNT(p.id) AS project_count, SUM(p.budget) AS total_budget
        FROM departments AS d
        LEFT JOIN projects AS p ON d.id = p.department_id
        GROUP BY d.id, d.name
        ORDER BY d.name
        """
    ).fetchall()

lines = ["Department project summary"]
for name, project_count, total_budget in rows:
    lines.append(f"{name}: {project_count} projects, budget {total_budget:.2f}")

SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
