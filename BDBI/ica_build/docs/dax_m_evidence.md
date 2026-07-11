# DAX & M Language Evidence — Appendix 2

## Part A — M Language (Power Query) transformations

Every step below is auto-recorded in the **Applied Steps** panel — that panel is the M evidence to screenshot. The equivalent M code is shown for the write-up.

1. **Source / Promote headers** — `Source = Csv.Document(...)`, `Table.PromoteHeaders`.
2. **Change types** — cast Order Date / Ship Date to `date`, Sales/Profit/Shipping Cost to `Currency.Type`, Quantity to `Int64.Type`, Discount to `Percentage.Type`:
   `= Table.TransformColumnTypes(Source,{{"Order Date", type date},{"Sales", Currency.Type},{"Discount", Percentage.Type}, ...})`
3. **Trim & Clean text columns** — remove stray whitespace:
   `= Table.TransformColumns(#"Changed Type",{{"City", Text.Trim},{"Country", Text.Trim}})`
4. **Remove duplicates** on Row ID (guarantee unique fact grain):
   `= Table.Distinct(#"Trimmed Text", {"Row ID"})`
5. **Add custom column "Ship Days"** (M arithmetic on dates):
   `= Table.AddColumn(#"Removed Dup", "Ship Days", each Duration.Days([Ship Date]-[Order Date]), Int64.Type)`
6. **Add "OrderDateKey"** integer surrogate for the date relationship:
   `= Table.AddColumn(prev, "OrderDateKey", each Date.Year([Order Date])*10000 + Date.Month([Order Date])*100 + Date.Day([Order Date]), Int64.Type)`
7. **Reference queries to build dimensions** — right-click the cleaned query → **Reference**, then **Choose Columns** down to the dimension attributes and **Remove Duplicates** on the key. One reference per dimension (Dim_Customer, Dim_Product, Dim_Geography, Dim_ShipMode).
8. **Dim_Date built with M** — `List.Dates` generated calendar then column adds:
   `= List.Dates(#date(2011,1,1), Duration.Days(#date(2014,12,12)-#date(2011,1,1))+1, #duration(1,0,0,0))`
9. **Merge** the Geo surrogate key back into the fact table (`Table.NestedJoin` / Merge Queries on the 5 geo columns) then expand only `GeoKey`.

## Part B — DAX measures (create in a dedicated `_Measures` table)

| # | Measure | DAX | What it does / why |
| --- | --- | --- | --- |
| 1 | Total Sales | `Total Sales = SUM(Fact_Sales[Sales])` | Core revenue KPI. |
| 2 | Total Profit | `Total Profit = SUM(Fact_Sales[Profit])` | Core profitability KPI. |
| 3 | Profit Margin % | `Profit Margin % = DIVIDE([Total Profit],[Total Sales])` | Ratio KPI; `DIVIDE` avoids divide-by-zero. Formatted as %. |
| 4 | Total Orders | `Total Orders = DISTINCTCOUNT(Fact_Sales[Order ID])` | Counts unique orders (a line-level table would otherwise overcount). |
| 5 | Total Quantity | `Total Quantity = SUM(Fact_Sales[Quantity])` | Units sold. |
| 6 | Avg Order Value | `Avg Order Value = DIVIDE([Total Sales],[Total Orders])` | Revenue per order. |
| 7 | Avg Discount | `Avg Discount = AVERAGE(Fact_Sales[Discount])` | Mean discount, % format. |
| 8 | Sales YoY % | `Sales YoY % = VAR py = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Dim_Date[Date])) RETURN DIVIDE([Total Sales]-py, py)` | Time-intelligence growth vs previous year. |
| 9 | Sales Rank by Sub-Cat | `Sales Rank = RANKX(ALL(Dim_Product[Sub-Category]), [Total Sales],, DESC)` | Ranks sub-categories; `ALL` removes the visual filter so the rank is stable. |
| 10 | Sales (by Ship Date) | `Sales by Ship Date = CALCULATE([Total Sales], USERELATIONSHIP(Fact_Sales[ShipDateKey], Dim_Date[DateKey]))` | Activates the inactive role-playing relationship — demonstrates advanced modelling. |

## Part C — Calculated columns (DAX, in the model)

| # | Column | DAX | Why |
| --- | --- | --- | --- |
| 1 | Discount Band | `Discount Band = SWITCH(TRUE(), Fact_Sales[Discount]=0,"0%", Fact_Sales[Discount]<=0.2,"1-20%", Fact_Sales[Discount]<=0.4,"21-40%", Fact_Sales[Discount]<=0.6,"41-60%","61-100%")` | Buckets discounts to expose the profit cliff (used in the headline chart). |
| 2 | Profit Flag | `Profit Flag = IF(Fact_Sales[Profit]<0,"Loss","Profit")` | Splits loss-making vs profitable lines for conditional formatting. |

All formulae are **explained in prose in the report** (not left as bare screenshots) — this is what Appendix 2's top band rewards.
