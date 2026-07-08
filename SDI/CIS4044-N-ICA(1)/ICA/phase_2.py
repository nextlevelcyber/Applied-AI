# Phase 2: draw charts from the database using matplotlib.
#
# Every chart function below does the same three steps:
#   1. read the numbers it needs from the database
#   2. build the chart with matplotlib
#   3. save the chart as a PNG file in the charts folder

import os

import matplotlib
matplotlib.use("Agg")  # draw charts in memory and save them as files (no window pops up)
import matplotlib.pyplot as plt

from phase_1 import (
    PROJECT_FOLDER,
    connect_database,
    validate_date,
    validate_date_range,
    validate_year,
)

CHART_FOLDER = os.path.join(PROJECT_FOLDER, "charts")


def save_chart(output_path):
    # Save the current chart as a PNG file and close it.
    folder = os.path.dirname(output_path)
    if folder != "" and not os.path.exists(folder):
        os.makedirs(folder)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print("Chart saved:", output_path)
    return output_path


def plot_seven_day_precipitation(connection, city_id, start_date, output_path=None):
    # Bar chart: daily precipitation for one city over 7 days.
    start_date = validate_date(start_date, "start_date")
    if output_path is None:
        output_path = os.path.join(CHART_FOLDER, "01_7_day_precipitation.png")

    rows = connection.execute(
        """
        SELECT daily_weather_entries.date,
               daily_weather_entries.precipitation,
               cities.name AS city_name
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.city_id = ?
          AND daily_weather_entries.date BETWEEN ? AND date(?, '+6 day')
        ORDER BY daily_weather_entries.date
        """,
        (city_id, start_date, start_date),
    ).fetchall()
    if not rows:
        raise ValueError("No weather records found for this city and date range")

    dates = []
    values = []
    for row in rows:
        dates.append(row["date"][5:])  # keep only the MM-DD part so labels stay short
        values.append(row["precipitation"])

    plt.figure(figsize=(9, 5))
    plt.bar(dates, values, color="steelblue")
    plt.title("7-Day Precipitation for " + rows[0]["city_name"] + " from " + start_date)
    plt.xlabel("Date")
    plt.ylabel("Precipitation (mm)")
    plt.grid(axis="y", alpha=0.3)  # light horizontal grid lines
    return save_chart(output_path)


def plot_precipitation_for_cities(connection, city_ids, date_from, date_to, output_path=None):
    # Bar chart: total precipitation for several cities in a date range.
    if not city_ids:
        raise ValueError("at least one city id is needed")
    date_from, date_to = validate_date_range(date_from, date_to)
    if output_path is None:
        output_path = os.path.join(CHART_FOLDER, "02_city_precipitation_comparison.png")

    # Run one small query per city. Simple, and fast enough
    # for the few cities in this database.
    names = []
    totals = []
    for city_id in city_ids:
        row = connection.execute(
            """
            SELECT cities.name AS city_name,
                   SUM(daily_weather_entries.precipitation) AS total_precipitation
            FROM daily_weather_entries
            JOIN cities ON cities.id = daily_weather_entries.city_id
            WHERE daily_weather_entries.city_id = ?
              AND daily_weather_entries.date BETWEEN ? AND ?
            """,
            (city_id, date_from, date_to),
        ).fetchone()
        # If the city has no data in this range, the sum comes back empty.
        if row["city_name"] is not None:
            names.append(row["city_name"])
            totals.append(row["total_precipitation"])
    if not names:
        raise ValueError("No precipitation records found for these cities")

    plt.figure(figsize=(8, 5))
    plt.bar(names, totals, color="purple")
    plt.title("Total Precipitation by City (" + date_from + " to " + date_to + ")")
    plt.xlabel("City")
    plt.ylabel("Total precipitation (mm)")
    plt.grid(axis="y", alpha=0.3)
    return save_chart(output_path)


def plot_average_yearly_precipitation_by_country(connection, year, output_path=None):
    # Bar chart: average daily precipitation for every country in one year.
    year = validate_year(year)
    if output_path is None:
        output_path = os.path.join(CHART_FOLDER, "03_country_average_precipitation.png")

    rows = connection.execute(
        """
        SELECT countries.name AS country_name,
               AVG(daily_weather_entries.precipitation) AS average_precipitation
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
        raise ValueError("No country precipitation records found for this year")

    names = []
    averages = []
    for row in rows:
        names.append(row["country_name"])
        averages.append(row["average_precipitation"])

    plt.figure(figsize=(8, 5))
    plt.bar(names, averages, color="seagreen")
    plt.title("Average Daily Precipitation by Country (" + str(year) + ")")
    plt.xlabel("Country")
    plt.ylabel("Average daily precipitation (mm)")
    plt.grid(axis="y", alpha=0.3)
    return save_chart(output_path)


def plot_temperature_precipitation_grouped(connection, city_ids, date_from, date_to, output_path=None):
    # Grouped bar chart: min, mean, max temperature and precipitation per city.
    if not city_ids:
        raise ValueError("at least one city id is needed")
    date_from, date_to = validate_date_range(date_from, date_to)
    if output_path is None:
        output_path = os.path.join(CHART_FOLDER, "04_grouped_weather_averages.png")

    names = []
    min_temps = []
    mean_temps = []
    max_temps = []
    rain = []
    for city_id in city_ids:
        row = connection.execute(
            """
            SELECT cities.name AS city_name,
                   AVG(daily_weather_entries.min_temp) AS min_temp,
                   AVG(daily_weather_entries.mean_temp) AS mean_temp,
                   AVG(daily_weather_entries.max_temp) AS max_temp,
                   AVG(daily_weather_entries.precipitation) AS precipitation
            FROM daily_weather_entries
            JOIN cities ON cities.id = daily_weather_entries.city_id
            WHERE daily_weather_entries.city_id = ?
              AND daily_weather_entries.date BETWEEN ? AND ?
            """,
            (city_id, date_from, date_to),
        ).fetchone()
        if row["city_name"] is not None:
            names.append(row["city_name"])
            min_temps.append(row["min_temp"])
            mean_temps.append(row["mean_temp"])
            max_temps.append(row["max_temp"])
            rain.append(row["precipitation"])
    if not names:
        raise ValueError("No records found for the grouped chart")

    # Each city gets one position on the x axis (0, 1, 2, ...).
    # The four bars are shifted a little left or right of that position
    # so they sit side by side instead of on top of each other.
    positions = list(range(len(names)))
    width = 0.2
    plt.figure(figsize=(10, 5.5))
    plt.bar([p - 1.5 * width for p in positions], min_temps, width=width, label="Min temp", color="steelblue")
    plt.bar([p - 0.5 * width for p in positions], mean_temps, width=width, label="Mean temp", color="seagreen")
    plt.bar([p + 0.5 * width for p in positions], max_temps, width=width, label="Max temp", color="darkorange")
    plt.bar([p + 1.5 * width for p in positions], rain, width=width, label="Precipitation", color="purple")
    plt.xticks(positions, names)
    plt.title("Weather Averages by City (" + date_from + " to " + date_to + ")")
    plt.xlabel("City")
    plt.ylabel("Average value")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    return save_chart(output_path)


def plot_monthly_min_max_temperature(connection, city_id, year, month, output_path=None):
    # Line chart: daily min and max temperature for one city in one month.
    year = validate_year(year)
    month = int(month)
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    if output_path is None:
        output_path = os.path.join(CHART_FOLDER, "05_monthly_min_max_temperature.png")

    month_text = f"{month:02d}"  # e.g. 7 becomes "07" to match the date format
    rows = connection.execute(
        """
        SELECT daily_weather_entries.date,
               daily_weather_entries.min_temp,
               daily_weather_entries.max_temp,
               cities.name AS city_name
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.city_id = ?
          AND strftime('%Y', daily_weather_entries.date) = ?
          AND strftime('%m', daily_weather_entries.date) = ?
        ORDER BY daily_weather_entries.date
        """,
        (city_id, str(year), month_text),
    ).fetchall()
    if not rows:
        raise ValueError("No temperature records found for this month")

    days = []
    min_temps = []
    max_temps = []
    for row in rows:
        days.append(row["date"][8:])  # keep only the DD part of the date
        min_temps.append(row["min_temp"])
        max_temps.append(row["max_temp"])

    plt.figure(figsize=(10, 5))
    plt.plot(days, min_temps, marker="o", label="Min temp")
    plt.plot(days, max_temps, marker="o", label="Max temp")
    plt.title("Daily Min/Max Temperature for " + rows[0]["city_name"] + " (" + str(year) + "-" + month_text + ")")
    plt.xlabel("Day")
    plt.ylabel("Temperature (C)")
    plt.legend()
    plt.grid(alpha=0.3)
    return save_chart(output_path)


def plot_temperature_vs_rainfall_scatter(connection, date_from, date_to, output_path=None):
    # Scatter plot: average temperature against average rainfall, one dot per city.
    date_from, date_to = validate_date_range(date_from, date_to)
    if output_path is None:
        output_path = os.path.join(CHART_FOLDER, "06_temperature_vs_rainfall.png")

    rows = connection.execute(
        """
        SELECT cities.name AS city_name,
               AVG(daily_weather_entries.mean_temp) AS average_temperature,
               AVG(daily_weather_entries.precipitation) AS average_precipitation
        FROM daily_weather_entries
        JOIN cities ON cities.id = daily_weather_entries.city_id
        WHERE daily_weather_entries.date BETWEEN ? AND ?
        GROUP BY cities.id, cities.name
        ORDER BY cities.name
        """,
        (date_from, date_to),
    ).fetchall()
    if not rows:
        raise ValueError("No records found for the scatter chart")

    plt.figure(figsize=(8, 5.5))
    for row in rows:
        plt.scatter(row["average_temperature"], row["average_precipitation"], s=90, color="darkorange")
        # Write the city name next to its dot.
        plt.annotate(row["city_name"], (row["average_temperature"], row["average_precipitation"]))
    plt.title("Average Temperature vs Rainfall (" + date_from + " to " + date_to + ")")
    plt.xlabel("Average mean temperature (C)")
    plt.ylabel("Average precipitation (mm)")
    plt.grid(alpha=0.3)
    return save_chart(output_path)


def generate_all_charts(connection):
    # Create every sample chart used as evidence for the report.
    charts = []
    charts.append(plot_seven_day_precipitation(connection, 1, "2024-01-01"))
    charts.append(plot_precipitation_for_cities(connection, [1, 2, 3, 4], "2024-01-01", "2024-01-31"))
    charts.append(plot_average_yearly_precipitation_by_country(connection, 2024))
    charts.append(plot_temperature_precipitation_grouped(connection, [1, 2, 3, 4], "2024-06-01", "2024-06-30"))
    charts.append(plot_monthly_min_max_temperature(connection, 1, 2024, 7))
    charts.append(plot_temperature_vs_rainfall_scatter(connection, "2024-01-01", "2024-12-31"))
    return charts


# Running this file directly creates all the sample charts.
if __name__ == "__main__":
    connection = connect_database()
    generate_all_charts(connection)
    connection.close()
