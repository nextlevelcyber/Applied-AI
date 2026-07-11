# Dashboard Specification — Appendix 3 (35%)

Consistent theme across all pages; slicers for Year, Market, Category on each page. Four pages.

## Page 1 — Executive Overview
- **6 KPI cards**: Total Sales, Total Profit, Profit Margin %, Total Orders, Customers, Avg Order Value. *(chart 01)*
- **Sales & Profit by Market** — clustered bar. *(chart 02)*
- **Sales share by Segment** — donut. *(chart 06)*
- **Annual sales growth** — column with Sales YoY %. *(chart 08)*
- Slicers: Year, Market.

## Page 2 — Product Performance
- **Sales vs Profit Margin by Category** — combo (column + line). *(chart 03)*
- **Profit by Sub-Category** — diverging bar, conditional colour (loss = red). Surfaces **Tables lose money**. *(chart 07)*
- **Decomposition Tree** — *AI/ML visual + new chart type*: Total Profit broken down by Market → Category → Sub-Category, using Power BI's "High/Low value" AI split. (Satisfies both the "new chart not covered in lessons" 5-mark item AND the "AI and ML tools" top-band requirement.)
- Slicer: Category.

## Page 3 — Trend & Forecast (Data Analytics — 10 marks)
- **Monthly Sales line chart** with the built-in **Analytics pane → Forecast** (6-month, 95% CI). *(chart 04)*
- **Sales by Year/Quarter** matrix with the Sales YoY % measure.
- **Key Influencers** visual — *second AI/ML visual*: "What influences Profit to be Loss?" → shows Discount > 20%, Sub-Category = Tables as top drivers.
- Slicer: Market.

## Page 4 — Customer & Discount Insight
- **Profit by Discount Band** — the headline insight chart; profit turns negative above 20%. *(chart 05)*
- **Map** (filled map): Sales by Country — a visual type beyond the basic labs.
- **Q&A / "Ask a question" visual** — natural-language query box (named explicitly in the rubric top band), e.g. "top 5 sub-categories by profit".
- **Top Customers table** with data bars.

## Required interactive/advanced elements (rubric top band checklist)
- ✅ New chart type not in lessons: **Decomposition Tree** (also map, Q&A).
- ✅ AI/ML visuals: **Decomposition Tree**, **Key Influencers**, **Q&A**.
- ✅ Trend + **Forecast** (Analytics pane).
- ✅ **KPI cards** clearly visualised.
- ✅ **Buttons + Bookmarks**: nav buttons across the 4 pages; a "Reset filters" bookmark button.
- ✅ Consistent **theme**, slicers, cross-filtering between visuals.
