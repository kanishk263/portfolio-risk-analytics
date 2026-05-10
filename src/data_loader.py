import pandas as pd


REQUIRED_PORTFOLIO_COLUMNS = [
    "portfolio_name",
    "ticker",
    "company_name",
    "sector",
    "buy_date",
    "quantity",
    "buy_price",
    "exchange",
]


def load_portfolio_data(path):
    """Load and validate the holdings input file."""
    df = pd.read_csv(path)

    missing_columns = [
        column for column in REQUIRED_PORTFOLIO_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            "Portfolio input is missing required columns: "
            + ", ".join(missing_columns)
        )

    if df.empty:
        raise ValueError("Portfolio input file is empty.")

    df = df.copy()
    df["ticker"] = df["ticker"].astype(str).str.strip()
    df["portfolio_name"] = df["portfolio_name"].astype(str).str.strip()
    df["company_name"] = df["company_name"].astype(str).str.strip()
    df["sector"] = df["sector"].astype(str).str.strip()
    df["exchange"] = df["exchange"].astype(str).str.strip()

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["buy_price"] = pd.to_numeric(df["buy_price"], errors="coerce")
    df["buy_date"] = pd.to_datetime(
        df["buy_date"],
        format="%d/%m/%y",
        dayfirst=True,
        errors="coerce",
    )

    invalid_rows = df[
        df["ticker"].eq("")
        | df["buy_date"].isna()
        | df["quantity"].isna()
        | df["buy_price"].isna()
    ]
    if not invalid_rows.empty:
        raise ValueError(
            "Portfolio input has invalid ticker, buy_date, quantity, or buy_price "
            f"values in rows: {', '.join(map(str, invalid_rows.index + 2))}"
        )

    df["buy_date"] = df["buy_date"].dt.strftime("%d/%m/%y")
    return df


if __name__ == "__main__":
    portfolio_df = load_portfolio_data("data/raw/portfolio_data.csv")

    print("\nPortfolio Dataset Loaded Successfully\n")
    print(portfolio_df.head())
