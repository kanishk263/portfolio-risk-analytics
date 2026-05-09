import pandas as pd

# -----------------------------
# Load Portfolio Analytics Data
# -----------------------------

df = pd.read_csv(
    "data/exports/portfolio_summary.csv"
)

# -----------------------------
# Sector Allocation Calculation
# -----------------------------

sector_summary = (

    df.groupby("Sector")["Current Value"]

    .sum()

    .reset_index()

)

# -----------------------------
# Calculate Allocation %
# -----------------------------

total_portfolio_value = sector_summary[
    "Current Value"
].sum()

sector_summary["Allocation %"] = (

    sector_summary["Current Value"]

    / total_portfolio_value

) * 100

# Round Values
sector_summary["Allocation %"] = (
    sector_summary["Allocation %"].round(2)
)

# -----------------------------
# Save Output
# -----------------------------

sector_summary.to_csv(
    "data/exports/sector_allocation.csv",
    index=False
)

# -----------------------------
# Display Results
# -----------------------------

print("\nSector Allocation Analysis Completed\n")

print(sector_summary)