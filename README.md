# Family Investment Intelligence & Wealth Analytics Platform

An automated portfolio analytics platform for tracking investment holdings, measuring performance, evaluating risk, comparing against market benchmarks, and exporting dashboard-ready wealth intelligence outputs.

This project simulates a real-world family office or wealth analytics workflow: transaction and holdings data is ingested, market prices are fetched, analytics are calculated through modular Python engines, and outputs are exported for Excel, Power BI, and executive reporting.

## Project Positioning

The platform is designed to demonstrate the intersection of finance, analytics, automation, quantitative risk analysis, and business intelligence.

It is positioned as more than a basic return tracker. The goal is to build a scalable investment decision-support system that can eventually support multiple family members, accounts, brokers, asset classes, benchmarks, and automated reporting workflows.

## Current Capabilities

- Fetches market data for listed portfolio holdings using `yfinance`
- Tracks invested amount, current value, profit/loss, absolute return, and CAGR
- Produces portfolio-level summaries across strategy buckets
- Calculates annualized return, volatility, Sharpe ratio, and maximum drawdown
- Generates sector allocation analytics
- Builds correlation matrices and heatmap visuals
- Compares portfolio return against benchmark index performance
- Exports dashboard-ready CSV files and an Excel workbook

## Target Platform Scope

The long-term platform is intended to support:

- Individual and consolidated family portfolios
- Broker-specific and account-specific investment views
- Equity, mutual fund, ETF, fixed income, gold, and cash holdings
- Performance, allocation, risk, benchmark, and insight dashboards
- Automated market data, NAV, benchmark, analytics, and reporting refreshes

## Architecture

```text
Investment Data
      |
      v
Data Ingestion Layer
      |
      v
Market Data Engine
      |
      v
Performance Analytics Engine
      |
      v
Risk Analytics Engine
      |
      v
Benchmark Analysis Engine
      |
      v
Visualization and Dashboard Exports
      |
      v
Executive Reporting and Insights
```

## Repository Structure

```text
.
|-- assets/                     # Generated charts and visual outputs
|-- dashboard/                  # Excel dashboard output
|-- data/
|   |-- benchmark/              # Benchmark index data
|   |-- exports/                # Analytics output datasets
|   |-- processed/              # Processed market data by ticker
|   `-- raw/                    # Input portfolio data
|-- reports/                    # Project proposal and roadmap documentation
|-- src/                        # Modular analytics pipeline scripts
|-- main.py                     # End-to-end pipeline runner
`-- requirements.txt            # Python dependencies
```

## Pipeline Modules

| Module | Purpose |
| --- | --- |
| `src/data_fetch.py` | Fetches historical market data for portfolio holdings |
| `src/fetch_benchmark.py` | Fetches benchmark index data |
| `src/combine_data.py` | Combines market data across holdings |
| `src/calculations.py` | Calculates stock-level performance metrics |
| `src/sector_analysis.py` | Generates sector allocation analytics |
| `src/portfolio_summary.py` | Aggregates stock analytics to portfolio level |
| `src/risk_metrics.py` | Calculates volatility, Sharpe ratio, return, and drawdown |
| `src/correlation_analysis.py` | Creates correlation analytics across holdings |
| `src/heatmap_visualization.py` | Generates correlation heatmap output |
| `src/benchmark_analysis.py` | Compares portfolio performance against benchmark return |
| `src/excel_export.py` | Exports analytics tables into an Excel dashboard workbook |

## Outputs

Generated outputs are written to:

- `data/exports/portfolio_summary.csv`
- `data/exports/portfolio_level_summary.csv`
- `data/exports/risk_metrics.csv`
- `data/exports/sector_allocation.csv`
- `data/exports/correlation_matrix.csv`
- `data/exports/benchmark_comparison.csv`
- `dashboard/Portfolio_Analytics_Dashboard.xlsx`
- `assets/correlation_heatmap.png`
- `assets/sector_allocation.png`

## Getting Started

Create or activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the full analytics pipeline:

```bash
python main.py
```

The pipeline reads holdings from `data/raw/portfolio_data.csv`, fetches market and benchmark data, calculates analytics, and refreshes export files.

If you already have the project `venv` available, run:

```bash
source venv/bin/activate
python main.py
```

## Data Input Format

The current raw portfolio file uses the following columns:

| Column | Description |
| --- | --- |
| `portfolio_name` | Portfolio or strategy bucket |
| `ticker` | Market ticker symbol |
| `company_name` | Company or instrument name |
| `sector` | Sector classification |
| `buy_date` | Purchase date |
| `quantity` | Units held |
| `buy_price` | Purchase price per unit |
| `exchange` | Exchange or market |

For detailed instructions on replacing the sample portfolio with your own real data, see [reports/DATA_INPUT_GUIDE.md](/Users/Kanishk/Desktop/portfolio-risk-analytics/reports/DATA_INPUT_GUIDE.md).

## Roadmap

Near-term development priorities:

- Add account holder and broker fields to support family-level consolidation
- Create a transaction-led data model for buys, sells, dividends, SIPs, and realized gains
- Add XIRR, rolling returns, downside risk, beta, alpha, and Value at Risk
- Support mutual funds, ETFs, fixed income, gold, and cash instruments
- Add automated insight generation for concentration, underperformance, and allocation imbalance
- Improve Excel/Power BI dashboard design with KPI cards, slicers, charts, and risk heatmaps
- Add tests, configuration files, and stronger error handling around market data refreshes

See [reports/PROJECT_ROADMAP.md](/Users/Kanishk/Desktop/portfolio-risk-analytics/reports/PROJECT_ROADMAP.md) for the full implementation plan.

## Resume Positioning

> Built an automated family investment intelligence and wealth analytics platform using Python, pandas, yfinance, Excel, and BI-ready data exports to track portfolio performance, evaluate risk, compare benchmarks, analyze diversification, and generate executive-level investment insights.
