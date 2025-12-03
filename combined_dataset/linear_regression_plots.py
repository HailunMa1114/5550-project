# linear_regression_plots.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("/Users/helen/Desktop/5550 project/combined_dataset/modeling_dataset.csv")

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

model = LinearRegression()
model.fit(X, y)

plt.figure(figsize=(10, 6))
coef = model.coef_
plt.barh(features, coef, color="steelblue")
plt.title("Linear Regression Coefficients", fontsize=16)
plt.xlabel("Coefficient Value")
plt.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("linear_coefficients.png", dpi=300)
plt.close()

print("Generated: linear_coefficients.png")

y_pred = model.predict(X)

plt.figure(figsize=(6, 6))
plt.scatter(y, y_pred, color="darkorange", s=80)
plt.plot([0, 1], [0, 1], "--", color="gray")  
plt.xlabel("Actual Exposure Index")
plt.ylabel("Predicted Exposure Index")
plt.title("Actual vs Predicted Exposure Index")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("actual_vs_predicted.png", dpi=300)
plt.close()

print("Generated: actual_vs_predicted.png")

print("\nAll linear regression plots completed!")
