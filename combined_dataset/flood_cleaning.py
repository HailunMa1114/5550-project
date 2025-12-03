import pandas as pd

df = pd.read_csv("data_download/flood_events_2010_2024.csv", low_memory=False)

df = df[df["EVENT_TYPE"].isin(["Flood", "Flash Flood"])]

df["BEGIN_DATE"] = pd.to_datetime(
    df["BEGIN_YEARMONTH"].astype(str) + df["BEGIN_DAY"].astype(str).str.zfill(2),
    format="%Y%m%d",
    errors="coerce"
)

df["YEAR"] = df["BEGIN_DATE"].dt.year
df["MONTH"] = df["BEGIN_DATE"].dt.month

def parse_damage(x):
    if pd.isna(x):
        return 0
    x = str(x)
    if x.endswith("K"):
        return float(x[:-1]) * 1_000
    if x.endswith("M"):
        return float(x[:-1]) * 1_000_000
    return float(x)

df["DAMAGE_PROPERTY_CLEAN"] = df["DAMAGE_PROPERTY"].apply(parse_damage)

df.to_csv("flood_events_cleaned.csv", index=False)

print("Saved → flood_events_cleaned.csv")
print("Total rows:", len(df))
