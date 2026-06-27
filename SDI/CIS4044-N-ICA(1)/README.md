# CIS4044-N ICA Historical Weather Data

This project implements the three ICA programming phases for the Open-Meteo historical weather data task.

## Contents

- `ICA/phase_1.py`: SQLite queries for countries, cities, temperature, precipitation, and extra analytical queries.
- `ICA/phase_2.py`: Matplotlib chart generation from the SQLite database.
- `ICA/phase_3.py`: Open-Meteo archive API retrieval and SQLite storage.
- `ICA/common.py`: shared connection, validation, and city helper logic.
- `ICA/main.py`: single command-line/menu entry point.
- `tests/test_weather_app.py`: automated regression tests.
- `charts/`: generated chart evidence.
- `REPORT_AND_TESTING.xlsx`: report plus black-box testing appendix for submission.
- `REPORT_AND_TESTING.md`: readable source copy of the report.
- `PRESENTATION_NOTES_ZH.md`: short Chinese speaking notes for explaining the work.

## Dependencies

Python 3.9+ is recommended.

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

The phase-specific libraries are:

- Phase 1: `sqlite3`.
- Phase 2: `sqlite3` and `matplotlib`.
- Phase 3: `sqlite3` and `requests`.

Small Python standard-library helpers are also used for validation, paths, typing, temporary test databases, and command-line handling. They do not replace the required ICA libraries; they support safer input handling and cleaner project structure.

## Running The Application

Run the deterministic demo. This performs Phase 1 queries and generates sample Phase 2 charts without making a network request:

```bash
python3 -m ICA.main demo
```

Run the interactive menu:

```bash
python3 -m ICA.main menu
```

Generate all chart evidence:

```bash
python3 -m ICA.main charts
```

Fetch Open-Meteo data and store it for an existing city:

```bash
python3 -m ICA.main update-weather 1 2024-01-01 2024-01-07
```

City ids in the provided database:

| Id | City | Country |
| --- | --- | --- |
| 1 | Middlesbrough | Great Britain |
| 2 | London | Great Britain |
| 3 | Paris | France |
| 4 | Toulouse | France |

## Chart Details

The sample chart command creates:

| File | Chart purpose |
| --- | --- |
| `charts/01_7_day_precipitation.png` | 7-day daily precipitation for Middlesbrough. |
| `charts/02_city_precipitation_comparison.png` | Total precipitation comparison across all four cities. |
| `charts/03_country_average_precipitation.png` | Country-level average daily precipitation for 2024. |
| `charts/04_grouped_weather_averages.png` | Grouped city comparison of min, mean, max temperature and precipitation. |
| `charts/05_monthly_min_max_temperature.png` | Daily minimum and maximum temperature line chart for one month. |
| `charts/06_temperature_vs_rainfall.png` | Scatter plot comparing average temperature and rainfall. |

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

The tests cover Phase 1 query outputs, input validation, Phase 2 chart file creation, Phase 3 JSON parsing, network error handling, and database replacement writes. Phase 3 network tests use mocks so the test suite does not depend on the live Open-Meteo service.

