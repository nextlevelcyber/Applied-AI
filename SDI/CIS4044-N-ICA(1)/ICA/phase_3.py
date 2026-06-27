"""Phase 3: retrieve Open-Meteo data and store it in SQLite."""

from __future__ import annotations

import sqlite3
from typing import Any

try:
    from .common import DEFAULT_DB_PATH, connect_database, get_city, validate_date, validate_date_range
except ImportError:
    from common import DEFAULT_DB_PATH, connect_database, get_city, validate_date, validate_date_range  # type: ignore


ARCHIVE_API_URL = "https://archive-api.open-meteo.com/v1/archive"


class WeatherApiError(RuntimeError):
    """Raised when Open-Meteo cannot provide usable weather data."""


def build_archive_params(city, start_date: str, end_date: str) -> dict[str, Any]:
    """Build Open-Meteo archive API parameters for one city."""

    start_date, end_date = validate_date_range(start_date, end_date)
    return {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_min,temperature_2m_max,temperature_2m_mean,precipitation_sum",
        "timezone": city.timezone,
    }


def fetch_open_meteo_archive(city, start_date: str, end_date: str, timeout: int = 20) -> dict[str, Any]:
    """Fetch daily weather data from Open-Meteo using a direct HTTP request."""

    import requests

    params = build_archive_params(city, start_date, end_date)
    try:
        response = requests.get(ARCHIVE_API_URL, params=params, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise WeatherApiError(f"Open-Meteo request failed: {exc}") from exc

    payload = response.json()
    if "daily" not in payload:
        reason = payload.get("reason", "daily weather data missing from response")
        raise WeatherApiError(reason)
    return payload


def parse_daily_weather(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert the Open-Meteo daily JSON block into rows for SQLite."""

    daily = payload.get("daily", {})
    required_keys = {
        "time",
        "temperature_2m_min",
        "temperature_2m_max",
        "temperature_2m_mean",
        "precipitation_sum",
    }
    missing_keys = required_keys.difference(daily)
    if missing_keys:
        raise WeatherApiError(f"Open-Meteo daily data missing keys: {', '.join(sorted(missing_keys))}")

    dates = daily.get("time", [])
    min_temps = daily.get("temperature_2m_min", [])
    max_temps = daily.get("temperature_2m_max", [])
    mean_temps = daily.get("temperature_2m_mean", [])
    precipitation = daily.get("precipitation_sum", [])
    lengths = {len(dates), len(min_temps), len(max_temps), len(mean_temps), len(precipitation)}
    if len(lengths) != 1:
        raise WeatherApiError("Open-Meteo daily arrays have inconsistent lengths")

    rows = []
    for index, date_value in enumerate(dates):
        rows.append(
            {
                "date": validate_date(date_value),
                "min_temp": float(min_temps[index]),
                "max_temp": float(max_temps[index]),
                "mean_temp": float(mean_temps[index]),
                "precipitation": float(precipitation[index]),
            }
        )
    return rows


def store_daily_weather(connection: sqlite3.Connection, city_id: int, weather_rows: list[dict[str, Any]]) -> int:
    """Store daily weather rows, replacing existing rows for the same city/date."""

    if not weather_rows:
        return 0

    with connection:
        for row in weather_rows:
            connection.execute(
                "DELETE FROM daily_weather_entries WHERE city_id = ? AND date = ?",
                (city_id, row["date"]),
            )
            connection.execute(
                """
                INSERT INTO daily_weather_entries
                    (date, min_temp, max_temp, mean_temp, precipitation, city_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row["date"],
                    row["min_temp"],
                    row["max_temp"],
                    row["mean_temp"],
                    row["precipitation"],
                    city_id,
                ),
            )
    return len(weather_rows)


def update_city_weather(connection: sqlite3.Connection, city_id: int, start_date: str, end_date: str) -> int:
    """Fetch Open-Meteo data for a known city and update the database."""

    city = get_city(connection, int(city_id))
    payload = fetch_open_meteo_archive(city, start_date, end_date)
    weather_rows = parse_daily_weather(payload)
    inserted = store_daily_weather(connection, city.id, weather_rows)
    print(f"Stored {inserted} weather rows for {city.name}.")
    return inserted


def add_city(connection: sqlite3.Connection, name: str, country_id: int, latitude: float, longitude: float) -> int:
    """Add a city so Phase 3 can request data for a wider area."""

    if not name.strip():
        raise ValueError("city name cannot be empty")
    with connection:
        cursor = connection.execute(
            "INSERT INTO cities (name, country_id, latlong) VALUES (?, ?, ?)",
            (name.strip(), int(country_id), f"{float(latitude)},{float(longitude)}"),
        )
    print(f"Added city {name.strip()} with id {cursor.lastrowid}.")
    return int(cursor.lastrowid)


if __name__ == "__main__":
    with connect_database(DEFAULT_DB_PATH) as conn:
        update_city_weather(conn, city_id=1, start_date="2024-01-01", end_date="2024-01-07")
