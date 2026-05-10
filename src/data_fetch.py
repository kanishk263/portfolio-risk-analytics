import pandas as pd
import yfinance as yf
from pathlib import Path

from data_loader import load_portfolio_data

# -----------------------------
# Load Portfolio Dataset
# -----------------------------

portfolio_path = "data/raw/portfolio_data.csv"

portfolio_df = load_portfolio_data(portfolio_path)

# Extract unique tickers
tickers = portfolio_df["Ticker"].unique()

# Create processed data folder if not exists
processed_folder = Path("data/processed")
processed_folder.mkdir(parents=True, exist_ok=True)

# Remove stale files so the processed folder matches the current raw input.
for old_file in processed_folder.glob("*.csv"):
    old_file.unlink()

# -----------------------------
# Fetch Historical Market Data
# -----------------------------

for ticker in tickers:

    print(f"\nFetching data for {ticker}...")

    try:
        stock = yf.Ticker(ticker)

        hist_data = stock.history(period="1y")

        if hist_data.empty:
            raise ValueError("No historical market data returned")

        # Reset index
        hist_data.reset_index(inplace=True)

        # Add ticker column
        hist_data["Ticker"] = ticker

        # Clean filename
        clean_name = ticker.replace(".", "_")

        # Save CSV
        output_path = processed_folder / f"{clean_name}.csv"

        hist_data.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

print("\nMarket data fetching completed.")
