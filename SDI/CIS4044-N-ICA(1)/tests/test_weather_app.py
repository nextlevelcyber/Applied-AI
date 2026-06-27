"""Regression tests for the historical weather ICA application."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from ICA.common import DEFAULT_DB_PATH, connect_database, get_city, validate_date, validate_date_range
from ICA.phase_1 import (
    average_annual_temperature,
    average_mean_temp_by_city,
    average_seven_day_precipitation,
    select_all_cities,
    select_all_countries,
)
from ICA.phase_2 import plot_seven_day_precipitation
from ICA.phase_2 import plot_precipitation_for_cities
from ICA.phase_3 import (
    WeatherApiError,
    build_archive_params,
    fetch_open_meteo_archive,
    parse_daily_weather,
    store_daily_weather,
)


class PhaseOneQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = connect_database(DEFAULT_DB_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_select_all_countries_returns_two_countries(self):
        rows = select_all_countries(self.connection)
        self.assertEqual(len(rows), 2)

    def test_select_all_cities_returns_four_cities(self):
        rows = select_all_cities(self.connection)
        self.assertEqual(len(rows), 4)

    def test_average_annual_temperature_returns_two_decimal_capable_float(self):
        rows = average_annual_temperature(self.connection, city_id=1, year=2024)
        self.assertEqual(len(rows), 1)
        self.assertIsInstance(rows[0]["average_mean_temp"], float)

    def test_average_seven_day_precipitation_counts_seven_rows(self):
        rows = average_seven_day_precipitation(self.connection, city_id=1, start_date="2024-01-01")
        self.assertEqual(rows[0]["days_found"], 7)

    def test_average_mean_temp_by_city_returns_one_row_per_city(self):
        rows = average_mean_temp_by_city(self.connection, "2024-01-01", "2024-12-31")
        self.assertEqual(len(rows), 4)

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_date("2024-99-99")

    def test_reversed_date_range_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_date_range("2024-02-01", "2024-01-01")


class PhaseTwoChartTests(unittest.TestCase):
    def test_chart_file_is_created(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "precipitation.png"
            with connect_database(DEFAULT_DB_PATH) as connection:
                result = plot_seven_day_precipitation(connection, 1, "2024-01-01", output_path)
            self.assertTrue(result.exists())
            self.assertGreater(result.stat().st_size, 0)

    def test_empty_city_list_is_rejected(self):
        with connect_database(DEFAULT_DB_PATH) as connection:
            with self.assertRaises(ValueError):
                plot_precipitation_for_cities(connection, [], "2024-01-01", "2024-01-31")


class PhaseThreeApiAndStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "weather.db"
        shutil.copy(DEFAULT_DB_PATH, self.db_path)
        self.connection = connect_database(self.db_path)

    def tearDown(self):
        self.connection.close()
        self.temp_dir.cleanup()

    def test_parse_daily_weather_returns_insertable_rows(self):
        payload = {
            "daily": {
                "time": ["2025-01-01", "2025-01-02"],
                "temperature_2m_min": [1.0, 2.0],
                "temperature_2m_max": [6.0, 7.0],
                "temperature_2m_mean": [3.5, 4.5],
                "precipitation_sum": [0.0, 1.2],
            }
        }
        rows = parse_daily_weather(payload)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["precipitation"], 1.2)

    def test_build_archive_params_rejects_reversed_dates(self):
        city = get_city(self.connection, 1)
        with self.assertRaises(ValueError):
            build_archive_params(city, "2024-02-01", "2024-01-01")

    def test_store_daily_weather_replaces_existing_city_date_rows(self):
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
        count = self.connection.execute(
            "SELECT COUNT(*) FROM daily_weather_entries WHERE city_id = 1 AND date = '2024-01-01'"
        ).fetchone()[0]
        self.assertEqual(count, 1)
        mean_temp = self.connection.execute(
            "SELECT mean_temp FROM daily_weather_entries WHERE city_id = 1 AND date = '2024-01-01'"
        ).fetchone()[0]
        self.assertEqual(mean_temp, 11.0)

    @patch("requests.get")
    def test_fetch_open_meteo_archive_uses_direct_request(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "daily": {
                "time": [],
                "temperature_2m_min": [],
                "temperature_2m_max": [],
                "temperature_2m_mean": [],
                "precipitation_sum": [],
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        city = get_city(self.connection, 1)
        payload = fetch_open_meteo_archive(city, "2024-01-01", "2024-01-02")
        self.assertIn("daily", payload)
        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args.kwargs["params"]["timezone"], "Europe/London")

    @patch("requests.get")
    def test_fetch_open_meteo_archive_wraps_network_errors(self, mock_get):
        mock_get.side_effect = requests.Timeout("simulated timeout")
        city = get_city(self.connection, 1)
        with self.assertRaises(WeatherApiError):
            fetch_open_meteo_archive(city, "2024-01-01", "2024-01-02")

    def test_missing_daily_payload_raises_weather_api_error(self):
        with self.assertRaises(WeatherApiError):
            parse_daily_weather({"not_daily": {}})


if __name__ == "__main__":
    unittest.main()
