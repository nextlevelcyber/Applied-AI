# SDI ICA Demo Script (approx. 5 minutes)

Scope: CIS4044-N (Software for Digital Innovation) ICA demo/presentation script.
Project: `CIS4044-N-ICA(1)/` — Historical Weather Data (Open-Meteo dataset).

***

## 1. Opening (\~20s)

Hi everyone, today I'll be presenting my ICA project for the SDI module, titled Historical Weather Data. It's built on the Open-Meteo open weather data source, using Python and SQLite3 to implement a system for querying, visualising, and live-fetching historical weather data. The project is split into three phases, and I'll walk through them in order.

## 2. How the marks break down (\~20s)

Phase 1 is SQL querying, worth 15%. Phase 2 is charting with Matplotlib, worth 15%. Phase 3 carries the most weight at 30%, requiring live retrieval from Open-Meteo's historical archive — and using the official sample code as-is caps the grade at a Pass, so I re-implemented that layer myself with the `requests` library to reach a higher grade band.

【Switch to File Explorer or VS Code here, showing the `ICA/` folder structure】

## 3. Code architecture (\~40s)

The code lives in the `ICA/` folder across four files, all written as simple scripts of plain functions — no classes: `phase_1.py` contains all the SQL query functions, including average annual temperature and seven-day precipitation by city, plus a bonus "wettest city per year" query (it first lists the years, then for each year sorts cities by total precipitation and takes the top one); it also holds the shared helpers like the database connection and date validation, which the other phases import; `phase_2.py` uses Matplotlib to generate six charts; `phase_3.py` handles calling the API, parsing the response, and writing it to the database — I implemented a delete-then-insert approach for deduplication there; and `main.py` is the entry point: it opens an interactive menu by default, or runs everything at once with the `demo` or `charts` argument.

## 4. Database design (\~20s)

The database is SQLite, with three tables: `countries`, `cities`, and `daily_weather_entries` for the actual weather records, linked by foreign keys. It currently covers 2 countries, 4 cities, and 2020–2024 data — just over 7,300 rows in total. Every query is written with parameterised SQL to avoid injection risk.

## 5. Live demo (\~90s)

Let me actually run it now.

【Switch to the terminal, run `python main.py demo`, showing Phase 1 query output printed to the console】

This is demo mode — it runs through the core Phase 1 queries, and you can see the average temperature and precipitation per city, per year, coming back correctly.

【Run `python main.py charts`, then open the `charts/` folder to show the generated PNG files】

This step calls the Phase 2 plotting functions and generates six charts into the `charts/` folder, including a precipitation trend chart and a temperature scatter plot — all drawn from real data in the database.

【Run `python main.py` to open the menu, choose option 6, showing a live fetch from Open-Meteo and the write-back to the database】

This is Phase 3 — it makes a real request to the Open-Meteo archive API, parses the returned daily-weather JSON, and writes it back to the database. If a record already exists, it deletes the old one first and inserts the new one, so there's no duplication.

## 6. Testing (\~30s)

For testing, I wrote 14 unit tests covering the queries, the chart generation, and the API parsing plus storage logic across all three phases — the API tests use hand-made example data instead of real network requests, and all 14 pass. On top of that, the report documents 13 black-box test cases covering normal, boundary, and invalid inputs, and those all pass as well.

## 7. Design trade-offs and current status (\~30s)

Two design decisions worth calling out: I insisted on writing my own `requests`-based logic for Phase 3 instead of using the official sample, specifically to reach a higher grade band; and deduplication is handled with a delete-then-insert pattern rather than a database unique constraint, which is one area that could still be improved. Of the optional enhancements, I only implemented the command-line interface. Overall, all three phases are implemented and passing their tests — the written report is slightly under the target word count, which I'll top up.

## 8. Closing (\~10s)

That's the overall implementation and demo for my ICA. Thank you, and I'm happy to take questions.

***

## Timing and length check

- Estimated total: about 5 minutes; the live-demo section (Part 5) is where actual command run-time adds variability, so it's the part most likely to run long.
- If time is tight, Part 3 (Code architecture) and Part 7 (Design trade-offs) compress the most easily.
- If asked for more detail: `get_city()` in `phase_3.py` joins the `cities` and `countries` tables and returns a plain dictionary; the deduplication approach has no unique constraint, so concurrent writes could in theory still collide — a good answer to keep in reserve for "what would you improve with more time?".

