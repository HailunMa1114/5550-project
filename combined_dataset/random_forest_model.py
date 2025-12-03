import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib

df = pd.read_csv("modeling_dataset.csv")

y = df["exposure_index"]
feature_cols = [
    "urban_ratio", "densityMi",
    "sea_level_trend", "sea_level_recent_mean", "sea_level_max_anomaly",
    "rain_daily_mean", "rain_daily_max",
    "heavy_rain_days_per_year"
]
X = df[feature_cols]

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X, y)

preds = rf.predict(X)
score = r2_score(y, preds)

print("\n===== Random Forest Model =====")
print("R² Score:", score)

importances = rf.feature_importances_
for f, imp in zip(feature_cols, importances):
    print(f"{f:25s}  →  {imp:.4f}")

joblib.dump(rf, "random_forest_model.pkl")
print("\nModel saved: random_forest_model.pkl")
