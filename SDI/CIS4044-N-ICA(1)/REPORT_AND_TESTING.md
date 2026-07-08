# Historical Weather Data ICA Report

Submission note: `REPORT_AND_TESTING.xlsx` is the formatted submission copy. This Markdown file is retained as a readable source version.

## 1. Introduction

This project implements a Python application for processing historical weather data from the supplied SQLite database and the Open-Meteo archive API. The work is organised into three phases: database querying, chart generation, and API retrieval/storage. Each phase is a plain script of small functions. `ICA/phase_1.py` also holds the shared helpers (database connection and date/year validation), which `phase_2.py` and `phase_3.py` import, while `ICA/main.py` provides a simple demo/menu entry point. This structure keeps every file easy to read from top to bottom while avoiding repeated connection and validation code.

## 2. Software Tools

SQLite is appropriate because the dataset is relational, local, and modest in size. It supports joins, grouping, date filtering, and aggregates, which are central to the temperature and precipitation queries. Its limitation is scalability: a production weather platform with concurrent users would need a server database and stronger migration controls.

Matplotlib is used for Phase 2 because it can generate reproducible PNG evidence without requiring a web dashboard. The charts include daily precipitation, city comparisons, country averages, grouped weather metrics, a min/max line chart, and a temperature/rainfall scatter plot. Matplotlib gives good control over labels and exported files, although it requires more manual layout work than higher-level visualisation packages.

Requests is used for Phase 3 because it allows direct HTTP request handling. The application builds Open-Meteo parameters itself, sets timezone, applies a timeout, and validates the JSON response before storage. This is suitable for the ICA requirement to write custom API request code. The main limitation is that live API calls can fail due to network problems, service changes, or malformed responses.

Visual Studio Code is useful for Python editing, terminal runs, source control, and database inspection extensions. However, an editor does not prove correctness, so the project also includes automated tests and chart evidence.

## 3. Security And Risk

The main risks are invalid input, SQL injection, dependency risk, duplicate data, and external API failure. SQL values are passed through placeholders rather than string concatenation. Dates and years are validated, including reversed date ranges, before database queries or API calls are made. City lists used in chart queries are converted to integers before SQL placeholder generation.

Third-party packages introduce maintenance risk. `requirements.txt` declares `matplotlib` and `requests`, but a production system should also pin versions, monitor vulnerabilities, and use controlled deployment. The solution uses only `sqlite3` for Phase 1 database work, `sqlite3` plus `matplotlib` for Phase 2 visualisation, and `requests` for Phase 3 API access. Other standard-library modules are limited to date validation, file paths, and temporary test databases.

Open-Meteo dependency is another risk. The parser checks that every required field is present before inserting data. Network errors are caught and re-raised with a clear message, and the automated tests use hand-made example data instead of live API calls so the test suite remains reliable. Database updates delete the same city/date row before inserting refreshed data, reducing duplicate record risk. A production schema would further improve this with a unique constraint on `(city_id, date)`.

## 4. Programming Concepts And Data Structures

The solution uses small functions with clear responsibilities: query functions return rows, chart functions save PNG files, API functions build parameters and parse JSON, and storage functions update SQLite. Lists hold query results and parsed weather rows. Dictionaries represent parsed API records using named fields such as `date`, `mean_temp`, and `precipitation`. A simple dictionary also carries the city id, name, latitude, longitude, and timezone required by Open-Meteo, which is clearer than passing separate values through several functions.

Exception handling is used for invalid dates, unknown cities, malformed API payloads, and network failures. Automated tests use `unittest`, temporary database copies, and hand-made example API data. This protects the supplied database while checking behaviour from the outside: expected rows, generated files, rejected invalid input, and stable error handling.

## 5. Conclusion

The application meets the ICA requirements by implementing SQLite queries, Matplotlib visualisations, Open-Meteo retrieval, database storage, a reusable code structure, a CLI/menu entry point, and repeatable tests. The design is intentionally small, but it demonstrates relational querying, validation, structured data, external API use, chart evidence, and black-box style testing.

## References

Hunter, J.D. (2007) 'Matplotlib: A 2D graphics environment', *Computing in Science and Engineering*, 9(3), pp. 90-95.

Open-Meteo (2024) *Historical Weather API documentation*. Available at: https://open-meteo.com/en/docs/historical-weather-api (Accessed: 27 June 2026).

Python Software Foundation (2024) *sqlite3: DB-API 2.0 interface for SQLite databases*. Available at: https://docs.python.org/3/library/sqlite3.html (Accessed: 27 June 2026).

Requests (2024) *Requests: HTTP for Humans documentation*. Available at: https://requests.readthedocs.io/ (Accessed: 27 June 2026).

SQLite Consortium (2024) *About SQLite*. Available at: https://www.sqlite.org/about.html (Accessed: 27 June 2026).

# Appendix A: Black-Box Test Plan

| Test ID | Phase | Feature/function | Input | Expected result | Actual result | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- |
| BB-001 | Phase 1 | List countries | `select_all_countries` | Two countries shown | 2 rows returned | PASS |
| BB-002 | Phase 1 | List cities | `select_all_cities` | Four cities shown | 4 rows returned | PASS |
| BB-003 | Phase 1 | Annual temperature | City 1, 2024 | One average temperature | One float result | PASS |
| BB-004 | Phase 1 | Seven-day precipitation | City 1, `2024-01-01` | 7 days counted | `days_found = 7` | PASS |
| BB-005 | Phase 1 | Invalid date | `2024-99-99` | Validation error | `ValueError` raised | PASS |
| BB-006 | Phase 1/2/3 | Reversed date range | `2024-02-01` to `2024-01-01` | Validation error | `ValueError` raised | PASS |
| BB-007 | Phase 2 | Chart creation | 7-day precipitation chart | PNG created | Non-empty PNG created | PASS |
| BB-008 | Phase 2 | Empty city list | `[]` | Validation error | `ValueError` raised | PASS |
| BB-009 | Phase 2 | Full chart evidence | `python3 main.py charts` | Six charts generated | Six PNG files created | PASS |
| BB-010 | Phase 3 | Parse API JSON | Example two-day payload | Two weather rows | 2 rows parsed | PASS |
| BB-011 | Phase 3 | Replace existing row | Same city/date | One updated row remains | Count 1, value updated | PASS |
| BB-012 | Phase 3 | Missing daily data | Payload without `daily` block | Controlled API error | Clear error raised | PASS |
| BB-013 | Menu | Demo command | `python3 main.py demo` | Queries print and charts save | Demo completed | PASS |

