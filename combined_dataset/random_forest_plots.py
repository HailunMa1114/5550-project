import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# ===========================
# Load Modeling Dataset
# ===========================
df = pd.read_csv("modeling_dataset.csv")

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

# ===========================
# Fit Random Forest Model
# ===========================
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
print(f"R² Score: {r2}")

importance = model.feature_importances_
sorted_idx = np.argsort(importance)

plt.figure(figsize=(10, 6))
plt.barh(np.array(features)[sorted_idx], importance[sorted_idx], color='tab:blue')
plt.title("Random Forest Feature Importance", fontsize=16)
plt.xlabel("Importance Score")
plt.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("random_forest_feature_importance.png", dpi=300)
print("Generated: random_forest_feature_importance.png")

plt.figure(figsize=(8, 6))
plt.scatter(y, y_pred, s=120, color="tab:orange", edgecolor="black")
plt.plot([0, 1], [0, 1], "k--", alpha=0.6)

plt.title("Random Forest: Actual vs Predicted Exposure Index", fontsize=16)
plt.xlabel("Actual Exposure Index")
plt.ylabel("Predicted Exposure Index")
plt.grid(linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("random_forest_actual_vs_predicted.png", dpi=300)
print("Generated: random_forest_actual_vs_predicted.png")

print("\nAll Random Forest plots completed!")
