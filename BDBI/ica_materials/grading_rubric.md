# BDBI ICA — Official Grading Rubric

Captured directly from Blackboard: **Assessments → ICA Submission Link → "This item is marked with a rubric"**.
Verified live on 2026-07-04 (module: *Big Data and Business Intelligence CIS4008-N, Amity - May 26*, course id `_29627_1`).

Maximum points: **100**. Attempts: **unlimited** (last marked attempt is used). Feedback within 20 working days of the deadline.

Note: the criterion titles show one weighting in brackets, but the percentage actually applied to the total mark is different. Always trust the **"% of total mark"** line, not the bracketed number in the title.

---

## 1) BI Report Structure — title says (20%), actually **25% of total mark**

a) Structure of the Business Intelligence Report.
b) Dataset is described and BI questions/KPIs addressed in the report, including Final Recommendations.
c) Visuals/Charts are appropriately used and explained in the Report.

**Excellent/Outstanding (70–100%):** The report is well written and contains the required sections, following the recommended format from the ICA — it must begin with its own Title page, the Executive Summary and Introduction. The dataset has been fully described, a link has been provided, and the questions addressed in the report are clearly stated. The Business Questions have been clearly addressed as shown by the Final Recommendations. The charts added in the report have been fully explained.

**Exemplary (60–69%):** Well written but doesn't fully follow the recommended format. Dataset fully described with a link, but BI question quality could improve. Business Questions addressed, but recommendations could be based on a wider set of charts/analysis. Some charts are missing an explanation/description.

**Satisfactory (50–59%):** Report is basic and needs more evidence, depth and content, though a clear audit of BI analytic/visual core skills is evident. Recommendation: review the library resources on report writing. Final recommendations are not clearly tied to the Power BI analysis. Most charts lack explanation.

---

## 2) Appendix 1 — Business Intelligence Design — title says (30%), **30% of total mark** (consistent)

b) Data pre-processing. c) Data modelling and relationships.

**Excellent/Outstanding (70–100%):** Clear and succinct set of design steps covering BI questions, pre-processing and star schema, at an industry level. Required pre-processing steps are shown and clearly explained. **The Star Schema model includes 4 or more tables (fact and dimension tables). Many-to-many relationships have been avoided.**

**Exemplary (60–69%):** Basic set of design steps; needs to be more succinct/industry-level. Pre-processing sometimes limited in disclosure. Star Schema includes 3 or more tables. Recommendation: develop star schemas — fact and dimensions — from several related datasets.

**Satisfactory (50–59%):** Limited set of design steps.

---

## 3) Appendix 2 — BI Data Manipulation via M and/or DAX — title says (15%), actually **10% of total mark**

**Excellent/Outstanding (70–100%):** M and DAX skills clearly provided in the report. M and DAX applied to perform several steps/calculations. Formulae correctly used **and clearly explained**, showing the student knows how to manipulate data into desired formats.

**Exemplary (60–69%):** M and DAX skills need to be more clearly identified/covered; there's an assumption some data-manipulation activity happened based on the analytics shown. Recommendation: document your M and DAX features; simulate the activity if your dataset is already cleansed (e.g. separate day-of-week from a date, then build analytics/visuals on it).

---

## 4) Appendix 3 — Dashboard Visuals — title says (35%), **35% of total mark** (consistent)

c) Data Analytics (analysing trends and forecast) — 10 of the 35. d) A new type of chart, not covered in the lessons — 5 of the 35.

**Excellent/Outstanding (70–100%):** Great variety of charts, correctly formatted to highlight the information conveyed; chart selection appropriate to the data displayed. KPIs clearly used and visualised, and used to analyse the data per the BI questions. Infographics, animated charts, buttons and an "ask-a-question" visual have been included. Data Analytics is used to further describe/analyse the data and show meaningful insights. **AI and Machine Learning tools have been included in the final dashboard/report** to further investigate the data, with a clear explanation of findings. A wide selection of new chart types has been included.

**Exemplary (60–69%):** Great variety of charts, correctly formatted and appropriate; some new chart types included; KPIs clear. Recommendation: practice predictive modelling, trending and/or forecasting functions/features; review analytics that support AI and ML.

**Satisfactory (50–59%):** A set of charts exists but needs more to form a viable full dashboard collection; charts are basic but appropriate. More thought needed on KPIs / Star Schema (facts and dimensions). Recommendation: practice developing multi-dimensional star schemas for each fact, with many dimensions of analytics.

---

## What this means in practice (read together with the self-assessment table in `ica_documents/Big Data and BI - ICA.docx`)

- Chase the **Appendix 3 (35%)** and **Appendix 1 (30%)** bands hardest — together they are 65% of the mark.
- Star schema needs **4+ tables** (fact + dimension) with **no many-to-many relationships** to hit the top band of Appendix 1.
- Appendix 3's top band explicitly calls for: a new/uncommon chart type, KPI visuals, an "ask-a-question" visual, infographics/animated charts/buttons, a trend/forecast analysis, and some visible use of an AI/ML feature (e.g. Key Influencers visual, Decomposition Tree, Q&A visual, or the built-in Forecasting on a line chart) — all of these are native Power BI features, no external AI tool required.
- Appendix 2 rewards M/DAX steps that are not just used but **explained** in the report text, not left as unexplained screenshots.
- Section 1 rewards a report that literally follows the template's section order (Title page → Executive Summary → Introduction → Findings → Conclusions/Recommendations → Appendices → self-assessment table).
