"""Phase 1: SQLite queries for the historical weather database."""

import sqlite3


# Note: Display all real/float numbers to 2 decimal places.


DEFAULT_DB_PATH = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"


def connect_database(db_path=DEFAULT_DB_PATH):
    """Open the SQLite database using named-column rows."""

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def fetch_all(connection, query, params=()):
    """Execute a SELECT query and return all rows."""

    return list(connection.execute(query, params))


def print_table(rows, columns):
    """Print database rows using display labels and row keys."""

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


def validate_date(value, field_name="date"):
    """Validate an ISO date string without importing extra libraries."""

    if not isinstance(value, str):
        raise ValueError(f"{field_name} must use YYYY-MM-DD format")
    parts = value.split("-")
    if len(parts) != 3 or len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format")
    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format") from exc

    if month < 1 or month > 12:
        raise ValueError(f"{field_name} is not a valid calendar date")
    days_in_month = [31, 29 if _is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if day < 1 or day > days_in_month[month - 1]:
        raise ValueError(f"{field_name} is not a valid calendar date")
    return value


def validate_date_range(date_from, date_to):
    """Validate an inclusive date range."""

    start = validate_date(date_from, "date_from")
    end = validate_date(date_to, "date_to")
    if start > end:
        raise ValueError("date_from must be before or equal to date_to")
    return start, end


def validate_year(year):
    """Validate a four-digit year."""

    try:
        value = int(year)
    except (TypeError, ValueError) as exc:
        raise ValueError("year must be an integer") from exc
    if value < 1900 or value > 2100:
        raise ValueError("year must be between 1900 and 2100")
    return value


def _is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def select_all_countries(connection):
    """Print and return all countries stored in the database."""

    try:
        rows = fetch_all(connection, "SELECT id, name, timezone FROM countries ORDER BY name")
        print_table(
            rows,
            (
                ("Country Id", "id"),
                ("Country Name", "name"),
                ("Country Timezone", "timezone"),
            ),
        )
        return rows
    except sqlite3.OperationalError as ex:
        print(ex)
        return []


def select_all_cities(connection):
    """Print and return all cities with their country names."""

    try:
        rows = fetch_all(
            connection,
            """
            SELECT cities.id, cities.name, countries.name AS country_name, cities.latlong
            FROM cities
            JOIN countries ON countries.id = cities.country_id
            ORDER BY country_name, cities.name
            """,
        )
        print_table(
            rows,
            (
                ("City Id", "id"),
                ("City Name", "name"),
                ("Country", "country_name"),
                ("Latitude/Longitude", "latlong"),
            ),
        )
        return rows
    except sqlite3.OperationalError as ex:
        print(ex)
        return []


def average_annual_temperature(connection, city_id, year):
    """Print and return a city's average mean temperature for one year."""

    year = validate_year(year)
    rows = fetch_all(
        connection,
        """
        SELECT cities.id AS city_id,
               cities.name AS city_name,
               ? AS year,
               AVG(daily_weather_entries.mean_temp) AS average_mean_temp
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.city_id = ?
          AND strftime('%Y', daily_weather_entries.date) = ?
        GROUP BY cities.id, cities.name
        """,
        (year, city_id, str(year)),
    )
    print_table(
        rows,
        (
            ("City Id", "city_id"),
            ("City", "city_name"),
            ("Year", "year"),
            ("Average Mean Temperature", "average_mean_temp"),
        ),
    )
    return rows


def average_seven_day_precipitation(connection, city_id, start_date):
    """Print and return the average precipitation from start_date for 7 days."""

    start_date = validate_date(start_date, "start_date")
    rows = fetch_all(
        connection,
        """
        SELECT cities.id AS city_id,
               cities.name AS city_name,
               ? AS start_date,
               date(?, '+6 day') AS end_date,
               AVG(daily_weather_entries.precipitation) AS average_precipitation,
               COUNT(*) AS days_found
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.city_id = ?
          AND daily_weather_entries.date BETWEEN ? AND date(?, '+6 day')
        GROUP BY cities.id, cities.name
        """,
        (start_date, start_date, city_id, start_date, start_date),
    )
    print_table(
        rows,
        (
            ("City Id", "city_id"),
            ("City", "city_name"),
            ("Start Date", "start_date"),
            ("End Date", "end_date"),
            ("Average Precipitation", "average_precipitation"),
            ("Days Found", "days_found"),
        ),
    )
    return rows



def average_mean_temp_by_city(connection, date_from, date_to):
    """Print and return average mean temperature per city for a date range."""

    date_from, date_to = validate_date_range(date_from, date_to)
    rows = fetch_all(
        connection,
        """
        SELECT cities.id AS city_id,
               cities.name AS city_name,
               countries.name AS country_name,
               AVG(daily_weather_entries.mean_temp) AS average_mean_temp
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        JOIN countries ON countries.id = cities.country_id
        WHERE daily_weather_entries.date BETWEEN ? AND ?
        GROUP BY cities.id, cities.name, countries.name
        ORDER BY average_mean_temp DESC
        """,
        (date_from, date_to),
    )
    print_table(
        rows,
        (
            ("City Id", "city_id"),
            ("City", "city_name"),
            ("Country", "country_name"),
            ("Average Mean Temperature", "average_mean_temp"),
        ),
    )
    return rows


def average_annual_precipitation_by_country(connection, year):
    """Print and return annual average precipitation grouped by country."""

    year = validate_year(year)
    rows = fetch_all(
        connection,
        """
        SELECT countries.id AS country_id,
               countries.name AS country_name,
               ? AS year,
               AVG(daily_weather_entries.precipitation) AS average_precipitation,
               SUM(daily_weather_entries.precipitation) AS total_precipitation
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        JOIN countries ON countries.id = cities.country_id
        WHERE strftime('%Y', daily_weather_entries.date) = ?
        GROUP BY countries.id, countries.name
        ORDER BY countries.name
        """,
        (year, str(year)),
    )
    print_table(
        rows,
        (
            ("Country Id", "country_id"),
            ("Country", "country_name"),
            ("Year", "year"),
            ("Average Precipitation", "average_precipitation"),
            ("Total Precipitation", "total_precipitation"),
        ),
    )
    return rows


def monthly_temperature_summary(connection, city_id, year):
    """Extra query: monthly min, mean, and max temperature summary for one city."""

    year = validate_year(year)
    rows = fetch_all(
        connection,
        """
        SELECT cities.name AS city_name,
               strftime('%m', daily_weather_entries.date) AS month,
               AVG(daily_weather_entries.min_temp) AS average_min_temp,
               AVG(daily_weather_entries.mean_temp) AS average_mean_temp,
               AVG(daily_weather_entries.max_temp) AS average_max_temp
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.city_id = ?
          AND strftime('%Y', daily_weather_entries.date) = ?
        GROUP BY cities.name, strftime('%m', daily_weather_entries.date)
        ORDER BY month
        """,
        (city_id, str(year)),
    )
    print_table(
        rows,
        (
            ("City", "city_name"),
            ("Month", "month"),
            ("Average Min", "average_min_temp"),
            ("Average Mean", "average_mean_temp"),
            ("Average Max", "average_max_temp"),
        ),
    )
    return rows


def wettest_city_by_year(connection):
    """Extra query: rank cities by total precipitation for each available year."""

    rows = fetch_all(
        connection,
        """
        SELECT year,
               city_name,
               country_name,
               total_precipitation
        FROM (
            SELECT strftime('%Y', dwe.date) AS year,
                   cities.name AS city_name,
                   countries.name AS country_name,
                   SUM(dwe.precipitation) AS total_precipitation,
                   RANK() OVER (
                       PARTITION BY strftime('%Y', dwe.date)
                       ORDER BY SUM(dwe.precipitation) DESC
                   ) AS precipitation_rank
            FROM daily_weather_entries AS dwe
            JOIN cities ON cities.id = dwe.city_id
            JOIN countries ON countries.id = cities.country_id
            GROUP BY year, cities.name, countries.name
        )
        WHERE precipitation_rank = 1
        ORDER BY year
        """,
    )
    print_table(
        rows,
        (
            ("Year", "year"),
            ("Wettest City", "city_name"),
            ("Country", "country_name"),
            ("Total Precipitation", "total_precipitation"),
        ),
    )
    return rows


if __name__ == "__main__":
    with connect_database(DEFAULT_DB_PATH) as conn:
        select_all_countries(conn)
        select_all_cities(conn)
        average_annual_temperature(conn, city_id=1, year=2024)
        average_seven_day_precipitation(conn, city_id=1, start_date="2024-01-01")
        average_mean_temp_by_city(conn, date_from="2024-01-01", date_to="2024-12-31")
        average_annual_precipitation_by_country(conn, year=2024)
        monthly_temperature_summary(conn, city_id=1, year=2024)
        wettest_city_by_year(conn)
