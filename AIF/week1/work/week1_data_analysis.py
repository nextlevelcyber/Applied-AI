from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
LAB = BASE / "lab"
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)


def dataset_profile(path: Path) -> dict:
    df = pd.read_csv(path, encoding="utf-8-sig")
    profile = {
        "file": path.name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "missing_values": {col: int(df[col].isna().sum()) for col in df.columns},
    }

    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        profile["numeric_summary"] = (
            numeric.describe().round(3).to_dict()
        )
    return profile


def clean_order_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["Units"] = pd.to_numeric(df["Units"], errors="coerce")
    df["Unit Cost"] = pd.to_numeric(df["Unit Cost"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    df["Computed Total"] = df["Units"] * df["Unit Cost"]
    df["Total"] = df["Total"].fillna(df["Computed Total"])
    return df


def main() -> None:
    csv_files = [
        LAB / "OrderData.csv",
        LAB / "forecast_data.csv",
        LAB / "Iris.csv",
        LAB / "Housing.csv",
    ]
    profiles = [dataset_profile(path) for path in csv_files]

    order = clean_order_data(LAB / "OrderData.csv")
    order_region = (
        order.groupby("Region", dropna=False)
        .agg(orders=("Item", "count"), units=("Units", "sum"), revenue=("Total", "sum"))
        .round(2)
        .reset_index()
    )
    order_region.to_csv(RESULTS / "week1_order_region_summary.csv", index=False)

    iris = pd.read_csv(LAB / "Iris.csv")
    iris_species = (
        iris.groupby("Species")
        [["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]
        .mean()
        .round(3)
        .reset_index()
    )
    iris_species.to_csv(RESULTS / "week1_iris_species_means.csv", index=False)

    housing = pd.read_csv(LAB / "Housing.csv")
    housing_summary = {
        "average_price": round(float(housing["price"].mean()), 2),
        "median_price": round(float(housing["price"].median()), 2),
        "average_area": round(float(housing["area"].mean()), 2),
        "price_area_correlation": round(float(housing["price"].corr(housing["area"])), 4),
    }

    forecast = pd.read_csv(LAB / "forecast_data.csv")
    forecast_summary = {
        "location": str(forecast["Name"].iloc[0]),
        "rows": int(len(forecast)),
        "mean_temperature": round(float(forecast["Temperature"].mean()), 2),
        "max_wind_speed": round(float(forecast["Wind Speed"].max()), 2),
        "rainy_days": int(forecast["Conditions"].str.contains("Rain", na=False).sum()),
    }

    report = {
        "profiles": profiles,
        "order_region_summary_file": "week1_order_region_summary.csv",
        "iris_species_means_file": "week1_iris_species_means.csv",
        "housing_summary": housing_summary,
        "forecast_summary": forecast_summary,
    }
    (RESULTS / "week1_data_analysis_results.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
