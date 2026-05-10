import pandas as pd
import yfinance as yf
from pathlib import Path

from data_loader import load_portfolio_data

# -----------------------------------
# Load Portfolio Dataset
# -----------------------------------

portfolio_df = load_portfolio_data("data/raw/portfolio_data.csv")

# -----------------------------------
# Create Empty Results List
# -----------------------------------

portfolio_summary = []


def fetch_latest_price(ticker):
    stock = yf.Ticker(ticker)
    latest_history = stock.history(period="5d")
    if not latest_history.empty:
        return latest_history["Close"].dropna().iloc[-1], stock

    processed_file = Path("data/processed") / f"{ticker.replace('.', '_')}.csv"
    if processed_file.exists():
        processed_df = pd.read_csv(processed_file)
        if "Close" in processed_df.columns and not processed_df["Close"].dropna().empty:
            return processed_df["Close"].dropna().iloc[-1], stock

    raise ValueError("No latest or processed price data available")


def enrich_instrument(stock, fallback_company, fallback_sector, instrument_type):
    company = fallback_company
    sector = fallback_sector

    try:
        info = stock.get_info()
    except Exception:
        info = {}

    if info:
        company = info.get("longName") or info.get("shortName") or company
        if instrument_type.lower() == "mutual fund":
            sector = info.get("category") or "Mutual Fund"
        else:
            sector = info.get("sector") or sector

    if not sector:
        sector = instrument_type

    return company, sector

# -----------------------------------
# Calculate Portfolio Metrics
# -----------------------------------

for index, row in portfolio_df.iterrows():

    ticker = row["Ticker"]
    company = row["Company"]
    portfolio = row["Portfolio"]
    sector = row["Sector"]
    instrument_type = row["Instrument Type"]

    quantity = row["Quantity"]
    buy_price = row["Buy Price"]
    invested_amount = row["Invested Amount"]

    print(f"\nProcessing {ticker}...")

    try:

        latest_price, stock = fetch_latest_price(ticker)
        company, sector = enrich_instrument(
            stock,
            company,
            sector,
            instrument_type,
        )

        # Current portfolio value
        current_value = quantity * latest_price

        # Profit / Loss
        profit_loss = current_value - invested_amount

        # Absolute Return %
        absolute_return = (profit_loss / invested_amount) * 100

        # Append Results
        portfolio_summary.append({

            "Portfolio": portfolio,
            "Instrument Type": instrument_type,
            "Ticker": ticker,
            "Company": company,
            "Sector": sector,

            "Quantity": quantity,
            "Buy Price": buy_price,
            "Current Price": round(latest_price, 2),

            "Invested Amount": round(invested_amount, 2),
            "Current Value": round(current_value, 2),

            "Profit/Loss": round(profit_loss, 2),

            "Absolute Return %": round(absolute_return, 2),

            "CAGR %": "N/A"

        })

        print(f"Completed {ticker}")

    except Exception as e:

        print(f"Error processing {ticker}: {e}")

# -----------------------------------
# Convert to DataFrame
# -----------------------------------

output_columns = [
    "Portfolio",
    "Instrument Type",
    "Ticker",
    "Company",
    "Sector",
    "Quantity",
    "Buy Price",
    "Current Price",
    "Invested Amount",
    "Current Value",
    "Profit/Loss",
    "Absolute Return %",
    "CAGR %",
]

summary_df = pd.DataFrame(portfolio_summary, columns=output_columns)

# -----------------------------------
# Save Summary
# -----------------------------------

summary_df.to_csv(
    "data/exports/portfolio_summary.csv",
    index=False
)

print("\nPortfolio analytics completed successfully.")
