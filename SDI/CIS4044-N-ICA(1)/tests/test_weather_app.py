# Simple tests for the weather application.
# Run them from the project folder with:
#   python3 -m unittest discover -s tests -v
#
# No internet is needed: the phase 3 tests use hand-made example data
# instead of calling the real Open-Meteo API.

import os
import shutil
import sys
import tempfile
import unittest

# The application code lives in the ICA folder, so add that folder
# to the import path before importing from it.
TESTS_FOLDER = os.path.dirname(os.path.abspath(__file__))
PROJECT_FOLDER = os.path.dirname(TESTS_FOLDER)
sys.path.insert(0, os.path.join(PROJECT_FOLDER, "ICA"))

from phase_1 import (
    DB_PATH,
    connect_database,
    validate_date,
    validate_date_range,
    select_all_countries,
    select_all_cities,
    average_annual_temperature,
    average_seven_day_precipitation,
    average_mean_temp_by_city,
)
from phase_2 import plot_seven_day_precipitation, plot_precipitation_for_cities
from phase_3 import get_city, parse_daily_weather, store_daily_weather


class TestPhase1Queries(unittest.TestCase):
    # initialize the database connection.
    def setUp(self):
        self.connection = connect_database()

    # close the database connection when tests all complete
    def tearDown(self):
        self.connection.close()

    def test_select_all_countries_returns_two_countries(self):
        rows = select_all_countries(self.connection)
        self.assertEqual(len(rows), 2)

    def test_select_all_cities_returns_four_cities(self):
        rows = select_all_cities(self.connection)
        self.assertEqual(len(rows), 4)

    def test_average_annual_temperature_returns_a_number(self):
        rows = average_annual_temperature(self.connection, city_id=1, year=2024)
        self.assertEqual(len(rows), 1)
        self.assertIsInstance(rows[0]["average_mean_temp"], float)

    def test_average_seven_day_precipitation_finds_seven_days(self):
        rows = average_seven_day_precipitation(self.connection, city_id=1, start_date="2024-01-01")
        self.assertEqual(rows[0]["days_found"], 7)

    def test_average_mean_temp_by_city_returns_one_row_per_city(self):
        rows = average_mean_temp_by_city(self.connection, "2024-01-01", "2024-12-31")
        self.assertEqual(len(rows), 4)

    def test_bad_date_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_date("2024-99-99")

    def test_reversed_date_range_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_date_range("2024-02-01", "2024-01-01")


class TestPhase2Charts(unittest.TestCase):
    def setUp(self):
        self.connection = connect_database()

    def tearDown(self):
        self.connection.close()

    def test_chart_file_is_created(self):
        with tempfile.TemporaryDirectory() as temp_folder:
            output_path = os.path.join(temp_folder, "precipitation.png")
            result = plot_seven_day_precipitation(self.connection, 1, "2024-01-01", output_path)
            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 0)

    def test_empty_city_list_is_rejected(self):
        with self.assertRaises(ValueError):
            plot_precipitation_for_cities(self.connection, [], "2024-01-01", "2024-01-31")


class TestPhase3ParseAndStore(unittest.TestCase):
    def setUp(self):
        # Work on a temporary copy of the database,
        # so the tests never change the real data.
        self.temp_folder = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_folder.name, "weather.db")
        shutil.copy(DB_PATH, self.db_path)
        self.connection = connect_database(self.db_path)

    def tearDown(self):
        self.connection.close()
        self.temp_folder.cleanup()

    def test_get_city_returns_city_details(self):
        city = get_city(self.connection, 1)
        self.assertEqual(city["name"], "Middlesbrough")
        self.assertEqual(city["timezone"], "Europe/London")

    def test_get_city_rejects_unknown_id(self):
        with self.assertRaises(ValueError):
            get_city(self.connection, 999)

    def test_parse_daily_weather_returns_rows(self):
        example_data = {
            "daily": {
                "time": ["2025-01-01", "2025-01-02"],
                "temperature_2m_min": [1.0, 2.0],
                "temperature_2m_max": [6.0, 7.0],
                "temperature_2m_mean": [3.5, 4.5],
                "precipitation_sum": [0.0, 1.2],
            }
        }
        rows = parse_daily_weather(example_data)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["precipitation"], 1.2)

    def test_parse_daily_weather_rejects_missing_daily_data(self):
        with self.assertRaises(Exception):
            parse_daily_weather({"not_daily": {}})

    def test_store_daily_weather_replaces_the_old_row(self):
        rows = [
            {
                "date": "2024-01-01",
                "min_temp": 10.0,
                "max_temp": 12.0,
                "mean_temp": 11.0,
                "precipitation": 2.0,
            }
        ]
        stored = store_daily_weather(self.connection, 1, rows)
        self.assertEqual(stored, 1)

        # There must still be exactly one row for this city and date,
        # and it must hold the new value.
        count = self.connection.execute(
            "SELECT COUNT(*) FROM daily_weather_entries WHERE city_id = 1 AND date = '2024-01-01'"
        ).fetchone()[0]
        self.assertEqual(count, 1)
        mean_temp = self.connection.execute(
            "SELECT mean_temp FROM daily_weather_entries WHERE city_id = 1 AND date = '2024-01-01'"
        ).fetchone()[0]
        self.assertEqual(mean_temp, 11.0)


if __name__ == "__main__":
    unittest.main()
