# SDI Component 2 ICA Notes

Assignment title: Historical Weather Data  
Module: Software for Digital Innovation (CIS4044-N)  
Module leader in specification: Steven Mead  
Submission method: Online via Blackboard  
AI permission: Red

## Deadline

No confirmed deadline is currently visible. The specification has blank deadline fields, and Blackboard Calendar/Gradebook do not currently list the summative ICA due date.

## Assessment Brief

Develop a Python application to process historical weather data using a provided partially populated SQLite3 database and the Open-Meteo archive API.

The provided database contains:

- `countries`: 2 rows
- `cities`: 4 rows
- `daily_weather_entries`: 7308 rows
- Date range: 2020-01-01 to 2024-12-31
- Cities: London, Middlesbrough, Paris, Toulouse

## Phases

Phase 1: Query and process data stored in the local SQLite3 database. Only the `sqlite3` library is allowed for this phase.

Phase 2: Generate charts using Matplotlib from data stored in SQLite3. Only `sqlite3` and `matplotlib` are allowed for this phase.

Phase 3: Retrieve historical data from Open-Meteo and update the SQLite database. For Merit/Distinction level work, the specification says to write your own HTTP request using `requests`, rather than relying on the Open-Meteo example library.

## Marking Breakdown

- Python solution structure: 10%
- Phase 1 database queries: 15%
- Phase 2 database queries and Matplotlib graphs: 15%
- Phase 3 data retrieval and storage: 30%
- Further enhancements: 10%
- Report and testing: 20%

## Report and Testing

The assessment asks for an individual report of around 1000 words, plus black-box testing evidence. The report should examine the software tools used, their appropriateness and limitations, and security/risk implications of libraries and tools.

Do not generate the assessed report with AI because the module permission is Red.
