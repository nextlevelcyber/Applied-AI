import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "CIS4044-N-ICA(1)" / "db" / "CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
RESULTS_PATH = Path(__file__).resolve().parents[1] / "results" / "schema_summary.txt"


def describe_database(db_path: Path) -> str:
    lines = [f"Database: {db_path.name}"]
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            lines.append("")
            lines.append(f"Table: {table}")
            lines.append(f"Rows: {row_count}")
            lines.append("Columns: " + ", ".join(column[1] for column in columns))

    return "\n".join(lines) + "\n"


summary = describe_database(DB_PATH)
RESULTS_PATH.parent.mkdir(exist_ok=True)
RESULTS_PATH.write_text(summary, encoding="utf-8")
print(summary)
