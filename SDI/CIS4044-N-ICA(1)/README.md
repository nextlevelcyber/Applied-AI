# CIS4044-N ICA Historical Weather Data

This project implements the three ICA programming phases for the Open-Meteo historical weather data task.

The code is written in a simple script style: plain functions, no classes, and short English comments.

## Contents

- `ICA/phase_1.py`: SQLite queries for countries, cities, temperature, precipitation, and extra analytical queries. Also holds the shared helpers (database connection and date/year validation) that the other phases import.
- `ICA/phase_2.py`: Matplotlib chart generation from the SQLite database.
- `ICA/phase_3.py`: Open-Meteo archive API retrieval and SQLite storage.
- `ICA/main.py`: simple menu entry point.
- `tests/test_weather_app.py`: automated tests (no internet needed).
- `charts/`: generated chart evidence.
- `REPORT_AND_TESTING.xlsx`: report plus black-box testing appendix for submission.
- `REPORT_AND_TESTING.md`: readable source copy of the report.

## Dependencies

Python 3.9+ is recommended.

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

The phase-specific libraries are:

- Phase 1: `sqlite3` (comes with Python).
- Phase 2: `sqlite3` and `matplotlib`.
- Phase 3: `sqlite3` and `requests`.

## Running The Application

All commands below are run from inside the `ICA` folder:

```bash
cd ICA
```

Start the interactive menu:

```bash
python3 main.py
```

Run the offline demo. This performs every Phase 1 query and generates the sample Phase 2 charts without making a network request:

```bash
python3 main.py demo
```

Generate all chart evidence:

```bash
python3 main.py charts
```

To fetch Open-Meteo data and store it for an existing city, use menu option 6.

Each phase file can also be run on its own, for example `python3 phase_1.py`.

City ids in the provided database:

| Id | City | Country |
| --- | --- | --- |
| 1 | Middlesbrough | Great Britain |
| 2 | London | Great Britain |
| 3 | Paris | France |
| 4 | Toulouse | France |

## Chart Details

The chart commands create:

| File | Chart purpose |
| --- | --- |
| `charts/01_7_day_precipitation.png` | 7-day daily precipitation for Middlesbrough. |
| `charts/02_city_precipitation_comparison.png` | Total precipitation comparison across all four cities. |
| `charts/03_country_average_precipitation.png` | Country-level average daily precipitation for 2024. |
| `charts/04_grouped_weather_averages.png` | Grouped city comparison of min, mean, max temperature and precipitation. |
| `charts/05_monthly_min_max_temperature.png` | Daily minimum and maximum temperature line chart for one month. |
| `charts/06_temperature_vs_rainfall.png` | Scatter plot comparing average temperature and rainfall. |

## Running Tests

Run from the project folder (the folder that contains `ICA` and `tests`):

```bash
python3 -m unittest discover -s tests -v
```

The tests cover Phase 1 query outputs, input validation, Phase 2 chart file creation, Phase 3 JSON parsing, and database replacement writes. The Phase 3 tests use hand-made example data instead of the live Open-Meteo service, so no internet connection is needed.
