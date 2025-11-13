# -*- coding: utf-8 -*-
"""
build_exposure_index.py
-----------------------------------------
Output:
    combined_dataset/exposure_dataset.csv
-----------------------------------------
"""

import pandas as pd
import numpy as np
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
INPUT_CSV = PROJECT_ROOT / "combined_dataset.csv"
OUTPUT_CSV = PROJECT_ROOT / "exposure_dataset.csv"

print("Loading:", INPUT_CSV)
df = pd.read_csv(INPUT_CSV)

# Check necessary columns
required = ["city", "state", "urban_ratio", "densityMi"]
for col in required:
    if col not in df.columns:
        raise RuntimeError(f" Missing required column: {col}")

# Compute Exposure Raw Score 
df["exposure_raw"] = df["urban_ratio"] * df["densityMi"]

# Normalize to 0–1 
min_val = df["exposure_raw"].min()
max_val = df["exposure_raw"].max()

df["exposure_index"] = (df["exposure_raw"] - min_val) / (max_val - min_val)

# Arrange Columns 
df_out = df[[
    "city", "state",
    "urban_ratio", "densityMi",
    "exposure_raw", "exposure_index"
]]

# Save output 
df_out.to_csv(OUTPUT_CSV, index=False)
print(" Exposure dataset saved to:", OUTPUT_CSV)

print("\n Exposure index complete!")
