import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------------
# Processed Market Data Folder
# -----------------------------------

processed_folder = Path("data/processed")

# -----------------------------------
# Store Risk Metrics
# -----------------------------------

risk_results = []

# -----------------------------------
# Calculate Risk Metrics
# -----------------------------------

for file in processed_folder.glob("*.csv"):

    df = pd.read_csv(file)

    ticker = df["Ticker"].iloc[0]

    print(f"\nCalculating risk metrics for {ticker}")

    # -----------------------------------
    # Daily Returns
    # -----------------------------------

    df["Daily Return"] = df["Close"].pct_change()

    returns = df["Daily Return"].dropna()

    # -----------------------------------
    # Annualized Volatility
    # -----------------------------------

    volatility = returns.std() * np.sqrt(252)

    # -----------------------------------
    # Annualized Return
    # -----------------------------------

    annual_return = returns.mean() * 252

    # -----------------------------------
    # Sharpe Ratio
    # Assume Risk-Free Rate = 7%
    # -----------------------------------

    risk_free_rate = 0.07

    sharpe_ratio = (

        annual_return - risk_free_rate

    ) / volatility

    # -----------------------------------
    # Maximum Drawdown
    # -----------------------------------

    cumulative_returns = (

        1 + returns

    ).cumprod()

    rolling_max = cumulative_returns.cummax()

    drawdown = (

        cumulative_returns - rolling_max

    ) / rolling_max

    max_drawdown = drawdown.min()

    # -----------------------------------
    # Store Results
    # -----------------------------------

    risk_results.append({

        "Ticker": ticker,

        "Annual Return": round(
            annual_return * 100, 2
        ),

        "Volatility": round(
            volatility * 100, 2
        ),

        "Sharpe Ratio": round(
            sharpe_ratio, 2
        ),

        "Maximum Drawdown": round(
            max_drawdown * 100, 2
        )

    })

# -----------------------------------
# Create DataFrame
# -----------------------------------

risk_df = pd.DataFrame(risk_results)

# -----------------------------------
# Save Results
# -----------------------------------

risk_df.to_csv(
    "data/exports/risk_metrics.csv",
    index=False
)

print("\nRisk analytics completed successfully.")