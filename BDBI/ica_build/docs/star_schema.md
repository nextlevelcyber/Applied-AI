# Star Schema Design — Global Superstore

## Grain
`Fact_Sales` = **one row per order line** (a single product on a single order). 13,297 rows.

## Tables (1 fact + 5 dimensions = 6 tables → clears the rubric's "4+ tables" top band)

| Table | Type | Key | Key attributes |
| --- | --- | --- | --- |
| `Fact_Sales` | Fact | Row ID (degenerate) | OrderDateKey, ShipDateKey, CustomerID, ProductID, GeoKey, ShipModeKey (all FKs) + Sales, Quantity, Discount, Profit, Shipping Cost, Ship Days, Order Priority |
| `Dim_Date` | Dimension | DateKey (yyyymmdd) | Date, Year, Quarter, MonthNo, Month, MonthYear, DayName, IsWeekend |
| `Dim_Customer` | Dimension | CustomerID | Customer Name, Segment |
| `Dim_Product` | Dimension | ProductID | Product Name, Category, Sub-Category |
| `Dim_Geography` | Dimension | GeoKey (surrogate) | City, State, Country, Market, Region |
| `Dim_ShipMode` | Dimension | ShipModeKey (surrogate) | Ship Mode |

## Relationships (all Many-to-One, single-direction cross filter → NO many-to-many)

| From (many) | To (one) | Cardinality | Cross-filter |
| --- | --- | --- | --- |
| Fact_Sales[OrderDateKey] | Dim_Date[DateKey] | * → 1 | Single (active) |
| Fact_Sales[ShipDateKey] | Dim_Date[DateKey] | * → 1 | Single (inactive — role-playing; activated via USERELATIONSHIP when needed) |
| Fact_Sales[CustomerID] | Dim_Customer[CustomerID] | * → 1 | Single |
| Fact_Sales[ProductID] | Dim_Product[ProductID] | * → 1 | Single |
| Fact_Sales[GeoKey] | Dim_Geography[GeoKey] | * → 1 | Single |
| Fact_Sales[ShipModeKey] | Dim_ShipMode[ShipModeKey] | * → 1 | Single |

Notes for the appendix write-up:
- `Dim_Date` is a **role-playing dimension** (Order Date + Ship Date). Only one relationship can be active at a time; the Ship Date relationship is kept inactive and activated inside a measure with `USERELATIONSHIP`.
- Each dimension key is **unique** (verified: Dim_Customer 1,434 distinct IDs, Dim_Product 6,984, Dim_Geography 2,261 surrogate keys) so every relationship resolves to Many-to-One — there are no many-to-many relationships anywhere in the model.
- To satisfy the appendix requirement to *demonstrate* relationship-building, delete the Fact→Dim_Geography relationship, show the model with the broken link, then re-create it (Model view → drag GeoKey onto GeoKey) — screenshot before and after.
