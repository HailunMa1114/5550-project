# -*- coding: utf-8 -*-
"""
land_cover.py
Clip NLCD 2021 Land Cover (.img, CONUS) for three cities and compute exposure metrics.
Outputs are saved in a subfolder under this script folder:
  - land_cover_outputs/miami_landcover_2021.tif
  - land_cover_outputs/new_orleans_landcover_2021.tif
  - land_cover_outputs/norfolk_landcover_2021.tif
  - land_cover_outputs/nlcd_exposure_summary.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from pyproj import CRS, Transformer
from shapely.geometry import box, mapping

PROJECT_DIR = Path(__file__).resolve().parent

# NLCD national raster 
NLCD_PATH = PROJECT_DIR / "nlcd_2021_land_cover_l48_20230630.img"

# Save outputs to a subfolder under this script folder
OUT_DIR = PROJECT_DIR / "land_cover_outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Format
BBOXES_WGS84 = {
    "miami":       (-80.88, 25.20, -80.03, 25.99),
    "new_orleans": (-90.40, 29.70, -89.60, 30.20),
    "norfolk":     (-76.50, 36.70, -76.00, 37.10),
}

URBAN_CLASSES = (21, 22, 23, 24) 

def clip_by_bbox(src: rasterio.DatasetReader, name: str, bbox_lonlat):
    """
    Clip the NLCD raster by a WGS84 bbox. We avoid EPSG lookups to bypass
    PROJ database conflicts: we build CRS from a proj-string and the raster's WKT.
    """
    left, bottom, right, top = bbox_lonlat

    # Build source/target CRS without EPSG database lookup
    crs_src = CRS.from_string("+proj=longlat +datum=WGS84 +no_defs +type=crs")
    crs_dst = CRS.from_wkt(src.crs.to_wkt())

    # Transform bbox corners from lon/lat to the raster's projected CRS
    transformer = Transformer.from_crs(crs_src, crs_dst, always_xy=True)
    xs = [left, right, right, left]
    ys = [bottom, bottom, top, top]
    X, Y = transformer.transform(xs, ys)

    # Make a minimal bounding rectangle in projected coordinates
    minx, maxx = min(X), max(X)
    miny, maxy = min(Y), max(Y)
    geom = box(minx, miny, maxx, maxy)

    out_image, out_transform = mask(src, [mapping(geom)], crop=True, nodata=0)

    # Write GeoTIFF
    meta = src.meta.copy()
    meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width":  out_image.shape[2],
        "transform": out_transform,
        "dtype": src.dtypes[0],
    })
    out_tif = OUT_DIR / f"{name}_landcover_2021.tif"
    with rasterio.open(out_tif, "w", **meta) as dst:
        dst.write(out_image)

    return out_tif, out_image[0] 
def summarize(arr: np.ndarray):
    """
    Compute exposure metrics: total pixels, urban pixels (21–24),
    urban ratio, and water pixels (11).
    """
    valid = arr != 0  
    total = int(valid.sum())
    vals, cnts = np.unique(arr[valid], return_counts=True)
    m = {int(v): int(c) for v, c in zip(vals, cnts)}
    urban = sum(m.get(v, 0) for v in URBAN_CLASSES)
    water = m.get(11, 0) 
    return {
        "pixels_total": total,
        "urban_pixels": urban,
        "urban_ratio": round(urban / total, 4) if total else 0.0,
        "water_pixels": water
    }

def main():
    if not NLCD_PATH.exists():
        raise FileNotFoundError(f"NLCD file not found: {NLCD_PATH}\n"
                                f"Ensure .img/.ige/.xml are in the same folder.")

    print(f"Reading NLCD: {NLCD_PATH}")
    with rasterio.open(NLCD_PATH) as src:
        print(f"  CRS: {src.crs}")
        print(f"  Size: {src.width} x {src.height}")

        rows = []
        for city, bbox in BBOXES_WGS84.items():
            print(f"\n→ Clipping {city} ...")
            out_tif, arr = clip_by_bbox(src, city, bbox)
            stats = summarize(arr)
            stats["city"] = city
            stats["tif_path"] = str(out_tif)
            rows.append(stats)
            print(f"  Saved {out_tif.name} | urban_ratio={stats['urban_ratio']}")

    df = pd.DataFrame(rows)[["city", "pixels_total", "urban_pixels", "urban_ratio", "water_pixels", "tif_path"]]
    summary_csv = OUT_DIR / "nlcd_exposure_summary.csv"
    df.to_csv(summary_csv, index=False)
    print("\nDone! Summary written to:", summary_csv)

if __name__ == "__main__":
    main()
