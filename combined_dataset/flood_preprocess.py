import pandas as pd

def load_and_process_flood_data(
        path="combined_dataset/flood_events_cleaned.csv"):
    df = pd.read_csv(path)

    df = df[df["EVENT_TYPE"].str.contains("Flood", case=False, na=False)]
    df["YEAR"] = df["YEAR"].astype(int)

    df["CZ_NAME_CLEAN"] = df["CZ_NAME"].str.upper().str.strip()

    CITY_MAP = {
        "ORLEANS": "new_orleans",
        "NEW ORLEANS": "new_orleans",
        "JEFFERSON": "new_orleans",
        "ST. BERNARD": "new_orleans",
        "PLAQUEMINES": "new_orleans",

        "MIAMI-DADE": "miami",
        "MIAMI DADE": "miami",
        "MIAMI": "miami",
        "BROWARD": "miami",
        "MONROE": "miami",

        "NORFOLK (C)": "norfolk",
    }

    df["city"] = df["CZ_NAME_CLEAN"].map(CITY_MAP)
    df = df[df["city"].notna()]

    flood_summary = (
        df.groupby(["city", "YEAR"])
          .size()
          .reset_index(name="flood_count")
          .sort_values(["city", "YEAR"])
    )

    out_path = "combined_dataset/flood_events_yearly.csv"
    flood_summary.to_csv(out_path, index=False)

    print("Saved:", out_path)
    print(flood_summary.head(20))

if __name__ == "__main__":
    load_and_process_flood_data()
