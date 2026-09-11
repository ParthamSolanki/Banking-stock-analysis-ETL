from . import config, metrics
from .data_loader_cleaner import data_load_clean


def run_pipeline(
    tickers: list[str] = config.tickers, rf_rate: float = config.default_rf
):

    data = data_load_clean()
    ticker_ohlc = {ticker: data.xs(ticker, axis=1, level=1) for ticker in tickers}

    data_close = data["Close"].copy()
    returns = data_close.pct_change().dropna()

    beta = {
        ticker: metrics.cal_beta(returns[ticker], returns[config.index])
        for ticker in tickers
        if ticker != config.index
    }

    annual_returns = returns.mean() * config.trading_days
    market_return = annual_returns[config.index]

    alpha = {
        ticker: metrics.jensen_alpha(
            beta[ticker], annual_returns[ticker], market_return, rf=rf_rate
        )
        for ticker in tickers
        if ticker != config.index
    }

    sharpe = metrics.sharpe_ratio(returns, rf=rf_rate)

    rsi = metrics.relative_strength_index(data_close)

    return {
        "ohlc": ticker_ohlc,
        "pct_change": returns,
        "beta": beta,
        "alpha": alpha,
        "sharpe": sharpe,
        "rsi": rsi,
    }
