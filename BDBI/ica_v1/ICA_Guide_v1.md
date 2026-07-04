# BDBI ICA — Guide v1 (Kaymen's working plan)

official Blackboard materials in `../ica_materials/` (verified live on
2026-07-04). This is v1: a complete plan to work from. Once a dataset is chosen and work starts,
produce `ica_v2/`, `ica_v3/`, etc. for later drafts rather than editing this file in place.

---

## Part 1 — What the ICA actually requires (short version)

- **Module:** Big Data and Business Intelligence CIS4008-N (Amity – May 26). **Deadline: 2026-07-29, 23:59 (UTC+8)** — 25 days from today (2026-07-04). Unlimited attempts, last marked attempt counts, feedback in 20 working days.
- **Task:** design and build a Business Intelligence solution in Power BI Desktop from an industry-style dataset, then write it up as a report.
- **Submit 3 things** through the Blackboard "ICA Submission Link":
  1. One PDF containing the whole written report (Section 1 + Section 2 + appendix + self-assessment table).
  2. The Power BI project file (`.pbix`).
  3. Any Excel/CSV file(s) you used to import the data.
- **Report length:** at least **1200 words**, but "mostly screenshots with wording in bullet points" — this is not meant to be a prose-heavy essay.
- **File naming for the PDF:** `studentnumber_lastname.firstname.pdf` (e.g. `x1234567_smith.pdf`) — confirm your Teesside student number before the final export, the placeholder in this guide is `<studentnumber>_cui.kaymen.pdf`.
- **AI permission: Amber.** You may use AI (including this session) as a companion for permitted tasks, but you must not submit unacknowledged AI-generated work as your own — say in the report where/how AI assisted.
- **Do not reuse content from the ICA Samples or the tutor's dashboard examples** — Blackboard explicitly warns this risks a plagiarism accusation. Use them only to see how sections are formatted.

### How the 100 marks break down (see `../ica_materials/grading_rubric.md` for full band text)

| Section | Weight | What it rewards at the top band |
| --- | --- | --- |
| 1. BI Report Structure | 25% | Full template followed; dataset + BI questions/KPIs clearly stated; every chart explained; recommendations tied to the analysis |
| Appendix 1 — BI Design | 30% | Clear pre-processing steps; **star schema with 4+ tables (fact + dimensions)**; no many-to-many relationships |
| Appendix 2 — M/DAX | 10% | DAX and M both used for real calculations/transformations, and both **explained**, not just shown |
| Appendix 3 — Dashboard Visuals | 35% | Wide variety of well-chosen charts; clear KPIs; trend/forecast analytics; **one chart type not covered in lessons**; some AI/ML-powered visual (Key Influencers, Decomposition Tree, Q&A, or Forecasting) |

Appendix 3 + Appendix 1 are 65% of the mark between them — the dashboard and the data model matter more than the prose.

### Required report structure (from `ICA - Template - Big Data and BI.docx` — follow this exactly)

1. **Title page** — report title, module, your name/student number.
2. **Executive Summary** — write this *last*; condensed findings + recommendations + 1-2 charts.
3. **Body**
   - **Introduction**, with two named sub-sections:
     - *Data Source* — link/database/table/column description.
     - *BI Requirements/Questions* — the KPI(s), the business questions, the audience, why it matters.
   - **Finding based on analysis and evaluation** — the main section. Every Power BI visual gets a screenshot + description of what it shows and why that chart type was chosen, plus the key finding it reveals.
   - **Conclusions and Recommendations** — tie explicitly back to the findings above.
4. **ICA – Appendix: BI Design**
   - **Data Pre-Processing or Data Cleansing** — bullet list of steps taken (remove NAs, rename columns, change types, merge tables, etc.) with a "before/after" screenshot, not a step-by-step click log.
   - **BI Data Modelling via Star Schema – Facts and Dimensions** — the model diagram (Model view), with keys explained. 4+ tables, no many-to-many.
   - **DAX and M Language** — every measure/calculated column, and where/how M was used in Power Query.
   - **Dashboard** — describe how the pages are organised, with a screenshot of every dashboard page.
5. **Self-assessment table** (0-100 scale, keep it in the report) — 4 rows: Report Structure, Data Pre-processing and Data Modelling, DAX and M language, Dashboard Design.

---

## Part 2 — Step-by-step execution plan

### Step 0 — Choose the dataset (do this first, before anything else)

Options, in order of recommendation:

1. **Pick one of the 23 approved datasets** in `../ica_materials/datasets/dataset_links.md` (mostly Kaggle). Good defaults for a clean star schema + rich KPIs: **Global Superstore Dataset** (#7 — orders/customers/products, very common BI teaching dataset, easy fact/dimension split), **Employee Attrition** (#10), or **Bikes Sales in Europe** (#12).
2. **AdventureWorks database** (`week5/lab/AdventureWorks_Database.xlsx`, already downloaded) — already fairly close to a real star schema, less cleaning needed, good if you want to spend more time on DAX/dashboard than on data prep.
3. One of the two SharePoint folders (Footwear Retail, Weather Sensor Data) if you want something less commonly used by classmates.
4. Your own workplace dataset, if you are a Degree Apprenticeship student — see `Masters Degree Apprenticeship Knowledge, Skills, and Behaviour.docx`.

Do **not** reuse `shopping_trends_updated Dataset.xlsx` from the `S3196622_Sivadasan.Aathiragouri_BDBI_ICA` sample folder — that is a real classmate's already-submitted dataset/analysis, shown to you only as a worked example.

Once you've decided, fill in `dataset_selection_matrix.md` and `planning.md` in this folder (both already have templates from an earlier session) — that becomes the anchor for the rest of this plan.

**Software:** Power BI Desktop, running on the remote Windows desktop via the "Cloud Computer" app (same setup used for the weekly labs).

### Step 1 — Import the data

1. Copy your chosen source file (xlsx/csv) into a working folder on the remote desktop, e.g. `C:\Users\admin\Desktop\AI\BDBI\ICA\`.
2. Power BI Desktop → **Home** ribbon tab → **Get data** button → choose **Excel workbook** (or **Text/CSV**).
3. Select the file → in the **Navigator** dialog, tick the sheet(s) → click **Transform Data** (not Load) so you land in Power Query first.

### Step 2 — Data pre-processing / cleansing (Power Query, M language)

In the Power Query Editor, for the working query:

- **Home → Remove Rows / Remove Columns** to drop anything irrelevant.
- **Transform → Data Type** dropdown on each column header to fix types (Date, Whole Number, Decimal, Text).
- **Home → Remove Duplicates** (right-click a column header → Remove Duplicates) where needed.
- **Transform → Split Column** (by delimiter or by number of characters) if any column packs multiple fields together.
- Rename columns by double-clicking the header.
- Every one of the above actions is automatically recorded as an **M** step in the **Applied Steps** panel on the right — this list *is* your M Language evidence. Screenshot the final Applied Steps panel per query for the appendix (that's the "before/after" screenshot the template asks for, not a click-by-click log).
- **Home → Close & Apply** when done.

### Step 3 — Build the star schema (Model view)

The rubric's top band wants **4+ tables (fact + dimensions)** with **no many-to-many relationships**.

1. In Power Query, duplicate your cleaned query once per dimension you need (similar to the week4 lab pattern: right-click query → **Duplicate**, rename, then **Choose Columns** down to just the key + dimension attributes, then **Remove Duplicates** on the key column).
2. Keep one query as the **fact table** (the transaction-level rows: e.g. one row per order/ticket/reading) with foreign keys pointing at each dimension's key column.
3. Switch to **Model view** (left-hand vertical icon bar). Power BI auto-detects relationships from matching column names — verify each one:
   - Double-click each relationship line → **Edit relationship** → confirm **Cardinality** is **Many to one** (fact → dimension) or **One to one**, and **Cross filter direction** is set appropriately (usually **Single**; only switch to **Both** if a dimension-side slicer needs to filter through to another dimension via the fact table, as was needed in the week4 lab).
   - If Power BI shows a **many-to-many** relationship anywhere, that's a modelling problem — go back and make sure each dimension table has a unique key (one row per key value) before relating it to the fact table.
4. Screenshot the finished Model view diagram for the appendix, with a brief note on what each key column is.

### Step 4 — DAX measures and calculated columns

1. In **Report view**, right-click a table in the **Data** pane → **New measure** (or **Modelling** ribbon tab → **New Measure** button).
2. Write DAX in the formula bar, e.g.:
   - `Total Sales = SUM(Fact[Amount])`
   - `YoY Growth % = DIVIDE([Total Sales] - CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date])), CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date])))`
   - `Rank by Category = RANKX(ALL(Dimension[Category]), [Total Sales])`
3. Aim for at least 3-5 measures covering totals, a ratio/percentage, and a ranking or time-comparison — this maps directly onto Appendix 2's "several steps and calculations" requirement.
4. Add at least one **calculated column** too (Modelling → **New Column**), to show both DAX features are used, e.g. `Price Band = IF(Table[Price] > 100, "High", "Low")`.
5. Keep a running note of every measure/column and what it's for in `dax_m_evidence_log.md` in this folder — you'll turn this directly into the Appendix 2 write-up.

### Step 5 — Build the dashboard (multiple pages)

Recommended page plan (adapt table/field names to your dataset once chosen):

- **Page 1 — Overview:** 3-4 KPI cards (Card visual: right-click field → set aggregation via the field dropdown, e.g. Sum/Count/Count Distinct), a slicer, and one or two headline charts.
- **Page 2 — Category/Comparison analysis:** clustered bar/column charts, a treemap or donut for composition.
- **Page 3 — Trend/forecast:** a line chart of a measure over time, then **Analytics pane** (the icon that looks like a magnifying glass over a chart, in the Visualizations panel when a line chart is selected) → **Forecast** → **Add** → set forecast length — this satisfies the "Data Analytics (trends/forecast)" 10-mark sub-item directly, no extra tooling needed.
- **Page 4 — The "not covered in lessons" chart + AI/ML visual:** pick at least one of the following, since none of these were used in the weekly labs (which only used card, line, clustered column/bar, donut, treemap, table, slicer, text box):
  - **Decomposition Tree** (Build visual grid → search "Decomposition tree") — lets a user drill into what's driving a measure; counts as both the new-chart-type requirement *and* an AI-powered visual.
  - **Key Influencers** visual — Power BI's built-in AI feature that explains what drives a metric up or down.
  - **Q&A / "Ask a question"** visual — natural-language querying of your model, explicitly named in the rubric's top band.
  - Alternatively a **Ribbon chart**, **Funnel chart**, or **Gauge chart** if you'd rather avoid the AI visuals — any of these were not covered in the labs.
- Add at least one **button** (Insert ribbon → Buttons) wired to a **bookmark** (View ribbon → Bookmarks pane) for simple page navigation or a toggle — the rubric's top band explicitly mentions buttons.
- Apply a consistent **Theme** (View ribbon → Themes) across all pages, same as the week4 dashboard rebuild.

Screenshot **every page** of the finished dashboard for the Appendix "Dashboard" sub-section.

### Step 6 — Evidence capture (do this continuously, not at the end)

Keep a running folder of screenshots as you go (Power Query Applied Steps, Model view, each DAX formula, each dashboard page) — trying to reconstruct all of this from memory on the last day is the single biggest risk to the Appendix 1/2/3 marks (65% combined). Log what each screenshot proves in `dax_m_evidence_log.md` / `dashboard_design_checklist.md`.

### Step 7 — Write the report

1. Open `../ica_materials/ica_documents/ICA - Template - Big Data and BI.docx`, **Save As** into a new working copy (don't edit the original template).
2. Delete the blue instructional text and the first guidance page as instructed in the template.
3. Fill sections in this order (matches how the mark scheme reads, and is easier to write in than top-to-bottom):
   1. Introduction → Data Source + BI Requirements/Questions (write this once the dataset is picked, before touching Power BI, so your BI questions genuinely drive the model instead of being reverse-engineered afterwards).
   2. Appendix: BI Design (pre-processing, star schema, DAX/M, dashboard) — write this alongside Steps 2-5 above, while the screenshots are still fresh.
   3. Finding based on analysis and evaluation — walk through each dashboard page/chart and state the finding.
   4. Conclusions and Recommendations.
   5. Executive Summary — last, once you know what the headline findings actually are.
   6. Title page.
   7. Self-assessment table — score yourself honestly against the rubric bands in `grading_rubric.md`.
4. Word count check: template + screenshots will likely clear 1200 words on their own, but check before submitting.

### Step 8 — Export and submit

1. In Word: **File → Save As → PDF**. Confirm the file opens correctly and nothing is cut off/corrupted.
2. Rename to `<studentnumber>_cui.kaymen.pdf` (replace `<studentnumber>` with your actual Teesside student ID).
3. Save the final `.pbix` and the source Excel/CSV file(s) together in this project's `ica_v1` (or a later `ica_vN`) folder so everything for the last attempt is in one place.
4. Blackboard → Assessments → **ICA Submission Link** → upload all three files → confirm submission before **2026-07-29, 23:59 (UTC+8)**.

---

## Part 3 — Suggested timeline (25 days from 2026-07-04)

| Dates | Focus |
| --- | --- |
| Day 1-2 | Step 0: pick dataset, fill `dataset_selection_matrix.md` + `planning.md` |
| Day 3-5 | Steps 1-2: import + clean data in Power Query |
| Day 6-8 | Step 3: build star schema, verify relationships |
| Day 9-11 | Step 4: DAX measures/calculated columns |
| Day 12-16 | Step 5: build all dashboard pages, incl. forecast + new chart type + buttons |
| Day 17-18 | Step 6 catch-up: make sure every screenshot needed for the appendix has been captured |
| Day 19-22 | Step 7: write the full report from the template |
| Day 23-24 | Proofread, self-assess against `grading_rubric.md`, fix gaps |
| Day 25 (buffer, before 2026-07-29 23:59 UTC+8) | Step 8: export PDF, rename, final submission |

---

## Part 4 — Open items / things to confirm with Kaymen

- [ ] Which dataset to use (Step 0) — nothing else in this plan can get more specific until this is picked.
- [ ] Confirm exact Teesside student number for the PDF filename.
- [ ] Confirm whether Kaymen is a standard student or a Degree Apprenticeship student (changes whether `Masters Degree Apprenticeship Knowledge, Skills, and Behaviour.docx` criteria also apply).

## Supporting files in this folder

- `dataset_selection_matrix.md` — fill in once candidate datasets are shortlisted.
- `planning.md` — business context, BI questions/KPIs, model plan, dashboard plan.
- `dax_m_evidence_log.md` — running log of every DAX/M step for Appendix 2.
- `dashboard_design_checklist.md` — running log of dashboard pages/visuals for Appendix 3.
- `report_outline.md` — section-by-section drafting space for the Word report.
