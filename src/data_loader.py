"""Input loading and normalization for portfolio holdings."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


SIMPLE_REQUIRED_COLUMNS = [
    "owner",
    "instrument_type",
    "stock_name",
    "qty",
    "avg_cost",
    "invested_amount",
]

LEGACY_REQUIRED_COLUMNS = [
    "portfolio_name",
    "ticker",
    "company_name",
    "sector",
    "buy_date",
    "quantity",
    "buy_price",
    "exchange",
]

COMMON_INDIAN_ALIASES = {
    "TCS": "TCS.NS",
    "TATA CONSULTANCY SERVICES": "TCS.NS",
    "INFY": "INFY.NS",
    "INFOSYS": "INFY.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "RELIANCE": "RELIANCE.NS",
    "RELIANCE INDUSTRIES": "RELIANCE.NS",
    "ADANIENT": "ADANIENT.NS",
    "ADANI ENTERPRISES": "ADANIENT.NS",
}


def _normalize_column_name(column: str) -> str:
    cleaned = column.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    return cleaned.strip("_")


def _clean_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def _resolve_symbol(value: str) -> str:
    """Resolve a user-entered name/symbol to a Yahoo Finance symbol.

    The simplified input keeps only one instrument identifier column. For best
    results, enter the Yahoo Finance symbol directly, for example `RELIANCE.NS`,
    `TCS.NS`, `AAPL`, or a mutual fund symbol supported by Yahoo Finance.
    A small alias map handles common sample Indian stock names.
    """
    cleaned = _clean_text(value)
    key = cleaned.upper()
    if key in COMMON_INDIAN_ALIASES:
        return COMMON_INDIAN_ALIASES[key]
    return cleaned


def _load_simple_schema(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [
        column for column in SIMPLE_REQUIRED_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            "Portfolio input is missing required columns: "
            + ", ".join(missing_columns)
        )

    normalized = pd.DataFrame()
    normalized["Portfolio"] = df["owner"].map(_clean_text)
    normalized["Instrument Type"] = df["instrument_type"].map(_clean_text).str.title()
    normalized["Input Name"] = df["stock_name"].map(_clean_text)
    normalized["Ticker"] = normalized["Input Name"].map(_resolve_symbol)
    normalized["Quantity"] = pd.to_numeric(df["qty"], errors="coerce")
    normalized["Buy Price"] = pd.to_numeric(df["avg_cost"], errors="coerce")
    normalized["Invested Amount"] = pd.to_numeric(
        df["invested_amount"],
        errors="coerce",
    )

    invalid_rows = normalized[
        normalized["Portfolio"].eq("")
        | normalized["Instrument Type"].eq("")
        | normalized["Ticker"].eq("")
        | normalized["Quantity"].isna()
        | normalized["Buy Price"].isna()
        | normalized["Invested Amount"].isna()
    ]
    if not invalid_rows.empty:
        raise ValueError(
            "Portfolio input has invalid owner, instrument_type, stock_name, qty, "
            "avg_cost, or invested_amount values in rows: "
            f"{', '.join(map(str, invalid_rows.index + 2))}"
        )

    normalized["Company"] = normalized["Input Name"]
    normalized["Sector"] = normalized["Instrument Type"]
    normalized["Exchange"] = ""
    normalized["Buy Date"] = ""
    normalized["CAGR Available"] = False

    return normalized[
        [
            "Portfolio",
            "Instrument Type",
            "Ticker",
            "Company",
            "Sector",
            "Quantity",
            "Buy Price",
            "Invested Amount",
            "Exchange",
            "Buy Date",
            "CAGR Available",
        ]
    ]


def _load_legacy_schema(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [
        column for column in LEGACY_REQUIRED_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            "Portfolio input is missing required columns: "
            + ", ".join(missing_columns)
        )

    normalized = pd.DataFrame()
    normalized["Portfolio"] = df["portfolio_name"].map(_clean_text)
    normalized["Instrument Type"] = "Stock"
    normalized["Ticker"] = df["ticker"].map(_clean_text)
    normalized["Company"] = df["company_name"].map(_clean_text)
    normalized["Sector"] = df["sector"].map(_clean_text)
    normalized["Quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    normalized["Buy Price"] = pd.to_numeric(df["buy_price"], errors="coerce")
    normalized["Invested Amount"] = normalized["Quantity"] * normalized["Buy Price"]
    normalized["Exchange"] = df["exchange"].map(_clean_text)
    normalized["Buy Date"] = pd.to_datetime(
        df["buy_date"],
        format="%d/%m/%y",
        dayfirst=True,
        errors="coerce",
    )
    normalized["CAGR Available"] = normalized["Buy Date"].notna()

    invalid_rows = normalized[
        normalized["Portfolio"].eq("")
        | normalized["Ticker"].eq("")
        | normalized["Buy Date"].isna()
        | normalized["Quantity"].isna()
        | normalized["Buy Price"].isna()
    ]
    if not invalid_rows.empty:
        raise ValueError(
            "Portfolio input has invalid ticker, buy_date, quantity, or buy_price "
            f"values in rows: {', '.join(map(str, invalid_rows.index + 2))}"
        )

    normalized["Buy Date"] = normalized["Buy Date"].dt.strftime("%d/%m/%y")
    return normalized[
        [
            "Portfolio",
            "Instrument Type",
            "Ticker",
            "Company",
            "Sector",
            "Quantity",
            "Buy Price",
            "Invested Amount",
            "Exchange",
            "Buy Date",
            "CAGR Available",
        ]
    ]


def load_portfolio_data(path):
    """Load and validate the holdings input file.

    Preferred simple columns:
    owner, instrument_type, stock_name, qty, avg_cost, invested_amount
    """
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Portfolio input file is empty.")

    df = df.rename(columns={column: _normalize_column_name(column) for column in df.columns})

    if all(column in df.columns for column in SIMPLE_REQUIRED_COLUMNS):
        return _load_simple_schema(df)

    if all(column in df.columns for column in LEGACY_REQUIRED_COLUMNS):
        return _load_legacy_schema(df)

    raise ValueError(
        "Portfolio input does not match the supported schema. Use columns: "
        + ", ".join(SIMPLE_REQUIRED_COLUMNS)
    )


def save_normalized_preview(path: str | Path = "data/exports/normalized_holdings.csv"):
    portfolio_df = load_portfolio_data("data/raw/portfolio_data.csv")
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    portfolio_df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    portfolio_df = load_portfolio_data("data/raw/portfolio_data.csv")
    output_path = save_normalized_preview()

    print("\nPortfolio Dataset Loaded Successfully\n")
    print(portfolio_df.head())
    print(f"\nNormalized preview saved to {output_path}")
