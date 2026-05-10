# Data Input Guide

Use this guide when replacing the sample holdings with your own real portfolio data.

## Main Input File

Edit:

```text
data/raw/portfolio_data.csv
```

## Required Columns

The input file is intentionally simple. You only need to maintain these columns:

| Column | Meaning | Example |
| --- | --- | --- |
| `owner` | Family member, account, broker, or portfolio bucket | `Father`, `Mother`, `Zerodha`, `Growth` |
| `instrument_type` | Type of investment | `Stock`, `Mutual Fund` |
| `stock_name` | Yahoo Finance symbol or supported alias | `RELIANCE.NS`, `TCS.NS`, `AAPL` |
| `qty` | Units or shares held | `10` |
| `avg_cost` | Average purchase cost per unit | `2500` |
| `invested_amount` | Total amount invested | `25000` |

## Example

```csv
owner,instrument_type,stock_name,qty,avg_cost,invested_amount
Father,Stock,RELIANCE.NS,5,2500,12500
Mother,Stock,HDFCBANK.NS,10,1450,14500
Long Term,Stock,TCS.NS,4,3400,13600
```

## Important Ticker Rules

The system fetches prices using Yahoo Finance through `yfinance`.

- Indian NSE stocks usually end with `.NS`, such as `RELIANCE.NS`
- Indian BSE stocks usually end with `.BO`
- US stocks generally use the ticker directly, such as `AAPL`, `MSFT`, or `GOOGL`
- Mutual funds can be used if Yahoo Finance supports the symbol you enter
- Common aliases like `TCS`, `Infosys`, `HDFC Bank`, `ICICI Bank`, `Reliance`, and `Adani Enterprises` are mapped automatically

For best results, enter the Yahoo Finance symbol directly in `stock_name`.

## Mutual Funds

For mutual funds, keep `instrument_type` as `Mutual Fund`.

```csv
owner,instrument_type,stock_name,qty,avg_cost,invested_amount
Father,Mutual Fund,0P0000XVU7.BO,100,50,5000
```

Mutual fund automation depends on whether Yahoo Finance provides data for that fund symbol. If Yahoo Finance does not support the fund, the pipeline cannot automatically fetch NAV yet. In that case, the next upgrade should add a manual NAV input or an India-specific mutual fund NAV data source.

## Refresh Workflow

After editing the CSV, run:

```bash
source venv/bin/activate
python main.py
```

The pipeline refreshes:

- `data/processed/`
- `data/exports/`
- `assets/`
- `dashboard/Portfolio_Analytics_Dashboard.xlsx`

## Current Limitation

The current version is holdings-based. Use your latest quantity and average cost per instrument.

Because the simplified input does not include purchase dates, CAGR is shown as `N/A`. Absolute return, profit/loss, allocation, risk, benchmark comparison, and dashboard analytics still refresh normally.
