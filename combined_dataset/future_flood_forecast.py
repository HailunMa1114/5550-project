import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

df = pd.read_csv("combined_dataset/flood_events_yearly.csv")

plt.figure(figsize=(10,6))

cities = df["city"].unique()

for city in cities:
    temp = df[df["city"] == city].copy()
    X = temp["YEAR"].values.reshape(-1, 1)
    y = temp["flood_count"].values

    model = LinearRegression()
    model.fit(X, y)

    # Predict until 2030
    future_years = np.arange(2010, 2031).reshape(-1, 1)
    future_pred = model.predict(future_years)

    # Plot actual data
    plt.plot(temp["YEAR"], temp["flood_count"], "o-", label=f"{city} (actual)")

    # Plot forecast
    plt.plot(future_years, future_pred, "--", label=f"{city} (forecast)")

plt.title("Flood Events Forecast (2010–2030)")
plt.xlabel("Year")
plt.ylabel("Flood Count")
plt.legend()
plt.tight_layout()

plt.savefig("combined_dataset/future_flood_forecast.png", dpi=300)
print("Saved: combined_dataset/future_flood_forecast.png")
