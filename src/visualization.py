import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load Sector Allocation Data
# -----------------------------

df = pd.read_csv(
    "data/exports/sector_allocation.csv"
)

# -----------------------------
# Create Pie Chart
# -----------------------------

plt.figure(figsize=(8, 8))

plt.pie(

    df["Allocation %"],

    labels=df["Sector"],

    autopct="%1.1f%%"

)

plt.title("Portfolio Sector Allocation")

# -----------------------------
# Save Visualization
# -----------------------------

plt.savefig(
    "assets/sector_allocation.png"
)

print("\nSector Allocation Chart Saved Successfully.")