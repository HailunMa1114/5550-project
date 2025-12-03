import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ------------- Load Data -------------
file_path = os.path.join(os.path.dirname(__file__), "modeling_dataset.csv")
df = pd.read_csv(file_path)

# Select numeric columns only 
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# ------------- Compute Correlation -------------
corr = numeric_df.corr()

# ------------- Plot Heatmap -------------
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

ax = sns.heatmap(
    corr, 
    annot=True, 
    fmt=".2f", 
    cmap="coolwarm", 
    linewidths=.5, 
    square=True, 
    cbar_kws={"shrink": .8}
)

plt.title("Correlation Heatmap of Environmental Features", fontsize=16)
plt.tight_layout()

# Save at project root folder
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "correlation_heatmap.png")
plt.savefig(output_path, dpi=300)

print("Generated:", output_path)
print("Heatmap complete!")
