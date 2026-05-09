import pandas as pd

# -----------------------------------
# Load Portfolio Summary
# -----------------------------------

portfolio_df = pd.read_csv(
    "data/exports/portfolio_level_summary.csv"
)

# -----------------------------------
# Load Benchmark Data
# -----------------------------------

nifty_df = pd.read_csv(
    "data/benchmark/NIFTY.csv"
)

# -----------------------------------
# Benchmark Returns
# -----------------------------------

# Convert Close column to numeric

nifty_df["Close"] = pd.to_numeric(
    nifty_df["Close"],
    errors="coerce"
)

# Remove missing values

nifty_df = nifty_df.dropna(subset=["Close"])

# Benchmark prices

start_price = nifty_df["Close"].iloc[0]
end_price = nifty_df["Close"].iloc[-1]

benchmark_return = (

    (end_price - start_price)

    / start_price

) * 100

# -----------------------------------
# Compare With Portfolios
# -----------------------------------

portfolio_df["Benchmark Return %"] = round(
    benchmark_return,
    2
)

portfolio_df["Outperformance"] = (

    portfolio_df["Portfolio Return %"]

    - benchmark_return

).round(2)

# -----------------------------------
# Save Output
# -----------------------------------

portfolio_df.to_csv(
    "data/exports/benchmark_comparison.csv",
    index=False
)

print("\nBenchmark comparison completed.")