# Power BI Build Guide — Global Superstore ICA

This guide reproduces the `.pbix` that the report describes. Do this on the Cloud Computer where Power BI Desktop runs. It takes ~2–3 hours. Capture the screenshots noted with 📸 as you go — they slot straight into the report appendix (replace my chart images with your real Power BI screenshots before submitting).

**Source files (in `ica_build/data/`):**
- `Global_Superstore_clean.csv` — cleaned flat table (import this and build the star schema in Power Query, as below). *Recommended path — gives authentic M evidence.*
- `Global_Superstore_StarSchema.xlsx` — the same tables already split (Fact_Sales + 5 dims), if you prefer to import the model ready-made.
- Individual `Fact_Sales.csv`, `Dim_*.csv` — same tables as CSVs.

Submit `Global_Superstore_clean.csv` as your "source Excel/CSV" file alongside the PDF and `.pbix`.

---

## 1. Import
Home → Get Data → Text/CSV → `Global_Superstore_clean.csv` → **Transform Data** (not Load).

## 2. Power Query — cleansing (M) 📸 *Applied Steps panel per query*
On the main query:
1. Set data types: Order Date / Ship Date → **Date**; Sales, Profit, Shipping Cost → **Fixed decimal number**; Quantity → **Whole number**; Discount → **Percentage**.
2. Home → Reduce Rows → **Remove Duplicates** (select Row ID first).
3. Add Column → Custom Column: `Ship Days = Duration.Days([Ship Date]-[Order Date])`.
4. Add Column → Custom Column: `OrderDateKey = Date.Year([Order Date])*10000 + Date.Month([Order Date])*100 + Date.Day([Order Date])` (type Whole Number). Repeat for `ShipDateKey` using Ship Date.
5. Rename this query **Fact_Sales**.

## 3. Power Query — build the dimensions (M References)
For each dimension, right-click Fact_Sales → **Reference**, then Choose Columns + Remove Duplicates on the key:
- **Dim_Customer**: Customer ID, Customer Name, Segment → Remove Duplicates on Customer ID.
- **Dim_Product**: Product ID, Product Name, Category, Sub-Category → Remove Duplicates on Product ID.
- **Dim_Geography**: City, State, Country, Market, Region → Remove Duplicates → Add Index Column (from 1) named **GeoKey**. Merge GeoKey back into Fact_Sales (Merge Queries on the 5 geo columns) and expand only GeoKey; then remove the 5 text geo columns from the fact.
- **Dim_ShipMode**: Ship Mode → Remove Duplicates → Add Index Column named **ShipModeKey**. Merge back into Fact_Sales, expand ShipModeKey, remove Ship Mode text column.
- **Dim_Date**: New Source → Blank Query → paste:
  ```
  = List.Dates(#date(2011,1,1), Duration.Days(#date(2014,12,12)-#date(2011,1,1))+1, #duration(1,0,0,0))
  ```
  Convert to Table, rename column **Date**, then Add Column for DateKey (`Date.Year([Date])*10000+Date.Month([Date])*100+Date.Day([Date])`), Year, Quarter (`"Q"&Text.From(Date.QuarterOfYear([Date]))`), Month name, MonthNo, MonthYear.

Home → **Close & Apply**.

## 4. Model view — star schema 📸 *before/after of the model diagram*
Verify/create these relationships (all should be **Many-to-One, single** cross-filter):
- Fact_Sales[OrderDateKey] → Dim_Date[DateKey] *(active)*
- Fact_Sales[ShipDateKey] → Dim_Date[DateKey] *(make **inactive** — dotted line)*
- Fact_Sales[CustomerID] → Dim_Customer[CustomerID]
- Fact_Sales[ProductID] → Dim_Product[ProductID]
- Fact_Sales[GeoKey] → Dim_Geography[GeoKey]
- Fact_Sales[ShipModeKey] → Dim_ShipMode[ShipModeKey]

To evidence the skill: delete the Fact_Sales → Dim_Geography relationship, screenshot the broken model, drag GeoKey → GeoKey to re-create it, screenshot again.

## 5. DAX 📸 *each measure in the formula bar*
Right-click in Data pane → New table → `_Measures = {BLANK()}` (holder). Add measures (Modeling → New measure):
```
Total Sales     = SUM(Fact_Sales[Sales])
Total Profit    = SUM(Fact_Sales[Profit])
Profit Margin % = DIVIDE([Total Profit],[Total Sales])
Total Orders    = DISTINCTCOUNT(Fact_Sales[Order ID])
Avg Order Value = DIVIDE([Total Sales],[Total Orders])
Sales YoY %     = DIVIDE([Total Sales]-CALCULATE([Total Sales],SAMEPERIODLASTYEAR(Dim_Date[Date])),
                        CALCULATE([Total Sales],SAMEPERIODLASTYEAR(Dim_Date[Date])))
Sales Rank      = RANKX(ALL(Dim_Product[Sub-Category]),[Total Sales],,DESC)
Sales by Ship Date = CALCULATE([Total Sales],USERELATIONSHIP(Fact_Sales[ShipDateKey],Dim_Date[DateKey]))
```
Calculated columns (Modeling → New column, on Fact_Sales):
```
Discount Band = SWITCH(TRUE(), Fact_Sales[Discount]=0,"0%", Fact_Sales[Discount]<=0.2,"1-20%",
                Fact_Sales[Discount]<=0.4,"21-40%", Fact_Sales[Discount]<=0.6,"41-60%","61-100%")
Profit Flag   = IF(Fact_Sales[Profit]<0,"Loss","Profit")
```

## 6. Build the 4 dashboard pages 📸 *one screenshot per page*
Apply a Theme (View → Themes). Add Year / Market / Category slicers to each page.

**Page 1 – Executive Overview**: 6 Card visuals (the measures above); Clustered bar Sales & Profit by Market; Donut Sales by Segment; Column Sales by Year.

**Page 2 – Product Performance**: Line-and-clustered-column (Category: Sales bars + Profit Margin % line); Bar Profit by Sub-Category with conditional colour (Format → Data colors → fx → based on Profit Flag / diverging); **Decomposition Tree** (Build → Decomposition tree; Analyze = Total Profit; Explain by = Market, Category, Sub-Category → use the AI "High/Low value" splits). *(new chart type + AI)*

**Page 3 – Trend & Forecast**: Line chart Total Sales by Date → select it → **Analytics pane** → **Forecast** → Add (Forecast length 6 months, confidence 95%); Matrix Year/Quarter with Sales YoY %; **Key Influencers** visual (Analyze = Profit Flag, Explain by = Discount, Sub-Category, Market). *(forecast + AI)*

**Page 4 – Customer & Discount**: Column Total Profit by Discount Band; **Filled Map** Sales by Country; **Q&A** visual (Insert → Q&A); Table of top customers with data bars. *(new chart types + AI)*

**Buttons/bookmarks**: Insert → Buttons for page navigation; View → Bookmarks for a "Reset filters" button.

## 7. Save & export
- Save as **`Global_Superstore_ICA.pbix`**.
- Paste your real screenshots into the report, replacing the placeholder chart images, then export the Word file to PDF.
- Rename the PDF to **`<studentnumber>_<lastname>.<firstname>.pdf`**.
- Submit the PDF + `.pbix` + `Global_Superstore_clean.csv` via the Blackboard ICA Submission Link before **2026-07-29 23:59 (UTC+8)**.
