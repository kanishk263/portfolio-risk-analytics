import pandas as pd
from pathlib import Path

# -----------------------------------
# Read All Processed Files
# -----------------------------------

processed_folder = Path("data/processed")

all_returns = pd.DataFrame()

# -----------------------------------
# Build Returns Matrix
# -----------------------------------

for file in processed_folder.glob("*.csv"):

    df = pd.read_csv(file)

    ticker = df["Ticker"].iloc[0]

    df["Daily Return"] = df["Close"].pct_change()

    all_returns[ticker] = df["Daily Return"]

# -----------------------------------
# Correlation Matrix
# -----------------------------------

correlation_matrix = all_returns.corr()

# -----------------------------------
# Save Matrix
# -----------------------------------

correlation_matrix.to_csv(
    "data/exports/correlation_matrix.csv"
)

print("\nCorrelation matrix created successfully.")