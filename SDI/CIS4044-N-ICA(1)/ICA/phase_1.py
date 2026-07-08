# read data from the SQLite database and print the results.
import os
import sqlite3
from datetime import datetime

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_FOLDER, "db", "CIS4044-N-SDI-OPENMETEO-PARTIAL.db")


def connect_database(db_path=DB_PATH):
    # open the database file.
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def validate_date(text, field_name="date"):
    # Check that the text is a real date written like 2024-01-31.
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError(field_name + " must be a real date in YYYY-MM-DD format")
    return text


def validate_date_range(date_from, date_to):
    # Check both dates and make sure the range is not reversed.
    validate_date(date_from, "date_from")
    validate_date(date_to, "date_to")
    if date_from > date_to:
        raise ValueError("date_from must be before or equal to date_to")
    return date_from, date_to


def validate_year(year):
    # Check that the year is a sensible whole number like 2024.
    try:
        year = int(year)
    except (TypeError, ValueError):
        raise ValueError("year must be a whole number")
    if year < 1900 or year > 2100:
        raise ValueError("year must be between 1900 and 2100")
    return year


def select_all_countries(connection):
    # Show every country stored in the database.
    rows = connection.execute(
        "SELECT id, name, timezone FROM countries ORDER BY name"
    ).fetchall()

    if not rows:
        print("No records found.")
    for row in rows:
        print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")
    return rows


def select_all_cities(connection):
    # Show every city together with the name of its country.
    rows = connection.execute(
        """
        SELECT cities.id, cities.name, countries.name AS country_name, cities.latlong
        FROM cities
        JOIN countries ON countries.id = cities.country_id
        ORDER BY country_name, cities.name
        """
    ).fetchall()

    if not rows:
        print("No records found.")
    for row in rows:
        print(f"City Id: {row['id']} -- City Name: {row['name']} -- Country: {row['country_name']} -- Latitude/Longitude: {row['latlong']}")
    return rows


def average_annual_temperature(connection, city_id, year):
    # Average of the daily mean temperatures for one city in one year.
    # strftime('%Y', date) takes the year part out of a date like 2024-01-31.
    year = validate_year(year)
    rows = connection.execute(
        """
        SELECT cities.id AS city_id,
               cities.name AS city_name,
               AVG(daily_weather_entries.mean_temp) AS average_mean_temp
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.city_id = ?
          AND strftime('%Y', daily_weather_entries.date) = ?
        GROUP BY cities.id, cities.name
        """,
        (city_id, str(year)),
    ).fetchall()

    if not rows:
        print("No records found.")
    for row in rows:
        print(f"City Id: {row['city_id']} -- City: {row['city_name']} -- Year: {year} -- Average Mean Temperature: {row['average_mean_temp']:.2f}")
    return rows


def average_seven_day_precipitation(connection, city_id, start_date):
    # Average precipitation for one city over 7 days from the start date.
    # date(?, '+6 day') adds 6 days, so start date + 6 more days = 7 days total.
    start_date = validate_date(start_date, "start_date")
    rows = connection.execute(
        """
        SELECT cities.id AS city_id,
               cities.name AS city_name,
               date(?, '+6 day') AS end_date,
               AVG(daily_weather_entries.precipitation) AS average_precipitation,
               COUNT(*) AS days_found
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.city_id = ?
          AND daily_weather_entries.date BETWEEN ? AND date(?, '+6 day')
        GROUP BY cities.id, cities.name
        """,
        (start_date, city_id, start_date, start_date),
    ).fetchall()

    if not rows:
        print("No records found.")
    for row in rows:
        print(f"City Id: {row['city_id']} -- City: {row['city_name']} -- Start Date: {start_date} -- End Date: {row['end_date']} -- Average Precipitation: {row['average_precipitation']:.2f} -- Days Found: {row['days_found']}")
    return rows


def average_mean_temp_by_city(connection, date_from, date_to):
    # Average mean temperature for every city between two dates,
    # warmest city first.
    date_from, date_to = validate_date_range(date_from, date_to)
    rows = connection.execute(
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
    ).fetchall()

    if not rows:
        print("No records found.")
    for row in rows:
        print(f"City Id: {row['city_id']} -- City: {row['city_name']} -- Country: {row['country_name']} -- Average Mean Temperature: {row['average_mean_temp']:.2f}")
    return rows


def average_annual_precipitation_by_country(connection, year):
    # Average and total precipitation for every country in one year.
    year = validate_year(year)
    rows = connection.execute(
        """
        SELECT countries.id AS country_id,
               countries.name AS country_name,
               AVG(daily_weather_entries.precipitation) AS average_precipitation,
               SUM(daily_weather_entries.precipitation) AS total_precipitation
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        JOIN countries ON countries.id = cities.country_id
        WHERE strftime('%Y', daily_weather_entries.date) = ?
        GROUP BY countries.id, countries.name
        ORDER BY countries.name
        """,
        (str(year),),
    ).fetchall()

    if not rows:
        print("No records found.")
    for row in rows:
        print(f"Country Id: {row['country_id']} -- Country: {row['country_name']} -- Year: {year} -- Average Precipitation: {row['average_precipitation']:.2f} -- Total Precipitation: {row['total_precipitation']:.2f}")
    return rows


def monthly_temperature_summary(connection, city_id, year):
    # Extra query: average min, mean and max temperature
    # for one city, month by month, in one year.
    year = validate_year(year)
    rows = connection.execute(
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
        GROUP BY cities.name, month
        ORDER BY month
        """,
        (city_id, str(year)),
    ).fetchall()

    if not rows:
        print("No records found.")
    for row in rows:
        print(f"City: {row['city_name']} -- Month: {row['month']} -- Average Min: {row['average_min_temp']:.2f} -- Average Mean: {row['average_mean_temp']:.2f} -- Average Max: {row['average_max_temp']:.2f}")
    return rows


def wettest_city_by_year(connection):
    # Extra query: for every year in the database, find the city
    # with the highest total precipitation.
    # Step 1: get the list of years. Step 2: for each year, sort the
    # cities by total precipitation and keep only the top one (LIMIT 1).
    years = connection.execute(
        "SELECT DISTINCT strftime('%Y', date) AS year FROM daily_weather_entries ORDER BY year"
    ).fetchall()

    results = []
    for year_row in years:
        year = year_row["year"]
        row = connection.execute(
            """
            SELECT cities.name AS city_name,
                   countries.name AS country_name,
                   SUM(daily_weather_entries.precipitation) AS total_precipitation
            FROM daily_weather_entries
            JOIN cities ON cities.id = daily_weather_entries.city_id
            JOIN countries ON countries.id = cities.country_id
            WHERE strftime('%Y', daily_weather_entries.date) = ?
            GROUP BY cities.id, cities.name, countries.name
            ORDER BY total_precipitation DESC
            LIMIT 1
            """,
            (year,),
        ).fetchone()
        if row is not None:
            print(f"Year: {year} -- Wettest City: {row['city_name']} -- Country: {row['country_name']} -- Total Precipitation: {row['total_precipitation']:.2f}")
            results.append(row)

    if not results:
        print("No records found.")
    return results


# Running this file directly tries every query with example values.
if __name__ == "__main__":
    connection = connect_database()
    select_all_countries(connection)
    # select_all_cities(connection)
    # average_annual_temperature(connection, city_id=1, year=2024)
    # average_seven_day_precipitation(connection, city_id=1, start_date="2024-01-01")
    # average_mean_temp_by_city(connection, date_from="2024-01-01", date_to="2024-12-31")
    # average_annual_precipitation_by_country(connection, year=2024)
    # monthly_temperature_summary(connection, city_id=1, year=2024)
    # wettest_city_by_year(connection)
    connection.close()
