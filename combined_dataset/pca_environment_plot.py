import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os

df = pd.read_csv("modeling_dataset.csv")  

feature_cols = [
    "urban_ratio", "densityMi",
    "sea_level_trend", "sea_level_recent_mean", "sea_level_max_anomaly",
    "rain_daily_mean", "rain_daily_max", "heavy_rain_days_per_year"
]

X = df[feature_cols]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)

df["PC1"] = pca_result[:, 0]
df["PC2"] = pca_result[:, 1]

plt.figure(figsize=(10, 7))
plt.scatter(df["PC1"], df["PC2"], s=300)

for i in range(len(df)):
    plt.text(df["PC1"][i] + 0.02, df["PC2"][i] + 0.02, df["city"][i], fontsize=14)

plt.title("PCA of Environmental Features (3 Cities)", fontsize=18)
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)")
plt.grid(True, linestyle="--", alpha=0.5)

plt.savefig("pca_environment_plot.png", dpi=300)
plt.close()

print("Generated: pca_environment_plot.png")
