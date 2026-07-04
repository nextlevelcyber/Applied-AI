"""Common helpers."""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "db" / "CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
DEFAULT_CHART_DIR = PROJECT_ROOT / "charts"


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class City:
    """Small data object used by Phase 3 when requesting weather data."""

    id: int
    name: str
    latitude: float
    longitude: float
    timezone: str


def connect_database(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open a SQLite connection configured for named-column access."""

    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Database file not found: {path}")

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def validate_date(value: str, field_name: str = "date") -> str:
    """Validate an ISO date string and return it unchanged."""

    if not isinstance(value, str) or not DATE_PATTERN.match(value):
        raise ValueError(f"{field_name} must use YYYY-MM-DD format")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field_name} is not a valid calendar date") from exc
    return value


def validate_date_range(date_from: str, date_to: str) -> tuple[str, str]:
    """Validate an inclusive ISO date range."""

    start = validate_date(date_from, "date_from")
    end = validate_date(date_to, "date_to")
    if start > end:
        raise ValueError("date_from must be before or equal to date_to")
    return start, end


def validate_year(year: int | str) -> int:
    """Validate a four-digit year used by the historical database."""

    try:
        value = int(year)
    except (TypeError, ValueError) as exc:
        raise ValueError("year must be an integer") from exc

    if value < 1900 or value > 2100:
        raise ValueError("year must be between 1900 and 2100")
    return value


def fetch_all(connection: sqlite3.Connection, query: str, params: Sequence = ()) -> list[sqlite3.Row]:
    """Execute a SELECT query and return all rows."""

    return list(connection.execute(query, params))


def print_table(rows: Iterable[sqlite3.Row], columns: Sequence[tuple[str, str]]) -> None:
    """Print rows using display labels and row keys."""

    rows = list(rows)
    if not rows:
        print("No records found.")
        return

    for row in rows:
        parts = []
        for label, key in columns:
            value = row[key]
            if isinstance(value, float):
                value = f"{value:.2f}"
            parts.append(f"{label}: {value}")
        print(" -- ".join(parts))


def get_city(connection: sqlite3.Connection, city_id: int) -> City:
    """Return city details including country timezone for a city id."""

    row = connection.execute(
        """
        SELECT c.id, c.name, c.latlong, countries.timezone
        FROM cities AS c
        JOIN countries ON countries.id = c.country_id
        WHERE c.id = ?
        """,
        (city_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"Unknown city_id: {city_id}")

    try:
        latitude_text, longitude_text = row["latlong"].split(",", 1)
        latitude = float(latitude_text)
        longitude = float(longitude_text)
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"City {row['name']} has invalid latlong data") from exc

    return City(
        id=row["id"],
        name=row["name"],
        latitude=latitude,
        longitude=longitude,
        timezone=row["timezone"],
    )
