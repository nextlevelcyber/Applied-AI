# Week 3 Lab Answers - Netflix Dataset

Date updated: 2026-06-27

## Context

This lab practises Power BI data loading, Power Query cleaning, table relationships, and simple dashboard design using the Netflix dataset.

The original dataset in this folder does not include a `release_year` column. To answer the year-based questions, I used `added_year`, extracted from `date_added`. This is a reasonable workaround for the available file, but I should mention it if asked during a demo.

## Data Preparation Completed

- Loaded `netflix_titles.csv`.
- Removed rows with blank `director`.
- Removed rows with blank `cast`.
- Kept `Movie` records only.
- Removed TV Show / Season based rows from the analysis.
- Converted duration into a numeric `duration_minutes` field.
- Created separate output tables for Power BI modelling:
  - `outputs/netflix_main_clean.csv`
  - `outputs/netflix_type.csv`
  - `outputs/netflix_date.csv`

## Relationship Model To Rebuild In Power BI

- `netflix_main_clean[show_id]` to `netflix_type[show_id]`
- `netflix_main_clean[show_id]` to `netflix_date[show_id]`

Expected model shape:

- Main movie table: title, director, cast, country, rating, duration, listed category, description.
- Type table: show ID and Movie type.
- Date table: show ID, date added, extracted year.

## Business Question Answers

| No. | Question | Answer / Current Result | Evidence |
| --- | --- | --- | --- |
| 1 | Which director has made the highest number of Movies? | `Raúl Campos, Jan Suter` with 18 movies. This looks slightly odd because it is a combined director value, so in a stricter model I would split multi-director rows. | `outputs/chart_top_directors.svg` |
| 2 | How many directors have made only one movie? | 1811 directors. This matches the target value in the lab document. | `outputs/week3_question_metrics.csv` |
| 3 | Which directors have made more than 10 movies? | `Raúl Campos, Jan Suter` with 18, and `Marcus Raboy` with 13. | `outputs/week3_question_metrics.csv` |
| 4 | How many movies are released / added in 2020? | 33 movies. | `outputs/movies_by_added_year.csv` |
| 5 | How many 2020 movies have duration greater than 60 minutes? | 32 movies. | `outputs/movies_by_added_year.csv` |
| 6 | Which year has the highest number of movies? | 2019 with 832 movies. | `outputs/chart_movies_by_year.svg` |
| 7 | Which year has the lowest number of movies? | 2020 with 33 movies. | `outputs/chart_movies_by_year.svg` |
| 8 | Map showing movie count by country | Use `country` as location and movie count as bubble size. The top country is United States with 968 movies. | `outputs/movies_by_country.csv` |
| 9 | Movies longer than 60 minutes by year | Use `added_year` on the x-axis and count of titles where `duration_minutes > 60` as values. | `outputs/chart_long_movies_by_year.svg` |
| 10 | Genre slicer | Use `listed_in` as slicer and rename the slicer title to `Genre`. | Power BI slicer setup |
| 11 | Structured dashboard | Use aligned tiles, red/black theme, borders, title, director chart, country chart, year chart, long-duration chart, and genre slicer. | `outputs/dashboard_practice_overview.html` |

## Power BI Rebuild Steps

1. Open Power BI Desktop.
2. Load the three prepared CSV files from `week3/lab/outputs`.
3. Set `duration_minutes` and `added_year` as whole numbers.
4. Create the two `show_id` relationships in Model view.
5. Build the following pages:
   - Model / cleaning check page.
   - Map page: country against movie count or duration variance.
   - Year page: average duration by year, red bars, black average line.
   - Dashboard page: business question overview.
6. Save the file. Current cloud desktop version is saved as `20260627.pbix` in `C:\Users\admin\Desktop\AI\BDBI\week3\lab\`.
7. Export or screenshot the final dashboard and save it in `outputs/`.

## Student Reflection

The main difficulty is that the dataset does not exactly match the wording of the questions because there is no `release_year` column. I solved this by using the year from `date_added`. The director result also shows a common data quality issue: some records contain multiple directors in one text field, so the highest director count may represent a pair rather than one person.

## Evidence Log

The Week 3 evidence package is saved as `week3_evidence_log.docx`. It includes:

- Completion summary for data import, model relationships, PBIX save, and business answers.
- Business question answer table.
- Generated evidence charts for year, country, and director analysis.
- Manual checklist for Power BI screenshots that should be inserted if formal screenshot proof is required.
