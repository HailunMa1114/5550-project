#!/usr/bin/env python3
"""
Exposure + Flood Frequency → 2030 Risk Index
Generates a bubble + color-scale plot for poster use.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. 读入数据（从项目根目录运行：python combined_dataset/exposure_risk_projection.py）
# --------------------------------------------------
flood = pd.read_csv("combined_dataset/flood_events_yearly.csv")
exposure = pd.read_csv("combined_dataset/exposure_dataset.csv")

# --------------------------------------------------
# 2. 计算每个城市 2010–2021 平均洪水次数
# --------------------------------------------------
flood_mean = (
    flood.groupby("city")["flood_count"]
    .mean()
    .reset_index(name="mean_flood")
)

# --------------------------------------------------
# 3. 合并到 exposure 表
# --------------------------------------------------
df = exposure.merge(flood_mean, on="city", how="left")

# --------------------------------------------------
# 4. 把 mean_flood 标准化到 [0, 1]
# --------------------------------------------------
f_min, f_max = df["mean_flood"].min(), df["mean_flood"].max()
df["flood_norm"] = (df["mean_flood"] - f_min) / (f_max - f_min)

# --------------------------------------------------
# 5. 构建 2030 风险指数（简单加权平均）
#    这里 50% 来自 exposure_index, 50% 来自历史洪水频率
# --------------------------------------------------
df["risk_2030"] = 0.5 * df["exposure_index"] + 0.5 * df["flood_norm"]

# --------------------------------------------------
# 6. 风险等级标签：Low / Medium / High
# --------------------------------------------------
bins = [0, 0.33, 0.66, 1.0]
labels = ["Low", "Medium", "High"]
df["risk_level"] = pd.cut(
    df["risk_2030"], bins=bins, labels=labels, include_lowest=True
)

# --------------------------------------------------
# 7. 为画图准备数据（去掉缺失）
# --------------------------------------------------
plot_df = (
    df.dropna(subset=["risk_2030", "exposure_index", "flood_norm"])
      .reset_index(drop=True)
)

if plot_df.empty:
    raise ValueError("plot_df 为空，请检查 exposure_index / flood_norm / risk_2030 是否都为 NaN。")

# --------------------------------------------------
# 8. 气泡 + 色阶图
# --------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(7.5, 6))

x = plot_df["exposure_index"]
y = plot_df["flood_norm"]
risk = plot_df["risk_2030"]

# 气泡大小：和风险一起变化，但保证有个最小尺寸
sizes = 1500 * (0.3 + risk)   # 可以根据效果再调

scatter = ax.scatter(
    x,
    y,
    s=sizes,
    c=risk,
    cmap="viridis",       # 色阶映射风险
    alpha=0.9,
    edgecolor="black",
    linewidth=0.8,
    zorder=3,
)

# 每个气泡上方写城市名，下方写风险等级
for xi, yi, city, lvl in zip(x, y, plot_df["city"], plot_df["risk_level"]):
    label_city = city.replace("_", " ").title()
    ax.text(
        xi,
        yi + 0.06,
        label_city,
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
    )
    ax.text(
        xi,
        yi - 0.06,
        f"{lvl}",
        ha="center",
        va="top",
        fontsize=10,
    )

# 坐标轴 & 标题
ax.set_xlim(0, 1.05)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Exposure index (population & land use, 0–1)", fontsize=12)
ax.set_ylabel("Historical flood frequency (normalized, 0–1)", fontsize=12)
ax.set_title(
    "Projected 2030 Coastal Flood Risk by City\n"
    "Bubble size & color show combined risk index",
    fontsize=15,
    pad=15,
)

# 色阶条（colorbar）
cbar = fig.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label("Projected 2030 Risk Index (0–1)", fontsize=12)

plt.tight_layout()

# --------------------------------------------------
# 9. 保存图片
# --------------------------------------------------
outpath = Path("combined_dataset/projected_risk_2030_bubble.png")
fig.savefig(outpath, dpi=300)
print("Saved figure to:", outpath)

# 顺便打印一下数据，方便核对
print(
    df[["city", "risk_2030", "risk_level", "exposure_index", "mean_flood"]]
      .sort_values("risk_2030")
      .to_string(index=False)
)



