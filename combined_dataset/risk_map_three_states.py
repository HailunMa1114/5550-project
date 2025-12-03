#!/usr/bin/env python3
"""
Three-state coastal flood risk map using GeoJSON from Natural Earth GitHub mirror.
"""

import os
import requests
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)


GEOJSON_PATH = os.path.join(BASE_DIR, "states.geojson")
GEOJSON_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
    "geojson/ne_110m_admin_1_states_provinces.geojson"
)

if not os.path.exists(GEOJSON_PATH):
    print("Downloading US states GeoJSON...")
    r = requests.get(GEOJSON_URL)
    r.raise_for_status()
    with open(GEOJSON_PATH, "wb") as f:
        f.write(r.content)
    print("Saved:", GEOJSON_PATH)
else:
    print("GeoJSON already exists, skip download.")

states = gpd.read_file(GEOJSON_PATH)
states["name"] = states["name"].str.title()

exposure = pd.read_csv(os.path.join(BASE_DIR, "exposure_dataset.csv"))
flood = pd.read_csv(os.path.join(BASE_DIR, "flood_events_yearly.csv"))

flood_mean = (
    flood.groupby("city")["flood_count"]
    .mean()
    .reset_index(name="flood_mean")
)

df = exposure.merge(flood_mean, on="city", how="left")
df["flood_mean"] = df["flood_mean"].fillna(0)

def norm(col):
    return (col - col.min()) / (col.max() - col.min()) if col.max() > col.min() else 0.5

df["exp_norm"] = norm(df["exposure_index"])
df["flood_norm"] = norm(df["flood_mean"])
df["risk_score"] = 0.5 * df["exp_norm"] + 0.5 * df["flood_norm"]

state_risk = df.groupby("state")["risk_score"].mean().reset_index()

target_states = ["Florida", "Louisiana", "Virginia"]
state_risk = state_risk[state_risk["state"].isin(target_states)]

subset = states[states["name"].isin(target_states)].merge(
    state_risk, left_on="name", right_on="state", how="left"
)

subset["risk_score"] = subset["risk_score"].fillna(0)

fig, ax = plt.subplots(figsize=(8, 6))

subset.boundary.plot(ax=ax, color="black", linewidth=1)
subset.plot(
    ax=ax,
    column="risk_score",
    cmap="Reds",
    legend=True,
    edgecolor="black",
    linewidth=1,
    legend_kwds={"label": "Relative Coastal Flood Risk", "shrink": 0.7}
)

ax.set_title(
    "Coastal Flood Risk Heatmap (Florida, Louisiana, Virginia)",
    fontsize=14
)
ax.axis("off")

OUT_PATH = os.path.join(BASE_DIR, "three_state_risk_map.png")
plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300)
print("✔ Saved:", OUT_PATH)

plt.show()

