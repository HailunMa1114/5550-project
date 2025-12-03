# -*- coding: utf-8 -*-
"""
Output:
  combined_dataset.csv  
"""

from pathlib import Path
import pandas as pd


HERE = Path(__file__).resolve().parent         
PROJECT_ROOT = HERE.parent                     

LAND_COVER_CSV = PROJECT_ROOT / "land_cover" / "land_cover_outputs" / "nlcd_exposure_summary.csv"
POP_CSV        = PROJECT_ROOT / "population" / "united-states-by-density-2025.csv"

OUT_CSV        = HERE / "combined_dataset.csv"


CITY_TO_STATE = {
    "miami":       "Florida",
    "new_orleans": "Louisiana",
    "norfolk":     "Virginia",
}


def main():
    print(f"Using land cover summary: {LAND_COVER_CSV}")
    print(f"Using population CSV:    {POP_CSV}\n")

    df_lc = pd.read_csv(LAND_COVER_CSV)
    print("[Land cover columns]")
    print(list(df_lc.columns), "\n")

    df_lc["city"] = df_lc["city"].str.lower().str.strip()
    df_lc["state"] = df_lc["city"].map(CITY_TO_STATE)

    df_pop = pd.read_csv(POP_CSV)
    print("[Population CSV columns]")
    print(list(df_pop.columns), "\n")

    needed_cols = ["state", "densityMi", "population", "TotalArea"]
    for col in needed_cols:
        if col not in df_pop.columns:
            raise RuntimeError(f" Missing column '{col}' in population CSV!")

    df_pop = df_pop[needed_cols].copy().set_index("state")

    df = df_lc.join(df_pop, on="state", how="left")

    missing = df[df["densityMi"].isna()]
    if not missing.empty:
        print(" WARNING: Some cities did not match population density:")
        print(missing[["city", "state"]])

    cols_order = [
        "city",
        "state",
        "pixels_total",
        "urban_pixels",
        "urban_ratio",
        "water_pixels",
        "densityMi",
        "population",
        "TotalArea",
        "tif_path",
    ]
    df = df[cols_order]

    df.to_csv(OUT_CSV, index=False)
    print(f"\n Saved final cleaned dataset to:\n{OUT_CSV}")


if __name__ == "__main__":
    main()
