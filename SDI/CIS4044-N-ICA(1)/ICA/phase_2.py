"""Phase 2: Matplotlib charts generated from SQLite weather data."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(os.getenv("TMPDIR", "/tmp")) / "cis4044_matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from .common import (
        DEFAULT_CHART_DIR,
        DEFAULT_DB_PATH,
        connect_database,
        fetch_all,
        validate_date,
        validate_date_range,
        validate_year,
    )
except ImportError:
    from common import (  # type: ignore
        DEFAULT_CHART_DIR,
        DEFAULT_DB_PATH,
        connect_database,
        fetch_all,
        validate_date,
        validate_date_range,
        validate_year,
    )


def _prepare_output(output_path: Path | str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _save_chart(output_path: Path | str) -> Path:
    path = _prepare_output(output_path)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Chart saved: {path}")
    return path


def plot_seven_day_precipitation(connection, city_id, start_date, output_path=None):
    """Create a bar chart showing daily precipitation for one city over 7 days."""

    start_date = validate_date(start_date, "start_date")
    output_path = output_path or DEFAULT_CHART_DIR / f"city_{city_id}_7_day_precipitation.png"
    rows = fetch_all(
        connection,
        """
        SELECT dwe.date, dwe.precipitation, cities.name AS city_name
        FROM daily_weather_entries AS dwe
        JOIN cities ON cities.id = dwe.city_id
        WHERE dwe.city_id = ?
          AND dwe.date BETWEEN ? AND date(?, '+6 day')
        ORDER BY dwe.date
        """,
        (city_id, start_date, start_date),
    )
    if not rows:
        raise ValueError("No weather records found for the requested city/date range")

    plt.figure(figsize=(9, 5))
    plt.bar([row["date"][5:] for row in rows], [row["precipitation"] for row in rows], color="#2f6f8f")
    plt.title(f"7-Day Precipitation for {rows[0]['city_name']} from {start_date}")
    plt.xlabel("Date")
    plt.ylabel("Precipitation (mm)")
    plt.grid(axis="y", alpha=0.3)
    return _save_chart(output_path)


def plot_precipitation_for_cities(connection, city_ids, date_from, date_to, output_path=None):
    """Create a comparison bar chart for selected cities over a date range."""

    city_ids = [int(city_id) for city_id in city_ids]
    if not city_ids:
        raise ValueError("at least one city id is required")
    date_from, date_to = validate_date_range(date_from, date_to)
    placeholders = ",".join("?" for _ in city_ids)
    output_path = output_path or DEFAULT_CHART_DIR / "city_precipitation_comparison.png"
    rows = fetch_all(
        connection,
        f"""
        SELECT cities.name AS city_name,
               SUM(dwe.precipitation) AS total_precipitation
        FROM daily_weather_entries AS dwe
        JOIN cities ON cities.id = dwe.city_id
        WHERE dwe.city_id IN ({placeholders})
          AND dwe.date BETWEEN ? AND ?
        GROUP BY cities.id, cities.name
        ORDER BY cities.name
        """,
        (*city_ids, date_from, date_to),
    )
    if not rows:
        raise ValueError("No precipitation records found for the requested selection")

    plt.figure(figsize=(8, 5))
    plt.bar([row["city_name"] for row in rows], [row["total_precipitation"] for row in rows], color="#7a5c99")
    plt.title(f"Total Precipitation by City ({date_from} to {date_to})")
    plt.xlabel("City")
    plt.ylabel("Total precipitation (mm)")
    plt.grid(axis="y", alpha=0.3)
    return _save_chart(output_path)


def plot_average_yearly_precipitation_by_country(connection, year, output_path=None):
    """Create a country-level average precipitation bar chart for one year."""

    year = validate_year(year)
    output_path = output_path or DEFAULT_CHART_DIR / f"country_average_precipitation_{year}.png"
    rows = fetch_all(
        connection,
        """
        SELECT countries.name AS country_name,
               AVG(dwe.precipitation) AS average_precipitation
        FROM daily_weather_entries AS dwe
        JOIN cities ON cities.id = dwe.city_id
        JOIN countries ON countries.id = cities.country_id
        WHERE strftime('%Y', dwe.date) = ?
        GROUP BY countries.id, countries.name
        ORDER BY countries.name
        """,
        (str(year),),
    )
    if not rows:
        raise ValueError("No country precipitation records found for the requested year")

    plt.figure(figsize=(8, 5))
    plt.bar([row["country_name"] for row in rows], [row["average_precipitation"] for row in rows], color="#48785f")
    plt.title(f"Average Daily Precipitation by Country ({year})")
    plt.xlabel("Country")
    plt.ylabel("Average daily precipitation (mm)")
    plt.grid(axis="y", alpha=0.3)
    return _save_chart(output_path)


def plot_temperature_precipitation_grouped(connection, city_ids, date_from, date_to, output_path=None):
    """Create grouped bars for min/max/mean temperature and precipitation by city."""

    city_ids = [int(city_id) for city_id in city_ids]
    if not city_ids:
        raise ValueError("at least one city id is required")
    date_from, date_to = validate_date_range(date_from, date_to)
    placeholders = ",".join("?" for _ in city_ids)
    output_path = output_path or DEFAULT_CHART_DIR / "temperature_precipitation_grouped.png"
    rows = fetch_all(
        connection,
        f"""
        SELECT cities.name AS city_name,
               AVG(dwe.min_temp) AS min_temp,
               AVG(dwe.mean_temp) AS mean_temp,
               AVG(dwe.max_temp) AS max_temp,
               AVG(dwe.precipitation) AS precipitation
        FROM daily_weather_entries AS dwe
        JOIN cities ON cities.id = dwe.city_id
        WHERE dwe.city_id IN ({placeholders})
          AND dwe.date BETWEEN ? AND ?
        GROUP BY cities.id, cities.name
        ORDER BY cities.name
        """,
        (*city_ids, date_from, date_to),
    )
    if not rows:
        raise ValueError("No records found for grouped chart")

    labels = [row["city_name"] for row in rows]
    x_positions = list(range(len(labels)))
    width = 0.18
    series = [
        ("Min temp", [row["min_temp"] for row in rows], "#2f6f8f"),
        ("Mean temp", [row["mean_temp"] for row in rows], "#48785f"),
        ("Max temp", [row["max_temp"] for row in rows], "#b85c38"),
        ("Precipitation", [row["precipitation"] for row in rows], "#7a5c99"),
    ]

    plt.figure(figsize=(10, 5.5))
    for index, (label, values, color) in enumerate(series):
        offsets = [x + (index - 1.5) * width for x in x_positions]
        plt.bar(offsets, values, width=width, label=label, color=color)
    plt.xticks(x_positions, labels)
    plt.title(f"Weather Averages by City ({date_from} to {date_to})")
    plt.xlabel("City")
    plt.ylabel("Average value")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    return _save_chart(output_path)


def plot_monthly_min_max_temperature(connection, city_id, year, month, output_path=None):
    """Create a multi-line chart for daily min and max temperature in a month."""

    year = validate_year(year)
    month = int(month)
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    output_path = output_path or DEFAULT_CHART_DIR / f"city_{city_id}_temperature_{year}_{month:02d}.png"
    rows = fetch_all(
        connection,
        """
        SELECT dwe.date, dwe.min_temp, dwe.max_temp, cities.name AS city_name
        FROM daily_weather_entries AS dwe
        JOIN cities ON cities.id = dwe.city_id
        WHERE dwe.city_id = ?
          AND strftime('%Y', dwe.date) = ?
          AND strftime('%m', dwe.date) = ?
        ORDER BY dwe.date
        """,
        (city_id, str(year), f"{month:02d}"),
    )
    if not rows:
        raise ValueError("No temperature records found for the requested month")

    plt.figure(figsize=(10, 5))
    dates = [row["date"][8:] for row in rows]
    plt.plot(dates, [row["min_temp"] for row in rows], marker="o", linewidth=1.5, label="Min temp")
    plt.plot(dates, [row["max_temp"] for row in rows], marker="o", linewidth=1.5, label="Max temp")
    plt.title(f"Daily Min/Max Temperature for {rows[0]['city_name']} ({year}-{month:02d})")
    plt.xlabel("Day")
    plt.ylabel("Temperature (C)")
    plt.legend()
    plt.grid(alpha=0.3)
    return _save_chart(output_path)


def plot_temperature_vs_rainfall_scatter(connection, date_from, date_to, output_path=None):
    """Create a scatter plot of average temperature against rainfall by city."""

    date_from, date_to = validate_date_range(date_from, date_to)
    output_path = output_path or DEFAULT_CHART_DIR / "temperature_vs_rainfall_scatter.png"
    rows = fetch_all(
        connection,
        """
        SELECT cities.name AS city_name,
               AVG(dwe.mean_temp) AS average_temperature,
               AVG(dwe.precipitation) AS average_precipitation
        FROM daily_weather_entries AS dwe
        JOIN cities ON cities.id = dwe.city_id
        WHERE dwe.date BETWEEN ? AND ?
        GROUP BY cities.id, cities.name
        ORDER BY cities.name
        """,
        (date_from, date_to),
    )
    if not rows:
        raise ValueError("No records found for scatter chart")

    plt.figure(figsize=(8, 5.5))
    plt.scatter(
        [row["average_temperature"] for row in rows],
        [row["average_precipitation"] for row in rows],
        color="#b85c38",
        s=90,
    )
    for row in rows:
        plt.annotate(row["city_name"], (row["average_temperature"], row["average_precipitation"]))
    plt.title(f"Average Temperature vs Rainfall ({date_from} to {date_to})")
    plt.xlabel("Average mean temperature (C)")
    plt.ylabel("Average precipitation (mm)")
    plt.grid(alpha=0.3)
    return _save_chart(output_path)


def generate_all_sample_charts(connection, output_dir=DEFAULT_CHART_DIR):
    """Generate a representative chart set for assessment evidence."""

    output_dir = Path(output_dir)
    return [
        plot_seven_day_precipitation(connection, 1, "2024-01-01", output_dir / "01_7_day_precipitation.png"),
        plot_precipitation_for_cities(connection, [1, 2, 3, 4], "2024-01-01", "2024-01-31", output_dir / "02_city_precipitation_comparison.png"),
        plot_average_yearly_precipitation_by_country(connection, 2024, output_dir / "03_country_average_precipitation.png"),
        plot_temperature_precipitation_grouped(connection, [1, 2, 3, 4], "2024-06-01", "2024-06-30", output_dir / "04_grouped_weather_averages.png"),
        plot_monthly_min_max_temperature(connection, 1, 2024, 7, output_dir / "05_monthly_min_max_temperature.png"),
        plot_temperature_vs_rainfall_scatter(connection, "2024-01-01", "2024-12-31", output_dir / "06_temperature_vs_rainfall.png"),
    ]


if __name__ == "__main__":
    with connect_database(DEFAULT_DB_PATH) as conn:
        generate_all_sample_charts(conn)
