import pandas as pd

# -----------------------------------
# Load All Analytics Datasets
# -----------------------------------

portfolio_summary = pd.read_csv(
    "data/exports/portfolio_summary.csv"
)

portfolio_level = pd.read_csv(
    "data/exports/portfolio_level_summary.csv"
)

sector_allocation = pd.read_csv(
    "data/exports/sector_allocation.csv"
)

risk_metrics = pd.read_csv(
    "data/exports/risk_metrics.csv"
)

benchmark_comparison = pd.read_csv(
    "data/exports/benchmark_comparison.csv"
)

# -----------------------------------
# Create Excel Workbook
# -----------------------------------

output_file = "dashboard/Portfolio_Analytics_Dashboard.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="xlsxwriter"
) as writer:

    portfolio_summary.to_excel(
        writer,
        sheet_name="Stock Analytics",
        index=False
    )

    portfolio_level.to_excel(
        writer,
        sheet_name="Portfolio Summary",
        index=False
    )

    sector_allocation.to_excel(
        writer,
        sheet_name="Sector Allocation",
        index=False
    )

    risk_metrics.to_excel(
        writer,
        sheet_name="Risk Metrics",
        index=False
    )

    benchmark_comparison.to_excel(
        writer,
        sheet_name="Benchmark Comparison",
        index=False
    )

print("\nExcel dashboard data exported successfully.")