import os
import requests
import pandas as pd
import gzip

# NOAA bulk directory
base = "https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/"

years = range(2010, 2025)   # 2010–2024
save_dir = "storm_downloads"
os.makedirs(save_dir, exist_ok=True)

all_records = []

for y in years:
    fname = f"StormEvents_details-ftp_v1.0_d{y}_c20250520.csv.gz"
    url = base + fname
    print("Downloading:", url)

    # download file
    gz_path = f"{save_dir}/{fname}"
    with open(gz_path, "wb") as f:
        f.write(requests.get(url).content)

    # unzip
    try:
        with gzip.open(gz_path, 'rb') as f_in:
            df = pd.read_csv(f_in, low_memory=False)
    except:
        print(f"Error reading {fname}, skipping")
        continue

    # filter flood-related events
    flood_df = df[df["EVENT_TYPE"].str.contains("Flood", case=False, na=False)]

    # filter 3 cities states
    flood_df = flood_df[flood_df["STATE"].isin(["FLORIDA","LOUISIANA","VIRGINIA"])]

    all_records.append(flood_df)

# combine
final = pd.concat(all_records, ignore_index=True)
final.to_csv("flood_events_2010_2024.csv", index=False)

print("\n✔ FINISHED — saved: flood_events_2010_2024.csv")
print("Total rows:", len(final))
