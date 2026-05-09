import pandas as pd
from pathlib import Path

processed_folder = Path("data/processed")

all_data = []

for file in processed_folder.glob("*.csv"):

    df = pd.read_csv(file)

    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

combined_df.to_csv(
    "data/exports/combined_market_data.csv",
    index=False
)

print("\nCombined dataset created successfully.")