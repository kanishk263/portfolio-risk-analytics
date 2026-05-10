# Data Input Guide

Use this guide when replacing the sample holdings with your own real portfolio data.

## Main Input File

Edit:

```text
data/raw/portfolio_data.csv
```

Current required columns:

| Column | Meaning | Example |
| --- | --- | --- |
| `portfolio_name` | Portfolio, family member, broker, or strategy bucket | `Father`, `Mother`, `Growth`, `Zerodha` |
| `ticker` | Yahoo Finance ticker | `RELIANCE.NS`, `TCS.NS`, `AAPL` |
| `company_name` | Display name | `Reliance Industries` |
| `sector` | Sector classification | `Energy`, `Banking`, `IT` |
| `buy_date` | Original purchase date in `dd/mm/yy` format | `15/01/24` |
| `quantity` | Units or shares held | `10` |
| `buy_price` | Average buy price per unit | `2500` |
| `exchange` | Exchange or market | `NSE`, `BSE`, `NASDAQ` |

## Example

```csv
portfolio_name,ticker,company_name,sector,buy_date,quantity,buy_price,exchange
Father,RELIANCE.NS,Reliance Industries,Energy,15/01/24,5,2500,NSE
Mother,HDFCBANK.NS,HDFC Bank,Banking,20/02/24,10,1450,NSE
Long Term,TCS.NS,TCS,IT,10/01/24,4,3400,NSE
```

## Ticker Rules

- Indian NSE stocks usually end with `.NS`
- Indian BSE stocks usually end with `.BO`
- US stocks generally use the ticker directly, such as `AAPL`, `MSFT`, or `GOOGL`
- Use the ticker format supported by Yahoo Finance because the current market data engine uses `yfinance`

## Refresh Workflow

After editing the CSV, run:

```bash
python main.py
```

The pipeline refreshes:

- `data/processed/`
- `data/exports/`
- `assets/`
- `dashboard/Portfolio_Analytics_Dashboard.xlsx`

## Current Limitation

The current version is holdings-based. Use your latest quantity and average buy price per instrument.

For exact real-world tracking of multiple buys, sells, SIPs, dividends, fees, and realized gains, the next upgrade should introduce a transaction-led model such as `accounts.csv`, `transactions.csv`, and `instruments.csv`.
