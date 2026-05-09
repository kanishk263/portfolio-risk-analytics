import pandas as pd

def load_portfolio_data(path):
    """
    Load portfolio dataset from CSV file.
    """
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    portfolio_df = load_portfolio_data("data/raw/portfolio_data.csv")

    print("\nPortfolio Dataset Loaded Successfully\n")
    print(portfolio_df.head())