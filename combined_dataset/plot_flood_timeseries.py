import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("combined_dataset/flood_events_yearly.csv")

plt.figure(figsize=(10,6))
sns.lineplot(data=df, x="YEAR", y="flood_count", hue="city", marker="o")

plt.title("Observed Annual Flood Events (2010–2024)")
plt.xlabel("Year")
plt.ylabel("Flood Count")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig("combined_dataset/flood_timeseries.png", dpi=300)
print("Saved flood_timeseries.png")
