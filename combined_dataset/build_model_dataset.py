# build_model_dataset.py
# Combine exposure, sea-level, and meteorological features into one modeling dataset.

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

# ---- 1. Read the three feature tables ----
exp_path = BASE_DIR / "exposure_dataset.csv"
sea_path = BASE_DIR.parent / "sea_level" / "sea_level_features.csv"
met_path = BASE_DIR.parent / "Meteorological" / "meteorological_features.csv"

df_exp = pd.read_csv(exp_path)
df_sea = pd.read_csv(sea_path)
df_met = pd.read_csv(met_path)

# Make city names consistent (lowercase)
for df in (df_exp, df_sea, df_met):
    df["city_key"] = df["city"].str.strip().str.lower()

# ---- 2. Merge ----
df = df_exp.merge(df_sea, on="city_key", how="left", suffixes=("", "_sea"))
df = df.merge(df_met, on="city_key", how="left", suffixes=("", "_met"))

# ---- 3. Select columns to keep ----
df = df[
    [
        "city",
        "state",

        # Target
        "exposure_index",
        "exposure_raw",

        # Exposure components
        "urban_ratio",
        "densityMi",

        # Sea level
        "sea_level_trend",
        "sea_level_recent_mean",
        "sea_level_max_anomaly",
        "years_covered",          # from sea_level table

        # Meteorology
        "rain_daily_mean",
        "rain_daily_max",
        "heavy_rain_threshold",
        "heavy_rain_days_per_year",
        "years_covered_met",      # rename below
    ]
]

# Rename meteorology years field
df = df.rename(columns={"years_covered_met": "met_years"})

# Output
out_path = BASE_DIR / "modeling_dataset.csv"
df.to_csv(out_path, index=False)

print(" Saved combined modeling dataset to:", out_path)
print(df)


