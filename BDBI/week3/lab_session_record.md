# Week 3 Lab Session Record - Netflix Dataset

Date started: 2026-06-27

## Lab Files

- `Challenge 1.1 - Netflix Dataset.docx`
- `Data Analytics - Netflix Dataset.docx`
- `netflix_titles.csv`

## Required Work

### Part A - Power Query And Model

- Import `netflix_titles.csv` as a CSV file.
- Remove rows where `director` is blank.
- Remove rows where `cast` is blank.
- Duplicate/reference the Netflix table to create a `Type` table with:
  - `show_id`
  - `type`
- Remove `type` from the main Netflix table.
- Create a `Date` table with:
  - `show_id`
  - `date_added`
- Remove `date_added` from the main Netflix table.
- Create/check one-to-one relationships:
  - `Netflix_titles[show_id]` to `Type[show_id]`
  - `Netflix_titles[show_id]` to `Date[show_id]`
- Filter out TV Shows so the report focuses on movies.
- Remove rows where `duration` contains `Season`.
- Remove `min` from `duration`.
- Change `duration` to whole number.

### Part B - Required Visuals

- Map showing variance of duration by country.
- Bar chart showing duration by year with an average line.
- Dashboard answering the 11 business questions from the lab document.

## Data Note

The provided `netflix_titles.csv` does not include a `release_year` column. For the lab questions that ask about release year, I will use the year extracted from `date_added` as the available year field and note this limitation.

## Generated Local Outputs

Saved under `BDBI/week3/lab/outputs/`:

- `netflix_main_clean.csv` - cleaned main Netflix movie table, with `type` and `date_added` removed.
- `netflix_type.csv` - relationship table with `show_id` and `type`.
- `netflix_date.csv` - relationship table with `show_id`, `date_added`, and extracted `added_year`.
- `week3_question_metrics.csv` - checked answers for the lab questions.
- `movies_by_added_year.csv` - movie count by extracted year, including count where duration is greater than 60 minutes.
- `movies_by_country.csv` - movie count by country for map/dashboard work.
- `chart_top_directors.svg` - practice visual for the director count question.
- `chart_movies_by_year.svg` - practice visual for movie count by available year.
- `chart_duration_by_year_average_line.svg` - practice visual matching the required red bar chart with an average line.
- `chart_long_movies_by_year.svg` - practice visual for movies longer than 60 minutes by year.
- `chart_movies_by_country_top15.svg` - practice visual for country-based analysis.
- `dashboard_practice_overview.html` - simple local dashboard layout reference.
- `lab_answers.md` - written answers and Power BI rebuild steps.
- `evidence/02_movies_by_year.png` - Word-ready chart for movie count by available year.
- `evidence/03_top_countries.png` - Word-ready chart for country ranking.
- `evidence/04_top_directors.png` - Word-ready chart for director ranking.
- `week3_evidence_log.docx` - Word evidence log with completion summary, business answers, generated charts, and manual Power BI screenshot checklist.

## Checked Answers From The Raw CSV

Using the same core cleaning rules as the lab:

- Rows after removing blank director/cast, keeping Movies only, and converting duration: 2311.
- Director with highest number of movies: `Raúl Campos, Jan Suter` with 18 movies.
- Directors with exactly one movie: 1811.
- Directors with more than 10 movies:
  - `Raúl Campos, Jan Suter`: 18.
  - `Marcus Raboy`: 13.
- Movies added in 2020: 33.
- Movies added in 2020 with duration greater than 60 minutes: 32.
- Highest movie count by available year: 2019 with 832 movies.
- Lowest movie count by available year: 2020 with 33 movies.
- Top country by movie count: United States with 968 movies.

## Power BI Build Checklist

Use `netflix_titles.csv` if building the full Power Query process from scratch, or use the generated `outputs/*.csv` files if rebuilding the report quickly.

1. Load the CSV data.
2. In Power Query, remove blank `director` and `cast` rows.
3. Keep Movie records only.
4. Clean `duration` by removing `min`, then convert it to whole number.
5. Create or import the `Type` and `Date` tables.
6. Connect tables by `show_id`.
7. Add `added_year` from `date_added` because this CSV has no `release_year`.
8. Create visuals:
   - Director count table/bar.
   - Directors with one movie.
   - Directors with more than 10 movies.
   - 2020 movie count and 2020 duration greater than 60 count.
   - Map/count by country.
   - Bar chart by year with the average line.
   - Genre slicer using `listed_in`.

## Evidence To Save

- Screenshot of imported CSV fields.
- Screenshot of Power Query cleaning steps.
- Screenshot of three-table model view and relationships.
- Screenshot of map visual.
- Screenshot of duration-by-year visual with average line.
- Screenshot of final dashboard.
- Final `.pbix` saved in the Week 3 lab folder.

## Status

- [x] Lab task requirements extracted from Blackboard files.
- [x] Dataset inspected locally.
- [x] Cleaned output tables generated locally.
- [x] Lab question metrics generated locally.
- [x] Practice charts generated locally.
- [x] Business question answers documented.
- [x] Week 3 files transferred/extracted on the Windows cloud desktop.
- [x] Power BI Desktop opened on the Windows cloud desktop.
- [x] Power BI reached the `Get Data > Text/CSV` connector selection step.
- [x] Windows file picker opened for Text/CSV import.
- [x] `netflix_main_clean.csv` imported into Power BI.
- [x] `netflix_type.csv` imported into Power BI.
- [x] `netflix_date.csv` imported into Power BI.
- [x] Power BI file created and saved on the Windows cloud desktop.
- [x] Model relationships checked in Power BI Model view.
- [x] Word evidence log created and checked in Microsoft Word.
- [ ] Power BI screenshots inserted manually.
- [x] Final dashboard evidence prepared using generated local charts and business answer table.

## Cloud Desktop Note

Attempted to use the Aliyun Wuying Windows desktop on 2026-06-27. The desktop is reachable, and Power BI is available there. The Wuying file transfer tool successfully uploaded `BDBI_week3_transfer.zip` to the Windows Downloads folder. User confirmed the transfer/extraction step is OK.

Current cloud desktop state:

- `C:\Users\admin\Desktop\AI\BDBI\week3\` is present after extraction.
- Power BI Desktop is open and has loaded the three prepared CSV tables:
  - `netflix_main_clean`
  - `netflix_type`
  - `netflix_date`
- The file has been saved in `C:\Users\admin\Desktop\AI\BDBI\week3\lab\` as `20260627.pbix`.
- The intended descriptive name was `BDBI_week3_netflix_lab.pbix`, but the remote Windows input method interfered with English text entry. A numeric filename was used to save the work reliably.
- Power BI Model view confirmed two active one-to-one relationships using `show_id`.
- macOS screenshot capture was blocked by system permission, so the Word evidence log includes a manual screenshot checklist instead of generated/fake screenshots.

Next practical step on the cloud computer is only to manually capture/insert the Power BI screenshots if formal visual proof is required. The data import, model relationship check, saved PBIX, local charts, and written answers are complete.
