import numpy as np
import pandas as pd

from .config import default_rf, trading_days


def cal_beta(stock: pd.Series, index: pd.Series) -> np.float64:
    matrix = np.cov(stock, index)
    return matrix[0, 1] / matrix[1, 1]


def jensen_alpha(beta_ticker, annual_returns, market_return, rf: float = default_rf):
    expected_return = rf + beta_ticker * (market_return - rf)
    alpha = annual_returns - expected_return
    return alpha


def sharpe_ratio(data_returns, rf: float = default_rf, trading_d: int = trading_days):
    annual_return = data_returns.mean() * trading_d
    annual_volatility = data_returns.std() * np.sqrt(trading_d)

    sharpe_val = (annual_return - rf) / annual_volatility
    sharpe = pd.DataFrame(
        {
            "Annual Returns": annual_return,
            "Annualized Volatility": annual_volatility,
            "Sharpe Ratio": sharpe_val,
        }
    )
    return sharpe


def relative_strength_index(data_closed, window: int = 14) -> pd.Series:
    difference = data_closed.diff()
    gain = difference.where(
        difference > 0, 0
    )  # Place the value in gain series if diff > 0 while placing 0 in the loss series for this day.
    loss = -difference.where(
        difference < 0, 0
    )  # Place the value in loss series if diff > 0 while placing 0 in the loss series for this day.

    # Wilder's Smoothing Method
    # avg_gain = gain.ewm(com=13, min_periods=14).mean()
    # avg_loss = loss.ewm(com=13, min_periods=14).mean()
    # The above two lines are the same as the below 2 in work, as alpha is calculated behind the scenes 1/1+com

    avg_gain = gain.ewm(alpha=1 / window, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.dropna()
