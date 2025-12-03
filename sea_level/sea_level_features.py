# -*- coding: utf-8 -*-
"""
Extract sea-level trend features for Miami, New Orleans, Norfolk.
Creates: sea_level_features.csv
"""

# sea_level_features.py
# Extract simple sea-level features for Miami / New Orleans / Norfolk
# and save a small CSV for modeling.

import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

SEA_LEVEL_FILES = {
    "miami":       PROJECT_DIR / "sea_level_Florida.csv",
    "new_orleans": PROJECT_DIR / "sea_level_louisiana.csv",
    "norfolk":     PROJECT_DIR / "sea_level_virginia.csv",
}

def load_and_extract(city: str, csv_path: Path) -> dict:
    """Load a NOAA monthly sea-level CSV and compute a few features."""

    print(f"\nProcessing {city} from {csv_path.name} ...")

    df = pd.read_csv(csv_path, skiprows=5)
    df.columns = df.columns.str.strip()

    df = df[df["Year"].astype(str).str.isnumeric()]
    df["Year"] = df["Year"].astype(int)

    trend_cols = [c for c in df.columns if "Linear" in c]
    if not trend_cols:
        raise RuntimeError(
            f"Cannot find a 'Linear_*' column in {csv_path.name}. "
            f"Available columns: {list(df.columns)}"
        )
    trend_col = trend_cols[0]

    monthly_cols = [c for c in df.columns if "Monthly" in c]
    if not monthly_cols:
        raise RuntimeError(
            f"Cannot find a 'Monthly_*' column in {csv_path.name}. "
            f"Available columns: {list(df.columns)}"
        )
    monthly_col = monthly_cols[0]

    print(f"  Using trend column:   {trend_col}")
    print(f"  Using monthly column: {monthly_col}")

    slope = df[trend_col].mean()
    max_year = df["Year"].max()
    recent = df[df["Year"] >= max_year - 10]
    recent_mean = recent[monthly_col].mean()
    max_anom = df[monthly_col].max()

    return {
        "city": city,
        "sea_level_trend": slope,
        "sea_level_recent_mean": recent_mean,
        "sea_level_max_anomaly": max_anom,
        "years_covered": f"{df['Year'].min()}–{df['Year'].max()}",
    }


def main():
    rows = []
    for city, path in SEA_LEVEL_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing sea level CSV: {path}")
        rows.append(load_and_extract(city, path))

    out_csv = PROJECT_DIR / "sea_level_features.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print("\n Done! Saved:", out_csv)


if __name__ == "__main__":
    main()
