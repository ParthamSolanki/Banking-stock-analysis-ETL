import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as plotly
import seaborn as sns


def plot_candlestick_ma(
    ticker_df: pd.DataFrame, ticker: str, short_ma: int = 20, long_ma: int = 50
):
    fig = plotly.Figure(
        data=[
            plotly.Candlestick(
                x=ticker_df.index,  # As the index is a datetime index
                open=ticker_df["Open"],
                high=ticker_df["High"],
                low=ticker_df["Low"],
                close=ticker_df["Close"],
                name=ticker,
            )
        ]
    )
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title_text=ticker,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    # Rangleslider = False as other wise it shows a range slider below the viz which is redundant
    ma_short = ticker_df["Close"].rolling(window=short_ma).mean()
    ma_long = ticker_df["Close"].rolling(window=long_ma).mean()
    # rolling makes it so that the mean does the operation for 20 entries, which are 20 trading days worth of data.

    # Adding the moving averages, go to the examples section for individual elements in the documentation.
    fig.add_trace(
        plotly.Scatter(
            x=ticker_df.index,
            y=ma_short,
            mode="lines",
            name=f"{short_ma} Day MA",
            line=dict(color="blue", width=2),
        )
    )

    fig.add_trace(
        plotly.Scatter(
            x=ticker_df.index,
            y=ma_long,
            mode="lines",
            name=f"{long_ma} Day MA",
            line=dict(color="orange", width=2),
        )
    )
    return fig


def beta_plot(index: str, ticker: str, returns: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=index, y=ticker, linewidth=0.5, alpha=0.7, data=returns, ax=ax)

    m, b = np.polyfit(returns[index], returns[ticker], 1)
    x = np.linspace(returns[index].min(), returns[index].max(), 100)
    line = m * x + b

    ax.plot(x, line, color="red", linewidth=2, label=f"Beta: {m:.3f}")

    ax.set_title(f"{ticker.replace('.NS', '')} Sensitivity to Bank Nifty (Beta)")
    ax.set_xlabel(f"{index.replace('^', '')} Daily Returns")
    ax.set_ylabel(f"{ticker.replace('.NS', '')} Daily Returns")
    ax.legend()

    plt.tight_layout()

    return fig


def comparison(returns: pd.DataFrame):
    normalized_df = (1 + returns).cumprod() * 100

    with sns.axes_style(style="whitegrid"):
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            data=normalized_df, palette="tab10", linewidth=1.5, dashes=False, ax=ax
        )
        ticker_list = " vs ".join(
            [ticker.replace(".NS", "").replace("^", "") for ticker in returns.columns]
        )
        ax.set_title(f"Performance Comparison: {ticker_list}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Value of ₹100 Investment")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
    return fig


def sharpe_data(results: pd.DataFrame):
    with sns.axes_style(style="whitegrid"):
        fig, ax = plt.subplots(figsize=(8, 5))

        sns.barplot(
            x=results.index,
            y=results["Sharpe Ratio"],
            hue=results.index,
            palette="viridis",
            legend=False,
            ax=ax,
        )
        ticker_list = " vs ".join(
            [ticker.replace(".NS", "").replace("^", "") for ticker in returns.index]
        )
        ax.set_title(f"Sharpe Ratio: {ticker_list}", fontsize=17)
        ax.set_ylabel("Sharpe Ratio")
        ax.set_xlabel("")
    return fig


def rsi(ticker: str, viz_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=viz_df, x=viz_df.index, y=ticker, ax=ax)
    ax.grid(False)
    ax.axhline(70, color="red", linestyle="--", alpha=0.7)
    ax.axhline(30, color="green", linestyle="--", alpha=0.7)
    ax.set_ylim(0, 100)
    ax.set_title(f"RSI for {ticker}")
    ax.set_ylabel("")
    ax.set_xlabel("")
    plt.tight_layout()
    return fig
