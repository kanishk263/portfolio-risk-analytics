import pandas as pd
import yfinance as yf

benchmark_df = pd.read_csv("data/benchmark/benchmark_tickers.csv")

for index, row in benchmark_df.iterrows():

    benchmark_name = row["benchmark"]
    ticker = row["ticker"]

    print(f"\nFetching benchmark data for {benchmark_name}")

    data = yf.download(ticker, period="1y")

    data.reset_index(inplace=True)

    output_file = f"data/benchmark/{benchmark_name}.csv"

    data.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")

print("\nBenchmark data fetching completed.")