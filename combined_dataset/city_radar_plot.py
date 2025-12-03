import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("modeling_dataset.csv")

features = [
    "urban_ratio",
    "densityMi",
    "sea_level_trend",
    "sea_level_recent_mean",
    "rain_daily_max",
    "heavy_rain_days_per_year"
]

cities = df["city"].tolist()
data = df[features].values

data_norm = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

num_vars = len(features)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

colors = ["#4F81BD", "#C0504D", "#9BBB59"]

for i, city in enumerate(cities):
    values = data_norm[i].tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, label=city, color=colors[i])
    ax.fill(angles, values, alpha=0.1, color=colors[i])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(features, fontsize=12)
ax.set_yticklabels([])
ax.set_title("Environmental Profile Radar Chart for 3 Coastal Cities", fontsize=15, pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.savefig("/Users/helen/Desktop/5550 project/city_radar_plot.png", dpi=300)
plt.show()

