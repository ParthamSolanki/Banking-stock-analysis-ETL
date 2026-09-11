import time
from pathlib import Path

import pandas as pd
import yfinance as yf

from . import config


def data_load_clean(
    tickers: list[str] = config.tickers, period: str = "10y", max_age_hours: int = 24
) -> pd.DataFrame:
    # If parquet or data file exists then just use that instead of loading from yfinance
    parquet_file = Path(config.parquet_path)
    if parquet_file.exists():
        file_age_hours = (time.time() - parquet_file.stat().st_mtime) / 3600
        if file_age_hours < max_age_hours:
            return pd.read_parquet(parquet_file)

    # Importing raw data
    data_raw = yf.download(tickers, period=period, auto_adjust=True)

    # Cleaning 0 and na values
    data_dropped = data_raw[~(data_raw == 0).any(axis=1)].copy()
    data_dropped = data_dropped[~data_dropped.isna().any(axis=1)].copy()

    # Creating copy of data
    data_cleaned = data_dropped.copy()

    # Changing volume datatype to float
    data_cleaned["Volume"] = data_cleaned["Volume"].astype("float64").copy()

    # Creating parquet file since it doesn't exist and then storing the cleaned data to it
    parquet_file.parent.mkdir(parents=True, exist_ok=True)
    data_cleaned.to_parquet(parquet_file)

    # Return cleaned dataframe
    return data_cleaned
