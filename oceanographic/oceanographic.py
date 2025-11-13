# -*- coding: utf-8 -*-
"""
NOAA Tide Data Downloader & Daily Aggregator
- 下载逐小时潮位 (hourly_height)
- 保存到桌面 ~/Desktop/noaa_raw/
- 合并年度文件 & 生成逐日最大潮位到 ~/Desktop/noaa_daily/
"""

import os
import time
from pathlib import Path
from typing import List, Dict
import requests
import pandas as pd

BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

# ====== 你可以在这里修改配置 ======
YEARS = list(range(2015, 2025))  # 2015-2024
STATIONS: Dict[str, str] = {
    "8723214": "Miami (Virginia Key)",      # Florida
    "8761927": "New Orleans (New Canal)",   # Louisiana
    "8638610": "Norfolk (Sewells Point)",   # Virginia
}
# ==================================

def desktop_path() -> Path:
    # 跨平台获取桌面路径（默认 ~/Desktop）
    d = Path.home() / "Desktop"
    d.mkdir(exist_ok=True)
    return d

def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def fetch_one_year(station_id: str, year: int, out_dir: Path, retries: int = 3, sleep_base: int = 2) -> Path:
    """下载某站点某一年的逐小时潮位CSV，返回保存路径。"""
    params = {
        "begin_date": f"{year}0101",
        "end_date":   f"{year}1231",
        "station": station_id,
        "product": "hourly_height",
        "datum": "MSL",
        "units": "metric",
        "time_zone": "gmt",
        "format": "csv",
    }
    fn = out_dir / f"{station_id}_{year}_hourly.csv"
    if fn.exists() and fn.stat().st_size > 200:  # 已存在且非空
        print(f"⏩ skip existing {fn.name}")
        return fn

    for attempt in range(1, retries + 1):
        try:
            r = requests.get(BASE_URL, params=params, timeout=60)
            r.raise_for_status()
            txt_head = r.text[:200].lower()
            if "<html" in txt_head or "error" in txt_head:
                raise RuntimeError(txt_head[:120])
            fn.write_bytes(r.content)
            print(f"✅ downloaded {fn.name}")
            return fn
        except Exception as e:
            print(f"⚠️ retry {attempt}/{retries} {station_id}-{year}: {e}")
            time.sleep(sleep_base * attempt)
    raise RuntimeError(f"❌ failed {station_id}-{year}")

def merge_years(station_id: str, year_files: List[Path], out_dir: Path) -> Path:
    """合并年度CSV为一个大CSV。"""
    dfs = []
    for p in year_files:
        df = pd.read_csv(p)
        dfs.append(df)
    merged = pd.concat(dfs, ignore_index=True)
    merged_fn = out_dir / f"{station_id}_{YEARS[0]}_{YEARS[-1]}_hourly_merged.csv"
    merged.to_csv(merged_fn, index=False)
    print(f"📦 merged -> {merged_fn.name}")
    return merged_fn

def hourly_to_daily_max(in_csv: Path, city_label: str, out_dir: Path) -> Path:
    """从逐小时CSV生成逐日最大潮位CSV。"""
    df = pd.read_csv(in_csv)
    # 标准化列名
    df.columns = [c.strip().lower().replace("  ", " ") for c in df.columns]

    # 识别时间列 & 水位列（不同站点的列名可能略有不同）
    time_col = next((c for c in ["date time", "date_time", "datetime", "time"] if c in df.columns), None)
    level_col = next((c for c in ["water level", "water_level", "waterlevel", "observed", "value"] if c in df.columns), None)
    if time_col is None or level_col is None:
        raise ValueError(f"列名无法识别，看看这些列：{df.columns.tolist()}")

    # 质量控制（如有“quality/qc/flag”，保留 'v' 或空）
    for qc in ["quality", "qc", "flag"]:
        if qc in df.columns:
            df = df[df[qc].astype(str).str.lower().isin(["v", "nan", ""])]

    # 转时间与聚合
    df["datetime"] = pd.to_datetime(df[time_col], utc=True, errors="coerce")
    df = df.dropna(subset=["datetime"])
    df["date"] = df["datetime"].dt.date
    daily = (df.groupby("date")[level_col]
               .max()
               .reset_index()
               .rename(columns={level_col: "daily_max_tide_m"}))
    daily["city"] = city_label

    out_fn = out_dir / f"{in_csv.stem.replace('_hourly_merged','').replace('_hourly','')}_daily_max.csv"
    daily.to_csv(out_fn, index=False)
    print(f"🗓️ daily -> {out_fn.name} ({len(daily)} rows)")
    return out_fn

def main():
    desk = desktop_path()
    raw_dir = ensure_dir(desk / "noaa_raw")
    daily_dir = ensure_dir(desk / "noaa_daily")

    for station_id, city_label in STATIONS.items():
        print(f"\n=== {city_label} ({station_id}) ===")
        # 逐年下载
        files = [fetch_one_year(station_id, y, raw_dir) for y in YEARS]
        # 合并
        merged = merge_years(station_id, files, raw_dir)
        # 转逐日
        hourly_to_daily_max(merged, city_label, daily_dir)

    print("\n✅ All done.")
    print(f"Raw files dir:    {raw_dir}")
    print(f"Daily files dir:  {daily_dir}")

if __name__ == "__main__":
    main()
