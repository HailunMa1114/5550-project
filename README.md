## Multi-City Coastal Flood Risk Forecasting Under Sea-Level Rise
DSAN 5550 – Final Project
Author: Helen Ma

# 1. Problem Definition

Coastal cities across the U.S. are experiencing increasing flood frequency due to rising sea levels, urbanization, and more frequent heavy precipitation.
However, most studies:

focus on only one city,

rely heavily on hydrodynamic simulations (ADCIRC, SLOSH),

or lack a unified framework combining built-environment exposure and climate indicators.

Goal:
Build a simple, interpretable, scalable ML framework to forecast coastal flood frequency across Miami (FL), New Orleans (LA), and Norfolk (VA).

Research question:

Can urban exposure + sea-level rise metrics + precipitation extremes predict near-term coastal flood frequency?

Why important?

NOAA projects accelerating sea-level rise along the U.S. East/Southeast coasts.

Local planners need lightweight, city-level tools for risk communication.

ML provides scalable alternatives to physics-based coastal models.

---------------------------------------------------------------------------------------------------------
# 2. Data Collection & Refinement

This project integrates four major datasets:

## 2.1 NOAA Tide-Gauge Records

Daily & annual sea-level values.

Extracted features:

Sea-level trend (mm/year)

Recent mean sea level

Maximum sea-level anomaly

## 2.2 NCEI Daily Precipitation

Extracted:

Maximum daily rainfall

Mean rainfall

Heavy-rain threshold

Heavy-rain days per year

## 2.3 NLCD Land Cover (Urban Ratio)

Used to compute % impervious/urban land.

Core input for exposure index.

## 2.4 U.S. Census (Population Density)
---------------------------------------------------------------------------------------------------------
# Data Cleaning & Harmonization

Removed headers, footers, stray characters.

Normalized city names.

Converted dates to a unified 2010–2024 window.

Aggregated daily → annual metrics.

Standardized all features using min–max scaling.

Built an Exposure Index combining:

Urban ratio

Population density

Formula:

  ExposureIndex_c = 0.5 * ( z(UrbanRatio_c) + z(PopDensity_c) )


Cleaned datasets are stored in:
combined_dataset/

---------------------------------------------------------------------------------------------------------

# 3. Implementation
## 3.1 Modeling Approaches

Two ML models were implemented:

① Linear Regression (baseline)

Interpretable

Shows directional relationships

Uses exposure + sea-level metrics + rainfall extremes

② Random Forest Regression

Captures nonlinear interactions

Better generalization given environmental complexity

## 3.2 Forecasting Framework

Sea-level extrapolation (linear trend):

**SL(τ) = SL(t0) + (τ – t0) * trend**

Forecast horizons:

2030

Pipeline Steps:

Load & clean data

Construct exposure index

Train ML models

Evaluate using R²

Forecast flood counts

Visualize differences

Generate risk maps (Florida, Louisiana, Virginia)

----------------------------------------------------------------------------------------------------------
# 4. Evaluation

## 4.1 Quantitative Metrics
| Model                 | R² Score                               |
| --------------------- | -------------------------------------- |
| **Linear Regression** | **1.00** (overfit due to small sample) |
| **Random Forest**     | **0.81**                               |

---------------------------------------------------------------------------------------------------------
## 4.2 Feature Importance (Random Forest)

Most influential predictors:

Sea-level trend

Maximum daily rainfall

Population density

Sea-level anomaly

---------------------------------------------------------------------------------------------------------

## 4.3 Key Findings

Miami shows the strongest upward flood trajectory.

New Orleans spikes in flood events correspond with extreme sea-level anomalies.

Norfolk has lower exposure yet remains sensitive to sea-level rise.

Exposure index meaningfully captures built-environment vulnerability.

Environmental variables create a transferable, interpretable forecasting system.

---------------------------------------------------------------------------------------------------------

# 5. Visualizations Included

Coastal Flood Risk Heatmap (FL, LA, VA)

Exposure Index vs. Flood Events

Correlation Heatmap of Environmental Features

Observed Flood Events (2010–2024)

Flood Forecasts to 2030

Random Forest Feature Importance

Radar Chart of Environmental Profiles

All plots stored in:

**combined_dataset/plots/**

---------------------------------------------------------------------------------------------------------
# 6. Reproducibility

## 6.1 Run Preprocessing

python combined_dataset/clean_data.py

## 6.2 Train Models
python combined_dataset/model_training.py

## 6.3 Generate Plots

python combined_dataset/plot_exposure_vs_floods.py
python combined_dataset/risk_map_three_states.py
python combined_dataset/flood_forecast_plot.py

## 6.4 Dependencies
pandas
numpy
matplotlib
seaborn
geopandas
rasterio
scikit-learn
shapely
requests

---------------------------------------------------------------------------------------------------------

# 7. Limitations

Only 3 cities → small dataset for ML.

Linear sea-level extrapolation does not capture nonlinear IPCC scenarios.

Does not include storm surge, ENSO, or coastal geomorphology.

Norfolk flood data is sparse.

---------------------------------------------------------------------------------------------------------

# 8. Future Work

Expand to 20+ U.S. coastal cities.

Replace linear sea-level trend with CMIP6 projections.

Add ENSO, storm surge, tidal range predictors.

Use temporal ML models (LSTM, boosted trees).

Incorporate socioeconomic vulnerability (income, elevation, housing age).

