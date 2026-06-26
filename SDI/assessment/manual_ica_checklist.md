# Manual ICA Checklist

Created: 2026-06-26

Use this while implementing the official ICA yourself.

## Before Coding

- [ ] Re-read the ICA specification.
- [ ] Confirm the official deadline on Blackboard.
- [ ] Open the starter project in VS Code.
- [ ] Make a backup branch or copy before editing.
- [ ] Confirm `phase_1.py`, `phase_2.py`, and `phase_3.py` run without syntax errors before changes.

## Phase 1 - SQLite Queries

Allowed library: `sqlite3`.

- [ ] Fill in your name and student ID.
- [ ] Implement `select_all_cities`.
- [ ] Implement `average_annual_temperature`.
- [ ] Implement `average_seven_day_precipitation`.
- [ ] Implement `average_mean_temp_by_city`.
- [ ] Implement `average_annual_precipitation_by_country`.
- [ ] Add your own higher-level query ideas only after required queries work.
- [ ] Manually check printed formatting to 2 decimal places.
- [ ] Save console output evidence.

## Phase 2 - Matplotlib

Allowed libraries: `sqlite3`, `matplotlib`.

- [ ] Decide which required charts to produce.
- [ ] Query data from SQLite.
- [ ] Produce chart outputs.
- [ ] Label axes, titles, legends, and units clearly.
- [ ] Save chart images for report evidence.
- [ ] Record what each chart shows.

## Phase 3 - Open-Meteo API

Expected library: `requests` for custom HTTP requests.

- [ ] Read Open-Meteo archive API documentation manually.
- [ ] Identify city coordinates and dates.
- [ ] Send a request manually from your code.
- [ ] Validate status code and response data.
- [ ] Insert/update database rows safely.
- [ ] Re-query database to confirm data was stored.

## Report

- [ ] Explain tools used and why they were appropriate.
- [ ] Discuss limitations of the tools/libraries.
- [ ] Evaluate security and risk implications.
- [ ] Include code snippets only where useful.
- [ ] Include black-box testing appendix.
- [ ] Use Harvard references.

## Submission Package

- [ ] Source code workspace.
- [ ] README with run instructions.
- [ ] Report and black-box testing document.
- [ ] Any required supporting files.
