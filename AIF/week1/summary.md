# Week 1 - What's AI

## Learning Focus

Week 1 introduces the AIF module, the meaning and scope of Artificial Intelligence, the history of AI, major application areas, and the difference between broad views of AI. The lab introduces R/RStudio and compares R with Python for data science and AI work.

## Key Concepts

- AI can be viewed as building systems that act rationally, think rationally, act like humans, or think like humans.
- AI applications include game agents, simulated agents, machine translation, expert systems, neural networks, and reinforcement learning.
- The module expects weekly lecture/lab participation and continued independent practice.
- R is strong for statistics and data analysis; Python is broader for general programming, AI engineering, deployment, and machine learning libraries.

## Official Materials

Lecture files are in `lecture/`:

- `AI Foundations 2025 2026 - Module Introduction.pdf`
- `CIS4049-N - Week 1 - Artificial Intelligence - An Introductory lecture - Part 1.pdf`
- `CIS4049-N - Week 1 - Artificial Intelligence - An Introductory lecture - Part 2.pdf`
- `CIS4049-N - Week 1 - Artificial Intelligence - An Introductory lecture - Part 3.pdf`
- `CIS4049-N - Week 1 - Artificial Intelligence - An Introductory lecture - Part 4.pdf`
- `CIS4049-N - Week 1 - Artificial Intelligence - An Introductory lecture - Part 5.pdf`

Lab files are in `lab/` and include R/RStudio introductions, R tutorial workbooks, extra R material, and datasets.

## Lab Completed

Completed practical work:

- Loaded and inspected `OrderData.csv`, `forecast_data.csv`, `Iris.csv`, and `Housing.csv`.
- Recomputed missing `Total` values in `OrderData.csv` as `Units * Unit Cost`.
- Produced regional order summaries.
- Produced Iris species-level mean measurements.
- Produced housing and weather dataset summaries.
- Ran both Python and R versions of the basic data analysis practice.

## Results

Results are saved in `results/`:

- `week1_data_analysis_results.json`
- `week1_order_region_summary.csv`
- `week1_iris_species_means.csv`
- `week1_r_console_output.txt`
- `week1_r_order_region_summary.csv`
- `week1_r_iris_species_means.csv`

Key outputs:

- Order dataset contains 43 rows. All original `Total` values were missing and were recomputed.
- Regional order revenue summary was produced for Central, East, and West.
- Iris species means were calculated for sepal and petal measurements.
- Housing dataset summary includes average price, median price, average area, and price-area correlation.

## ICA Connection

This week supports the ICA by introducing AI as a broad applied discipline and by starting the data handling skills needed for any AI case study. The R/Python comparison is useful when deciding whether the ICA implementation should focus on Python, R, or both.
