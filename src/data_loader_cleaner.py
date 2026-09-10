import pandas as pd
import yfinance as yf

from . import config


def data_load_clean(
    tickers: list[str] = config.tickers, period: str = "10y"
) -> pd.DataFrame:
    # Importing raw data
    data_raw = yf.download(tickers, period=period, auto_adjust=True)

    # Cleaning 0 and na values
    data_dropped = data_raw[~(data_raw == 0).any(axis=1)].copy()
    data_dropped = data_dropped[~data_dropped.isna().any(axis=1)].copy()

    # Creating copy of data
    data_cleaned = data_dropped.copy()

    # Changing volume datatype to float
    data_cleaned["Volume"] = data_cleaned["Volume"].astype("float64").copy()

    # Return cleaned dataframe
    return data_cleaned
