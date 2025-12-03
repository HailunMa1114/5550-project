import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

flood = pd.read_csv("combined_dataset/flood_events_yearly.csv")
exposure = pd.read_csv("combined_dataset/exposure_dataset.csv")

df = flood.merge(exposure[["city", "exposure_index"]], on="city", how="left")

plt.figure(figsize=(10,6))
sns.regplot(
    data=df,
    x="exposure_index",
    y="flood_count",
    scatter_kws={"alpha": 0.7},
    line_kws={"color": "black"}
)

sns.scatterplot(
    data=df,
    x="exposure_index",
    y="flood_count",
    hue="city",
    s=80
)

plt.title("Flood Events vs. Exposure Index (2010–2024)")
plt.xlabel("Exposure Index")
plt.ylabel("Flood Count")

plt.tight_layout()
plt.savefig("combined_dataset/flood_vs_exposure.png", dpi=300)
print("Saved: combined_dataset/flood_vs_exposure.png")
