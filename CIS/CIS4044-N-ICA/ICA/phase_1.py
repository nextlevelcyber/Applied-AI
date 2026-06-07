# Author: Cui Jiangkun
# Student ID: 20268996

import sqlite3


# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory 50-59
'''
def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")
            # print(row)

    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities(connection):
    # Queries the database and selects all the cities
    # stored in the cities table of the database.
    # The returned results are then printed to the
    # console.
    try:
        # Define the query
        query = "SELECT * from [cities]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(
                f"City Id: {row['id']} -- City Name: {row['name']} -- "
                f"Country Id: {row['country_id']} -- Lat/Long: {row['latlong']}"
            )

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Good

In additional to successfully completing *all* the "Satisfactory" queries, 
implement the queries that satisfy the each query requirements indicated by the name
of the function and any parameters to achieve a potential mark in the range 60-69.
'''
def average_annual_temperature(connection, city_id, year):
    # Calculates the average mean temperature for one city in one year.
    try:
        query = """
            SELECT
                cities.name AS city_name,
                ROUND(AVG(daily_weather_entries.mean_temp), 2) AS average_temp
            FROM daily_weather_entries
            INNER JOIN cities
                ON cities.id = daily_weather_entries.city_id
            WHERE
                daily_weather_entries.city_id = ?
                AND strftime('%Y', daily_weather_entries.date) = ?
            GROUP BY cities.id, cities.name
        """

        cursor = connection.cursor()
        row = cursor.execute(query, (city_id, str(year))).fetchone()

        if row is None:
            print(f"No temperature data found for city id {city_id} in {year}.")
            return

        print(
            f"City: {row['city_name']} -- Year: {year} -- "
            f"Average Annual Temperature: {row['average_temp']:.2f}"
        )

    except sqlite3.OperationalError as ex:
        print(ex)

def average_seven_day_precipitation(connection, city_id, start_date):
    # Calculates the average precipitation over seven consecutive days.
    try:
        query = """
            SELECT
                cities.name AS city_name,
                DATE(?) AS start_date,
                DATE(?, '+6 day') AS end_date,
                ROUND(AVG(daily_weather_entries.precipitation), 2) AS average_precipitation
            FROM daily_weather_entries
            INNER JOIN cities
                ON cities.id = daily_weather_entries.city_id
            WHERE
                daily_weather_entries.city_id = ?
                AND daily_weather_entries.date BETWEEN DATE(?) AND DATE(?, '+6 day')
            GROUP BY cities.id, cities.name
        """

        cursor = connection.cursor()
        row = cursor.execute(
            query,
            (start_date, start_date, city_id, start_date, start_date),
        ).fetchone()

        if row is None:
            print(
                f"No precipitation data found for city id {city_id} "
                f"from {start_date}."
            )
            return

        print(
            f"City: {row['city_name']} -- Date Range: {row['start_date']} "
            f"to {row['end_date']} -- Average Seven Day Precipitation: "
            f"{row['average_precipitation']:.2f}"
        )

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Very good

In additional to successfully completing *all* the "Satisfactory" and "Good" queries, 
implement the queries that satisfy the each query requirements indicated by the name
of the function and any parameters to achieve a potential mark in the range 70-79.
'''
def average_mean_temp_by_city(connection, date_from, date_to):
    # Calculates the average mean temperature for each city in a date range.
    try:
        query = """
            SELECT
                cities.name AS city_name,
                ROUND(AVG(daily_weather_entries.mean_temp), 2) AS average_temp
            FROM daily_weather_entries
            INNER JOIN cities
                ON cities.id = daily_weather_entries.city_id
            WHERE daily_weather_entries.date BETWEEN DATE(?) AND DATE(?)
            GROUP BY cities.id, cities.name
            ORDER BY cities.name
        """

        cursor = connection.cursor()
        results = cursor.execute(query, (date_from, date_to)).fetchall()

        if len(results) == 0:
            print(f"No temperature data found from {date_from} to {date_to}.")
            return

        print(f"Average Mean Temperature by City: {date_from} to {date_to}")
        for row in results:
            print(
                f"City: {row['city_name']} -- "
                f"Average Mean Temperature: {row['average_temp']:.2f}"
            )

    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_precipitation_by_country(connection, year):
    # Calculates the average daily precipitation by country for one year.
    try:
        query = """
            SELECT
                countries.name AS country_name,
                ROUND(AVG(daily_weather_entries.precipitation), 2) AS average_precipitation
            FROM daily_weather_entries
            INNER JOIN cities
                ON cities.id = daily_weather_entries.city_id
            INNER JOIN countries
                ON countries.id = cities.country_id
            WHERE strftime('%Y', daily_weather_entries.date) = ?
            GROUP BY countries.id, countries.name
            ORDER BY countries.name
        """

        cursor = connection.cursor()
        results = cursor.execute(query, (str(year),)).fetchall()

        if len(results) == 0:
            print(f"No precipitation data found for {year}.")
            return

        print(f"Average Annual Precipitation by Country: {year}")
        for row in results:
            print(
                f"Country: {row['country_name']} -- "
                f"Average Annual Precipitation: "
                f"{row['average_precipitation']:.2f}"
            )

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Excellent

To achieve 80+ you will identify several suitable queries of your own that go beyond 
basic requirements for this phase.
'''

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    database_path = __file__.replace(
        "ICA/phase_1.py",
        "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db",
    )
    print(database_path)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    select_all_countries(connection)
    select_all_cities(connection)
    average_annual_temperature(connection, 1, 2020)
    average_seven_day_precipitation(connection, 1, "2020-01-01")
    average_mean_temp_by_city(connection, "2020-01-01", "2020-01-07")
    average_annual_precipitation_by_country(connection, 2020)
    connection.close()
