# meteorological_features.py
# Extract simple rainfall features for Miami, New Orleans, and Norfolk
#
# Input (in the same folder as this script):
#   - Miami.csv
#   - NewOrleans.csv
#   - Norfolk.csv
#
# Output:
#   - meteorological_features.csv
#       columns:
#         city,
#         rain_daily_mean,
#         rain_daily_max,
#         heavy_rain_threshold,
#         heavy_rain_days_per_year,
#         years_covered

import csv
from pathlib import Path

import numpy as np
import pandas as pd


# ---------- 1. Paths and city<->file mapping ----------

SCRIPT_DIR = Path(__file__).resolve().parent

CITY_FILES = {
    "miami": SCRIPT_DIR / "Miami.csv",
    "new_orleans": SCRIPT_DIR / "NewOrleans.csv",
    "norfolk": SCRIPT_DIR / "Norfolk.csv",
}


# ---------- 2. Helper: find the header row (DATE, PRCP) ----------

def find_header_row(csv_path: Path) -> int:
    """
    NOAA daily CSV files often start with several lines of text.
    This function scans until it finds the line that contains a DATE
    column and a precipitation column (PRCP).
    Returns the 0-based index of the header row.
    """
    with csv_path.open("r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            # Very forgiving check: look for DATE and PRCP in the header
            if "DATE" in line and "PRCP" in line:
                return i
    # Fallback: assume header is the first line
    return 0


# ---------- 3. Load & extract features for one city ----------

def load_and_extract(city: str, csv_path: Path) -> dict:
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing file for {city}: {csv_path}")

    print(f"\nProcessing {city} from {csv_path.name} ...")

    header_row = find_header_row(csv_path)

    df = pd.read_csv(
        csv_path,
        header=header_row,       
        encoding="utf-8",
        dtype=str,
        na_values=["", "NA", "NaN", "M", "m"],
    )

    df.columns = df.columns.str.strip()
    print("  Columns:", list(df.columns))

    date_candidates = [c for c in df.columns if c.upper().startswith("DATE")]
    if not date_candidates:
        raise KeyError(f"Could not find DATE column in {csv_path}")
    date_col = date_candidates[0]

    precip_candidates = []
    for c in df.columns:
        cu = c.upper()
        if any(key in cu for key in ["PRCP", "PRECIP", "RAIN"]):
            precip_candidates.append(c)

    if not precip_candidates:
        raise KeyError(
            f"Could not find precipitation column (PRCP / PRECIP* / *RAIN*) in {csv_path}.\n"
            f"Available columns: {list(df.columns)}"
        )

    precip_col = precip_candidates[0]
    print(f"  Using precipitation column: {precip_col}")

    df = df[[date_col, precip_col]].copy()
    df.rename(columns={date_col: "DATE", precip_col: "PRCP"}, inplace=True)

    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
    df["PRCP"] = df["PRCP"].str.replace("T", "0", regex=False)
    df["PRCP"] = pd.to_numeric(df["PRCP"], errors="coerce")

    df = df.dropna(subset=["DATE", "PRCP"])

    df.loc[df["PRCP"] < -1e-6, "PRCP"] = np.nan
    df = df.dropna(subset=["PRCP"])

    if df.empty:
        print("  ⚠ After cleaning, dataframe is empty. Here are first 10 raw rows:")
        raw_preview = pd.read_csv(
            csv_path, nrows=10, encoding="utf-8", dtype=str, errors="ignore"
        )
        print(raw_preview)
        raise RuntimeError(f"No valid precipitation data for {city}.")

    df["year"] = df["DATE"].dt.year

    rain_daily_mean = df["PRCP"].mean()
    rain_daily_max = df["PRCP"].max()
    heavy_thresh = df["PRCP"].quantile(0.9)

    heavy_flag = df["PRCP"] >= heavy_thresh
    heavy_per_year = heavy_flag.groupby(df["year"]).sum()
    heavy_days_per_year = heavy_per_year.mean()

    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    years_covered = f"{min_year}–{max_year}"

    return {
        "city": city,
        "rain_daily_mean": float(rain_daily_mean),
        "rain_daily_max": float(rain_daily_max),
        "heavy_rain_threshold": float(heavy_thresh),
        "heavy_rain_days_per_year": float(heavy_days_per_year),
        "years_covered": years_covered,
    }


# ---------- 4. Main ----------

def main():
    rows = []
    for city, path in CITY_FILES.items():
        rows.append(load_and_extract(city, path))

    out_df = pd.DataFrame(rows)[
        [
            "city",
            "rain_daily_mean",
            "rain_daily_max",
            "heavy_rain_threshold",
            "heavy_rain_days_per_year",
            "years_covered",
        ]
    ]

    out_path = SCRIPT_DIR / "meteorological_features.csv"
    out_df.to_csv(out_path, index=False)
    print("\n Saved meteorological features to:", out_path)


if __name__ == "__main__":
    main()
