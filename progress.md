1. ✔ Completed Work

Below is a full summary of everything finished so far.
All steps are functioning and all outputs are stored in organized folders.
1.1 Land Cover Exposure (NLCD 2021) — Completed
Downloaded U.S. national NLCD 2021 land cover dataset (.img)
Built land_cover.py to Clip NLCD data for Miami, New Orleans, Norfolk
Compute: total pixels，urban pixels (NLCD 21–24 classes)，urban ratio，water pixels，Save clipped GeoTIFF + summary CSV
Output：land_cover/land_cover_outputs/nlcd_exposure_summary.csv

1.2 Population Density (2025) — Completed
Downloaded united-states-by-density-2025.csv
Used it to attach state population, density, and area for: Florida，Louisiana，Virginia

1.3 Combined Exposure Dataset — Completed
Created folder: combined_dataset/
Built build_combined_dataset.py to merge: NLCD exposure summary，2025 population density CSV
Output：combined_dataset/combined_dataset.csv

1.4 Exposure Index — Completed
Built build_exposure_index.py
Exposure formula uses: urban_ratio，state population density，Min–max normalized result
Output：combined_dataset/exposure_dataset.csv


