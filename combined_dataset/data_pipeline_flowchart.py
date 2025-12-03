#!/usr/bin/env python3
"""
Data pipeline flowchart for 5550 coastal exposure project.

Vertical layout (top -> bottom):
Data Sources -> Cleaning & Harmonization -> Feature Engineering
-> Exposure Index Construction -> Modeling -> Results & Visualization
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.patches import FancyArrow

# ---------- helper: draw one rounded box ----------
def add_box(ax, xy, width, height, text, fontsize=11, facecolor="#e8f1ff"):
    x, y = xy
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.2,
        edgecolor="black",
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        wrap=True,
    )

# ---------- figure setup ----------
fig, ax = plt.subplots(figsize=(5, 10))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

box_w = 0.78
box_h = 0.11
x0 = 0.11

# y positions from top to bottom
ys = [0.83, 0.66, 0.49, 0.32, 0.15, -0.02]

# 1. Data sources
add_box(
    ax,
    (x0, ys[0]),
    box_w,
    box_h,
    "Data Sources\n\n• NOAA sea-level (3 tide gauges)\n"
    "• NCEI daily precipitation\n"
    "• NLCD land cover (urban / water)\n"
    "• Census population & density",
)

# 2. Cleaning & harmonization
add_box(
    ax,
    (x0, ys[1]),
    box_w,
    box_h,
    "Cleaning & Harmonization\n\n"
    "• Remove headers / extra rows\n"
    "• Parse dates, select common years\n"
    "• Aggregate to city-scale metrics",
)

# 3. Feature engineering
add_box(
    ax,
    (x0, ys[2]),
    box_w,
    box_h,
    "Feature Engineering\n\n"
    "• Sea-level trend & anomalies\n"
    "• Heavy-rain threshold & days/year\n"
    "• Urban ratio, population density",
)

# 4. Exposure index construction
add_box(
    ax,
    (x0, ys[3]),
    box_w,
    box_h,
    "Exposure Index Construction\n\n"
    "• Combine urban_ratio and density\n"
    "• Scale to [0, 1] across 3 cities",
)

# 5. Modeling
add_box(
    ax,
    (x0, ys[4]),
    box_w,
    box_h,
    "Modeling\n\n"
    "• Linear regression (baseline)\n"
    "• Random forest (non-linear)\n"
    "• Evaluate with R² and predictions",
)

# 6. Results & visualization
add_box(
    ax,
    (x0, ys[5]),
    box_w,
    box_h,
    "Results & Visualization\n\n"
    "• Coefficient & feature-importance plots\n"
    "• Actual vs predicted exposure index\n"
    "• Correlation heatmap & PCA",
)

# ---------- arrows between boxes ----------
def add_arrow(y_from, y_to):
    ax.add_patch(
        FancyArrow(
            0.5,
            y_from,
            0.0,
            y_to - y_from,
            width=0.0025,
            length_includes_head=True,
            head_width=0.03,
            head_length=0.015,
            color="gray",
        )
    )

for i in range(len(ys) - 1):
    # arrow starts just below upper box, ends just above lower box
    add_arrow(ys[i] - 0.01, ys[i + 1] + box_h + 0.01)

fig.tight_layout()

# 保存到项目根目录，跟其他 png 在一起
fig.savefig("../data_pipeline_flowchart.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("Saved flowchart to ../data_pipeline_flowchart.png")
