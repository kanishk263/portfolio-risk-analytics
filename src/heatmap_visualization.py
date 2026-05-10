import pandas as pd
import os

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib")

import matplotlib.pyplot as plt

# -----------------------------------
# Load Correlation Matrix
# -----------------------------------

corr_df = pd.read_csv(
    "data/exports/correlation_matrix.csv",
    index_col=0
)

# -----------------------------------
# Create Heatmap
# -----------------------------------

plt.figure(figsize=(10, 8))

plt.imshow(corr_df)

plt.colorbar()

plt.xticks(
    range(len(corr_df.columns)),
    corr_df.columns,
    rotation=90
)

plt.yticks(
    range(len(corr_df.columns)),
    corr_df.columns
)

plt.title("Portfolio Correlation Heatmap")

# -----------------------------------
# Save Figure
# -----------------------------------

plt.savefig(
    "assets/correlation_heatmap.png",
    bbox_inches="tight"
)

print("\nCorrelation heatmap saved successfully.")
