# Family Investment Intelligence & Wealth Analytics Platform Roadmap

## 1. Project Summary

The project aims to build a centralized wealth analytics platform for monitoring family investments across accounts, brokers, asset classes, and strategy buckets. It combines financial analytics, market data automation, risk measurement, benchmark comparison, dashboard exports, and executive insight generation.

The current repository already implements the first version of this system for listed equity holdings. It includes a complete Python pipeline that reads portfolio holdings, fetches market data, calculates performance and risk metrics, compares against benchmarks, creates allocation/correlation outputs, and exports dashboard-ready files.

## 2. Current Repo Assessment

### Implemented

- Holdings ingestion from `data/raw/portfolio_data.csv`
- Historical equity market data fetching through `src/data_fetch.py`
- Benchmark data fetching through `src/fetch_benchmark.py`
- Stock-level performance analytics through `src/calculations.py`
- Portfolio-level summaries through `src/portfolio_summary.py`
- Sector allocation analytics through `src/sector_analysis.py`
- Risk metrics through `src/risk_metrics.py`
- Correlation analytics and heatmap generation
- Benchmark return comparison through `src/benchmark_analysis.py`
- Excel dashboard export through `src/excel_export.py`
- End-to-end orchestration through `main.py`

### Current Limitations

- Current input is holdings-based, not transaction-based
- Family members, account holders, brokers, and account types are not yet modeled
- Realized gains, dividends, SIP flows, XIRR, and cash flows are not yet captured
- Asset-class coverage is currently equity-focused
- Risk analytics cover core metrics but not beta, alpha, VaR, downside risk, or rolling returns
- Benchmark comparison currently uses a single benchmark return rather than instrument-specific or portfolio-weighted benchmark mapping
- Dashboard output is data-export focused and can be enhanced into a more polished executive workbook or Power BI model

## 3. Target Architecture

```text
Account and Transaction Data
        |
        v
Data Validation and Cleaning
        |
        v
Instrument Master and Classification
        |
        v
Market Data and Benchmark Data Refresh
        |
        v
Performance Analytics Engine
        |
        v
Allocation and Diversification Engine
        |
        v
Risk Analytics Engine
        |
        v
Benchmark and Attribution Engine
        |
        v
Insight Generation Engine
        |
        v
Excel, Power BI, Plotly, and Report Exports
```

## 4. Recommended Data Model

### `accounts.csv`

| Column | Purpose |
| --- | --- |
| `account_id` | Unique account identifier |
| `holder_name` | Family member or entity name |
| `account_type` | Individual, joint, demat, mutual fund, savings, retirement |
| `broker` | Broker, bank, AMC, or platform |
| `base_currency` | Reporting currency |
| `status` | Active or inactive |

### `transactions.csv`

| Column | Purpose |
| --- | --- |
| `transaction_id` | Unique transaction identifier |
| `account_id` | Link to account master |
| `date` | Transaction date |
| `instrument_id` | Link to instrument master |
| `transaction_type` | Buy, sell, dividend, interest, SIP, redemption, fee |
| `quantity` | Units transacted |
| `price` | Transaction price |
| `amount` | Gross transaction amount |
| `fees` | Brokerage, taxes, or other charges |
| `currency` | Transaction currency |

### `instruments.csv`

| Column | Purpose |
| --- | --- |
| `instrument_id` | Unique instrument identifier |
| `ticker` | Market ticker or fund code |
| `name` | Instrument name |
| `asset_class` | Equity, mutual fund, ETF, fixed income, gold, cash |
| `sector` | Sector classification |
| `geography` | India, US, international, global |
| `benchmark` | Relevant benchmark mapping |
| `data_source` | yfinance, manual, AMC, bank, broker |

### `prices.csv`

| Column | Purpose |
| --- | --- |
| `date` | Price date |
| `instrument_id` | Link to instrument master |
| `close_price` | Closing price or NAV |
| `source` | Data provider |

## 5. Implementation Milestones

### Milestone 1: Strengthen Existing Equity Pipeline

- Replace hard-coded paths with a central config file
- Add validation for missing columns, invalid dates, and empty market data responses
- Standardize date formats across raw, processed, and export files
- Add logging instead of relying only on print statements
- Add basic tests for performance and risk calculations

### Milestone 2: Multi-Account Family Model

- Extend raw input to include `account_id`, `holder_name`, `broker`, and `account_type`
- Generate account-wise, holder-wise, broker-wise, and family-level summaries
- Export consolidated family wealth views
- Add account allocation charts and tables

### Milestone 3: Transaction Engine

- Introduce a transaction-led model for buys, sells, SIPs, dividends, interest, fees, and redemptions
- Calculate current holdings from transaction history
- Add realized gains and realized income tracking
- Add cash-flow-aware XIRR calculations

### Milestone 4: Asset Class Expansion

- Add mutual fund support with NAV-based valuation
- Add ETF support using the existing equity-style price pipeline
- Add fixed income support with manual valuation and accrued interest assumptions
- Add gold support for SGBs, gold ETFs, and physical gold valuation
- Add cash and savings balances for total wealth reporting

### Milestone 5: Advanced Risk and Benchmark Analytics

- Add beta and alpha versus mapped benchmark
- Add downside deviation and Sortino ratio
- Add historical and parametric Value at Risk
- Add rolling 1-month, 3-month, 6-month, and 1-year returns
- Add rolling volatility and drawdown charts
- Add benchmark mapping by instrument or portfolio strategy

### Milestone 6: Investment Insight Engine

- Generate automated insights for sector concentration, asset-class imbalance, and single-stock exposure
- Flag underperforming holdings versus benchmark
- Highlight top contributors and detractors
- Identify portfolios with weak risk-adjusted performance
- Add threshold-based alerts for concentration and drawdown

### Milestone 7: Executive Dashboard and Reporting

- Upgrade the Excel workbook with formatted KPI sheets, charts, filters, and executive summary sections
- Create a Power BI-ready star schema export
- Add Plotly charts for interactive analysis
- Add automated PDF or HTML reporting as a future enhancement

## 6. Dashboard Blueprint

### Executive Wealth Dashboard

- Total invested amount
- Current family wealth value
- Unrealized gains/losses
- Absolute return and CAGR
- Best and worst performing portfolios
- Asset allocation overview

### Portfolio Analytics Dashboard

- Portfolio-wise invested amount, value, return, and CAGR
- Holding-level performance table
- Monthly performance trend
- Top gainers and laggards

### Risk Analytics Dashboard

- Volatility
- Sharpe ratio
- Maximum drawdown
- Beta and alpha
- VaR
- Correlation heatmap

### Allocation Dashboard

- Asset class allocation
- Sector allocation
- Geography allocation
- Account-wise allocation
- Broker-wise allocation

### Benchmark Dashboard

- Portfolio return versus NIFTY, SENSEX, and mapped benchmarks
- Alpha
- Relative return
- Outperformance summary

### Insights Dashboard

- Concentration warnings
- Diversification gaps
- Underperforming holdings
- Allocation imbalance alerts
- Risk-adjusted return quality

## 7. Suggested Resume Bullets

- Built an automated investment analytics platform using Python, pandas, yfinance, and Excel to track portfolio performance, risk, allocation, and benchmark comparison across multiple investment portfolios.
- Designed a modular wealth analytics pipeline covering market data ingestion, portfolio valuation, sector allocation, risk metrics, benchmark analysis, dashboard exports, and executive insight generation.
- Implemented quantitative risk analytics including volatility, Sharpe ratio, maximum drawdown, correlation analysis, and benchmark outperformance measurement for portfolio decision support.

## 8. Interview Talking Points

- Explain how the project converts raw investment holdings into analytics-ready outputs through an automated ETL pipeline.
- Discuss the difference between simple return tracking and decision-support analytics.
- Highlight how benchmark comparison, risk-adjusted returns, and concentration analysis make the platform more business-relevant.
- Describe how the current equity pipeline can scale into a transaction-based multi-asset family wealth platform.
- Emphasize practical business use cases in wealth management, investment advisory, FP&A, analytics, and consulting.
