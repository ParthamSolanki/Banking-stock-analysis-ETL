import streamlit as st

from src import config, pipeline, plots


@st.cache_data
def load_pipeline_data(rf_rate: float):
    return pipeline.run_pipeline(rf=rf_rate)


st.set_page_config(
    page_title="Banking Stocks Analytics",
    page_icon="📈",
    layout="wide",
)

# plotly config for getting high res output images.
plt_config = {
    "toImageButtonOptions": {
        "format": "png",  # one of png, svg, jpeg, webp
        "filename": "high_res_plot",
        "height": 800,
        "width": 1600,
        "scale": 2,  # Increase this for higher resolution (e.g., 3 or 4)
    }
}

st.sidebar.header("User Parameters")
rf_rate_pct = st.sidebar.number_input(
    "Risk-Free Rate (%)", value=6.75, step=0.25, min_value=0.0, max_value=15.0
)
rf_rate = rf_rate_pct / 100.0

short_ma = st.sidebar.slider("Short Moving Average", 5, 50, 20)
long_ma = st.sidebar.slider("Long Moving Average", 20, 200, 50)

bank_tickers = [t for t in config.tickers if t != config.index]
select_ticker = st.sidebar.selectbox("Select bank for Inspection", bank_tickers)

data = load_pipeline_data(rf_rate=rf_rate)

select_clean = select_ticker.replace(".NS", "")

st.title("Banking Sector Analytics")

tab_1, tab_2, tab_3 = st.tabs(
    ["Asset Deep Dive", "Comparative Analysis & Verdict", "Macro Overview (NSEBANK)"]
)

with tab_1:
    st.header(f"Performance Analysis: {select_clean}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Beta (Sensitivity)", f"{data['beta'][select_ticker]:.3f}")
    col2.metric(label="Jensen's Alpha", value=f"{data['alpha'][select_ticker]:.2f}")
    col3.metric(
        label="Sharpe Ratio",
        value=f"{data['sharpe']['Sharpe Ratio'][select_ticker]:.2%}",
    )
    st.subheader("Price & Moving Averages")
    ticker_ohlc = data["ohlc"][select_ticker]
    candlestick_fig = plots.plot_candlestick_ma(
        ticker_ohlc, select_ticker, short_ma, long_ma
    )

    st.plotly_chart(candlestick_fig, width="stretch", config=plt_config)

    st.subheader(
        body=f"Sensitivity with respect to {config.index.replace('^', '')} (Beta)"
    )
    beta_fig = plots.beta_plot(config.index, select_ticker, data["pct_change"])
    st.pyplot(beta_fig)

    st.subheader(body=f"Relative Strength Index (RSI) of {select_clean}")
    rsi_fig = plots.rsi(select_ticker, data["rsi"])
    st.pyplot(fig=rsi_fig)

with tab_2:
    st.header("Comparative Analysis & Allocation Verdict")

    st.subheader("Performance Comparison (Base ₹100)")
    comp_fig = plots.comparison(data["pct_change"])
    st.pyplot(comp_fig)

    st.subheader("Risk-Adjusted Performance Summary")

    st.subheader("Automated Investment Takeaway")
    best_sharpe_ticker = data["sharpe"]["Sharpe Ratio"].idxmax()
    best_alpha_ticker = data["alpha"].idxmax()

    best_sharpe_val = data["sharpe"]["Sharpe Ratio"].loc[best_sharpe_ticker]
    best_alpha_val = data["alpha"].loc[best_alpha_ticker]

    if best_sharpe_ticker == best_alpha_ticker:
        st.success(
            f"**Top Overall Pick: {best_sharpe_ticker}**\n\n"
            f"Demonstrates superior overall efficiency, generating both the highest "
            f"Sharpe Ratio (**{best_sharpe_val:.2f}**) and highest excess return (**{best_alpha_val:.2%}** Alpha)."
        )
    else:
        st.info(
            f"**Strategic Trade-Off:**\n\n"
            f"* **Best Risk-Adjusted Stability:** **{best_sharpe_ticker}** (Sharpe Ratio: **{best_sharpe_val:.2f}**)\n"
            f"* **Highest Excess Return (Alpha):** **{best_alpha_ticker}** (Alpha: **{best_alpha_val:.2%}**)"
        )

with tab_3:
    st.subheader("Price & Moving Averages")
    ticker_ohlc = data["ohlc"][config.index]
    candlestick_fig = plots.plot_candlestick_ma(
        ticker_ohlc, config.index, short_ma, long_ma
    )
    st.plotly_chart(candlestick_fig, width="stretch", config=plt_config)

    st.subheader(
        body=f"Relative Strength Index (RSI) of {config.index.replace('^', '')}"
    )
    rsi_fig = plots.rsi(config.index, data["rsi"])
    st.pyplot(fig=rsi_fig)
