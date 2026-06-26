# SDI ICA Database Reference

Created: 2026-06-26

This reference records the observed structure of the provided SQLite database so the ICA work can be planned manually.

Database path:

`SDI/CIS4044-N-ICA(1)/db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db`

## Tables

### countries

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER | yes | Primary key |
| name | TEXT | yes | Country name |
| timezone | TEXT | yes | Timezone string |

Observed rows:

- Great Britain, Europe/London
- France, Europe/Berlin

### cities

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER | yes | Primary key |
| name | TEXT | yes | City name |
| country_id | INTEGER | yes | References `countries.id` |
| latlong | TEXT | no | Latitude/longitude string |

Observed cities:

- Middlesbrough
- London
- Paris
- Toulouse

### daily_weather_entries

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER | yes | Primary key |
| date | TEXT | yes | Date as text, observed format `YYYY-MM-DD` |
| min_temp | REAL | yes | Minimum temperature |
| max_temp | REAL | yes | Maximum temperature |
| mean_temp | REAL | no | Mean temperature, default `0.0` |
| precipitation | REAL | no | Precipitation, default `0.0` |
| city_id | INTEGER | yes | References `cities.id` |

Observed date range:

- 2020-01-01 to 2024-12-31

Observed row count:

- `daily_weather_entries`: 7308 rows

## Relationship Sketch

```text
countries.id 1 --- many cities.country_id
cities.id    1 --- many daily_weather_entries.city_id
```

## Manual Query Planning Notes

- For country-level outputs, join `countries -> cities -> daily_weather_entries`.
- For city-level outputs, join `cities -> daily_weather_entries`.
- For year filters, use date text patterns or date functions carefully.
- Format real/float numbers to 2 decimal places in console output, as the specification notes.
