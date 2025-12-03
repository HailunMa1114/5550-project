#!/usr/bin/env python3
"""
Linear Regression model for climate exposure index prediction.

"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv("/Users/helen/Desktop/5550 project/combined_dataset/modeling_dataset.csv")

print("\n===== Loaded Modeling Dataset =====")
print(df.head(), "\n")


target = "exposure_index"

features = [
    "urban_ratio",
    "densityMi",
    "sea_level_trend",
    "sea_level_recent_mean",
    "sea_level_max_anomaly",
    "rain_daily_mean",
    "rain_daily_max",
    "heavy_rain_days_per_year"
]

X = df[features]
y = df[target]

print("Using features:", features, "\n")

model = Pipeline([
    ("scaler", StandardScaler()),
    ("lr", LinearRegression())
])

model.fit(X, y)

print("=== Model Fitted ===\n")

coef = model.named_steps["lr"].coef_
intercept = model.named_steps["lr"].intercept_

print("Intercept:", intercept)
print("\nCoefficients:")
for f, c in zip(features, coef):
    print(f"{f:30s} → {c:.4f}")

print("\n")

r2 = model.score(X, y)
print(f"R² Score: {r2:.4f}\n")

df["prediction"] = model.predict(X)

print("===== City Predictions =====")
print(df[["city", "exposure_index", "prediction"]])
print("\nDone.\n")
