import pandas as pd

# -----------------------------
# Load Portfolio Analytics Data
# -----------------------------

df = pd.read_csv(
    "data/exports/portfolio_summary.csv"
)

# -----------------------------
# Aggregate Portfolio Metrics
# -----------------------------

portfolio_summary = (

    df.groupby("Portfolio")[

        [
            "Invested Amount",
            "Current Value",
            "Profit/Loss"
        ]

    ]

    .sum()

    .reset_index()

)

# -----------------------------
# Calculate Portfolio Returns
# -----------------------------

portfolio_summary["Portfolio Return %"] = (

    portfolio_summary["Profit/Loss"]

    /

    portfolio_summary["Invested Amount"]

) * 100

# Round Values
portfolio_summary = portfolio_summary.round(2)

# -----------------------------
# Save Output
# -----------------------------

portfolio_summary.to_csv(
    "data/exports/portfolio_level_summary.csv",
    index=False
)

# -----------------------------
# Display Results
# -----------------------------

print("\nPortfolio-Level Analytics Completed\n")

print(portfolio_summary)