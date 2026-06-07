import io
import sqlite3
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ICA_DIR = PROJECT_ROOT / "CIS" / "CIS4044-N-ICA" / "ICA"
DB_PATH = (
    PROJECT_ROOT
    / "CIS"
    / "CIS4044-N-ICA"
    / "db"
    / "CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
)

sys.path.insert(0, str(ICA_DIR))

import phase_1  # noqa: E402


class Phase1QueryTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row

    def tearDown(self):
        self.connection.close()

    def capture_output(self, function, *args):
        stream = io.StringIO()
        with redirect_stdout(stream):
            function(self.connection, *args)
        return stream.getvalue()

    def test_average_annual_temperature_prints_city_year_and_value(self):
        output = self.capture_output(
            phase_1.average_annual_temperature,
            1,
            2020,
        )

        self.assertIn("Middlesbrough", output)
        self.assertIn("2020", output)
        self.assertIn("27.36", output)

    def test_average_seven_day_precipitation_prints_average_value(self):
        output = self.capture_output(
            phase_1.average_seven_day_precipitation,
            1,
            "2020-01-01",
        )

        self.assertIn("Middlesbrough", output)
        self.assertIn("2020-01-01", output)
        self.assertIn("2020-01-07", output)
        self.assertIn("4.90", output)

    def test_average_mean_temp_by_city_prints_all_city_averages(self):
        output = self.capture_output(
            phase_1.average_mean_temp_by_city,
            "2020-01-01",
            "2020-01-07",
        )

        self.assertIn("London", output)
        self.assertIn("27.20", output)
        self.assertIn("Middlesbrough", output)
        self.assertIn("26.96", output)
        self.assertIn("Paris", output)
        self.assertIn("27.01", output)
        self.assertIn("Toulouse", output)
        self.assertIn("29.53", output)

    def test_average_annual_precipitation_by_country_prints_country_averages(self):
        output = self.capture_output(
            phase_1.average_annual_precipitation_by_country,
            2020,
        )

        self.assertIn("France", output)
        self.assertIn("1.56", output)
        self.assertIn("Great Britain", output)
        self.assertIn("3.03", output)


if __name__ == "__main__":
    unittest.main()
