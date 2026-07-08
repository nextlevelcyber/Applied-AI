# Phase 3: download weather data from the Open-Meteo web API
# and save it into the database. The extra library needed is "requests".
#
# The full job is split into four small functions:
#   get_city              -> look up the city in the database
#   download_weather_data -> call the Open-Meteo API
#   parse_daily_weather   -> turn the JSON answer into simple rows
#   store_daily_weather   -> write the rows into the database

import requests

from phase_1 import connect_database, validate_date_range

API_URL = "https://archive-api.open-meteo.com/v1/archive"


def get_city(connection, city_id):
    # Look up one city and return its details as a simple dictionary.
    row = connection.execute(
        """
        SELECT cities.id, cities.name, cities.latlong, countries.timezone
        FROM cities
        JOIN countries ON countries.id = cities.country_id
        WHERE cities.id = ?
        """,
        (city_id,),
    ).fetchone()
    if row is None:
        raise ValueError("No city found with id " + str(city_id))

    # latlong is stored as one text value like "54.57,-1.23",
    # so split it at the comma to get the two numbers.
    latitude_text, longitude_text = row["latlong"].split(",")
    return {
        "id": row["id"],
        "name": row["name"],
        "latitude": float(latitude_text),
        "longitude": float(longitude_text),
        "timezone": row["timezone"],
    }


def download_weather_data(city, start_date, end_date):
    # Ask the Open-Meteo archive API for daily weather data for one city.
    start_date, end_date = validate_date_range(start_date, end_date)
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_min,temperature_2m_max,temperature_2m_mean,precipitation_sum",
        "timezone": city["timezone"],
    }

    try:
        response = requests.get(API_URL, params=params, timeout=20)
    except requests.RequestException as error:
        # Covers timeouts, no internet, wrong address, and so on.
        raise Exception("Could not reach Open-Meteo: " + str(error))

    if response.status_code != 200:
        raise Exception("Open-Meteo request failed with status code " + str(response.status_code))

    data = response.json()
    if "daily" not in data:
        raise Exception("Open-Meteo answer did not include daily weather data")
    return data


def parse_daily_weather(data):
    # Turn the JSON from the API into a list of simple row dictionaries.
    # The API sends parallel lists: one list of dates, one list of
    # min temperatures, and so on. Item i of every list belongs together.
    if "daily" not in data:
        raise Exception("Open-Meteo answer did not include daily weather data")
    daily = data["daily"]

    needed_keys = [
        "time",
        "temperature_2m_min",
        "temperature_2m_max",
        "temperature_2m_mean",
        "precipitation_sum",
    ]
    for key in needed_keys:
        if key not in daily:
            raise Exception("Open-Meteo daily data is missing: " + key)

    rows = []
    for i in range(len(daily["time"])):
        rows.append(
            {
                "date": daily["time"][i],
                "min_temp": daily["temperature_2m_min"][i],
                "max_temp": daily["temperature_2m_max"][i],
                "mean_temp": daily["temperature_2m_mean"][i],
                "precipitation": daily["precipitation_sum"][i],
            }
        )
    return rows


def store_daily_weather(connection, city_id, weather_rows):
    # Write the rows into the database.
    # Delete the old row for the same city and date first, so running
    # the same update twice does not create duplicate rows.
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
            (row["date"], row["min_temp"], row["max_temp"], row["mean_temp"], row["precipitation"], city_id),
        )
    connection.commit()
    return len(weather_rows)


def update_city_weather(connection, city_id, start_date, end_date):
    # The full phase 3 job: find the city, download its weather, store it.
    city = get_city(connection, city_id)
    data = download_weather_data(city, start_date, end_date)
    weather_rows = parse_daily_weather(data)
    count = store_daily_weather(connection, city["id"], weather_rows)
    print("Stored", count, "weather rows for", city["name"] + ".")
    return count


def add_city(connection, name, country_id, latitude, longitude):
    # Extra helper: add a new city, so weather can be downloaded
    # for more places than the four cities that come with the database.
    if name.strip() == "":
        raise ValueError("city name cannot be empty")
    cursor = connection.execute(
        "INSERT INTO cities (name, country_id, latlong) VALUES (?, ?, ?)",
        (name.strip(), country_id, str(latitude) + "," + str(longitude)),
    )
    connection.commit()
    print("Added city", name.strip(), "with id", cursor.lastrowid)
    return cursor.lastrowid


# Running this file directly downloads one example week for city 1.
if __name__ == "__main__":
    connection = connect_database()
    update_city_weather(connection, city_id=1, start_date="2024-01-01", end_date="2024-01-07")
    connection.close()
