from pathlib import Path

import pandas as pd
import yfinance as yf

from config import tickers

# Importing raw data
data_raw = yf.download(tickers, period="10y", auto_adjust=True)

# Cleaning 0 and na values
data_dropped = data_raw[~(data_raw == 0).any(axis=1)].copy()
data_dropped = data_dropped[~data_dropped.isna().any(axis=1)].copy()

# Creating copy of data
data_cleaned = data_dropped.copy()

# Changing volume datatype to float
data_cleaned["Volume"] = data_cleaned["Volume"].astype("float64").copy()

# Saving data to parquet
# Anchor to the project root relative to this file
root = Path(__file__).resolve().parent.parent

# Define directories relative to the root
data_dir = root / "data"

# Ensure the directory exists (safe if it already does)
data_dir.mkdir(parents=True, exist_ok=True)

# Export
output_path = data_dir / "data_clean.parquet"
data_cleaned.to_parquet(output_path, index=True)
