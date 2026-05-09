import pandas as pd
import yfinance as yf
from datetime import datetime

# -----------------------------------
# Load Portfolio Dataset
# -----------------------------------

portfolio_df = pd.read_csv("data/raw/portfolio_data.csv")

# -----------------------------------
# Create Empty Results List
# -----------------------------------

portfolio_summary = []

# -----------------------------------
# Calculate Portfolio Metrics
# -----------------------------------

for index, row in portfolio_df.iterrows():

    ticker = row["ticker"]
    company = row["company_name"]
    portfolio = row["portfolio_name"]
    sector = row["sector"]

    quantity = row["quantity"]
    buy_price = row["buy_price"]
    buy_date = row["buy_date"]

    invested_amount = quantity * buy_price

    print(f"\nProcessing {ticker}...")

    try:

        # Fetch latest market price
        stock = yf.Ticker(ticker)

        latest_price = stock.history(period="1d")["Close"].iloc[-1]

        # Current portfolio value
        current_value = quantity * latest_price

        # Profit / Loss
        profit_loss = current_value - invested_amount

        # Absolute Return %
        absolute_return = (profit_loss / invested_amount) * 100

        # CAGR Calculation
        buy_date_obj = datetime.strptime(buy_date, "%d/%m/%y")

        holding_days = (datetime.today() - buy_date_obj).days

        years_held = holding_days / 365

        if years_held > 0:

            cagr = (
                ((current_value / invested_amount) ** (1 / years_held)) - 1
            ) * 100

        else:
            cagr = 0

        # Append Results
        portfolio_summary.append({

            "Portfolio": portfolio,
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

            "CAGR %": round(cagr, 2)

        })

        print(f"Completed {ticker}")

    except Exception as e:

        print(f"Error processing {ticker}: {e}")

# -----------------------------------
# Convert to DataFrame
# -----------------------------------

summary_df = pd.DataFrame(portfolio_summary)

# -----------------------------------
# Save Summary
# -----------------------------------

summary_df.to_csv(
    "data/exports/portfolio_summary.csv",
    index=False
)

print("\nPortfolio analytics completed successfully.")