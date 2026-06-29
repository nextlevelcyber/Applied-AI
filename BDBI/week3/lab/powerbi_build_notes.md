# Week 3 Power BI Build Notes

Date prepared: 2026-06-27

## Files To Use

- Full lab process: `netflix_titles.csv`
- Faster rebuild:
  - `outputs/netflix_main_clean.csv`
  - `outputs/netflix_type.csv`
  - `outputs/netflix_date.csv`
  - `outputs/movies_by_added_year.csv`
  - `outputs/movies_by_country.csv`

## Model

- Main table: `netflix_main_clean`
- Type table: `netflix_type`
- Date table: `netflix_date`
- Relationship keys:
  - `netflix_main_clean[show_id]` to `netflix_type[show_id]`
  - `netflix_main_clean[show_id]` to `netflix_date[show_id]`

## Visuals

- Map: country against duration variance or movie count.
- Bar chart: duration by `added_year`, red bars, average line.
- Director chart/table: movie count by director.
- Filter/slicer: `listed_in`, renamed visually as Genre.
- KPI/card examples:
  - Movies in 2020: 33.
  - Movies in 2020 and duration > 60: 32.
  - Directors with one movie: 1811.

## Important Note

This CSV does not contain `release_year`. For the year-based lab questions, use `added_year`, extracted from `date_added`, and mention this limitation if asked during review.

## Cloud Desktop Progress

Date updated: 2026-06-27

- The Week 3 folder has been transferred and extracted on the Windows cloud desktop.
- Power BI Desktop is available and has been opened.
- The three prepared CSV files have been imported:
  - `netflix_main_clean.csv`
  - `netflix_type.csv`
  - `netflix_date.csv`
- The report has been saved in the Windows cloud desktop lab folder as `20260627.pbix`.
- The numeric filename was used because the remote Windows input method interfered with English filename/path entry.
- Model view confirmed two active one-to-one relationships on `show_id`.
- A temporary visual was attempted but not saved as final evidence because Power BI defaulted to an unsuitable aggregation. Final visual evidence is currently provided through the generated local charts and `week3_evidence_log.docx`.

Recommended manual continuation:

1. Open Model view.
2. Confirm the existing relationships on `show_id`:
   - `netflix_main_clean[show_id]` to `netflix_type[show_id]`
   - `netflix_main_clean[show_id]` to `netflix_date[show_id]`
3. Save screenshots of the model view and data pane if needed.
4. Keep the current saved PBIX file as `C:\Users\admin\Desktop\AI\BDBI\week3\lab\20260627.pbix`, or rename it manually to `BDBI_week3_netflix_lab.pbix` if convenient.
5. Use `week3_evidence_log.docx` for the current evidence package.
