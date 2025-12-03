#!/usr/bin/env python3
"""
High-quality, poster-ready model comparison plot.
"""

import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "modeling_dataset.csv")
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SAVE_PATH = os.path.join(PROJECT_ROOT, "model_performance_comparison_poster.png")

df = pd.read_csv(CSV_PATH)

X = df[[
    "urban_ratio",
    "densityMi",
    "sea_level_trend",
    "sea_level_recent_mean",
    "sea_level_max_anomaly",
    "rain_daily_mean",
    "rain_daily_max",
    "heavy_rain_days_per_year",
]].values
y = df["exposure_index"].values

lin = LinearRegression().fit(X, y)
rf = RandomForestRegressor(n_estimators=200, random_state=42).fit(X, y)

r2_lin = r2_score(y, lin.predict(X))
r2_rf = r2_score(y, rf.predict(X))

sns.set_theme(style="whitegrid")

models = ["Linear Regression", "Random Forest"]
scores = [r2_lin, r2_rf]

palette = sns.color_palette("coolwarm", 2)

plt.figure(figsize=(8, 5), dpi=300)

bars = plt.bar(
    models,
    scores,
    color=palette,
    edgecolor="black",
    linewidth=1.2,
)

for bar, score in zip(bars, scores):
    plt.text(
        bar.get_x() + bar.get_width()/2,
        score + 0.03,
        f"{score:.2f}",
        ha="center", va="bottom",
        fontsize=12, fontweight="bold"
    )

plt.ylim(0, 1.15)

plt.title("Model Performance Comparison (R²)", fontsize=16, fontweight="bold", pad=15)
plt.ylabel("R² Score", fontsize=12)
plt.xticks(fontsize=12)

sns.despine()

plt.tight_layout()
plt.savefig(SAVE_PATH, dpi=300)
plt.close()

print(f"Saved poster-ready plot to:\n{SAVE_PATH}")



