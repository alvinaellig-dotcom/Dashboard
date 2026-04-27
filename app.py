from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Finance Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@dataclass(frozen=True)
class StockProfile:
    name: str
    sector: str
    start_price: float
    drift: float
    volatility: float


STOCKS: dict[str, StockProfile] = {
    "AAPL": StockProfile("Apple Inc.", "Technology", 172.0, 0.00048, 0.014),
    "MSFT": StockProfile("Microsoft", "Technology", 395.0, 0.00052, 0.013),
    "GOOGL": StockProfile("Alphabet", "Communication Services", 138.0, 0.00044, 0.016),
    "AMZN": StockProfile("Amazon", "Consumer Discretionary", 154.0, 0.0005, 0.018),
    "NVDA": StockProfile("NVIDIA", "Semiconductors", 610.0, 0.00078, 0.024),
    "JPM": StockProfile("JPMorgan Chase", "Financials", 172.0, 0.00034, 0.011),
    "V": StockProfile("Visa", "Financials", 268.0, 0.00036, 0.01),
    "TSLA": StockProfile("Tesla", "Consumer Discretionary", 215.0, 0.00046, 0.029),
}

DEFAULT_SHARES = {
    "AAPL": 22,
    "MSFT": 12,
    "GOOGL": 18,
    "AMZN": 16,
    "NVDA": 8,
    "JPM": 20,
    "V": 10,
    "TSLA": 9,
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --card-bg: rgba(255, 255, 255, 0.78);
                --card-border: rgba(15, 23, 42, 0.08);
                --muted: #64748b;
                --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
            }

            .block-container {
                padding-top: 1.25rem;
                padding-bottom: 2rem;
                max-width: 1240px;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
            }

            [data-testid="stSidebar"] * {
                color: #f8fafc;
            }

            [data-testid="stSidebar"] .stMultiSelect div,
            [data-testid="stSidebar"] .stDateInput div,
            [data-testid="stSidebar"] .stNumberInput div,
            [data-testid="stSidebar"] .stSelectbox div {
                color: #0f172a;
            }

            .hero {
                background:
                    radial-gradient(circle at top left, rgba(14, 165, 233, 0.22), transparent 32%),
                    linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0369a1 100%);
                border-radius: 28px;
                color: white;
                padding: 2rem;
                box-shadow: var(--shadow);
                margin-bottom: 1.3rem;
            }

            .hero h1 {
                margin: 0;
                font-size: clamp(2rem, 6vw, 4.25rem);
                line-height: 1;
                letter-spacing: -0.06em;
            }

            .hero p {
                color: rgba(255, 255, 255, 0.78);
                font-size: 1.05rem;
                margin: 0.75rem 0 0;
                max-width: 760px;
            }

            .metric-card {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 22px;
                box-shadow: var(--shadow);
                padding: 1.05rem 1.15rem;
                min-height: 132px;
            }

            .metric-label {
                color: var(--muted);
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }

            .metric-value {
                color: #0f172a;
                font-size: clamp(1.65rem, 4vw, 2.55rem);
                font-weight: 800;
                letter-spacing: -0.04em;
                margin-top: 0.2rem;
            }

            .metric-delta {
                font-size: 0.95rem;
                font-weight: 700;
                margin-top: 0.25rem;
            }

            .positive { color: #059669; }
            .negative { color: #dc2626; }
            .neutral { color: #64748b; }

            .section-title {
                color: #0f172a;
                font-size: 1.15rem;
                font-weight: 800;
                letter-spacing: -0.02em;
                margin: 1rem 0 0.25rem;
            }

            [data-testid="stDataFrame"] {
                border: 1px solid var(--card-border);
                border-radius: 18px;
                overflow: hidden;
                box-shadow: var(--shadow);
            }

            @media (max-width: 768px) {
                .block-container {
                    padding-left: 0.85rem;
                    padding-right: 0.85rem;
                    padding-top: 0.75rem;
                }

                .hero {
                    border-radius: 20px;
                    padding: 1.25rem;
                }

                .metric-card {
                    min-height: auto;
                    padding: 0.95rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def build_price_history(tickers: tuple[str, ...], start: date, end: date) -> pd.DataFrame:
    business_days = pd.bdate_range(start, end)
    if business_days.empty:
        business_days = pd.DatetimeIndex([pd.Timestamp(end)])

    frames: list[pd.DataFrame] = []

    for ticker in tickers:
        profile = STOCKS[ticker]
        seed_input = f"{ticker}:{start.isoformat()}:{end.isoformat()}".encode()
        seed = int.from_bytes(sha256(seed_input).digest()[:8], "big") % (2**32)
        rng = np.random.default_rng(seed)
        daily_returns = rng.normal(profile.drift, profile.volatility, len(business_days))

        # Add a gentle market cycle so the sample data feels realistic but repeatable.
        cycle = np.sin(np.linspace(0, 4 * np.pi, len(business_days))) * 0.0018
        prices = profile.start_price * np.cumprod(1 + daily_returns + cycle)

        volume_base = rng.integers(1_800_000, 18_000_000)
        volumes = volume_base * rng.lognormal(mean=0.0, sigma=0.24, size=len(business_days))

        frames.append(
            pd.DataFrame(
                {
                    "Date": business_days,
                    "Ticker": ticker,
                    "Company": profile.name,
                    "Sector": profile.sector,
                    "Close": prices.round(2),
                    "Volume": volumes.astype(int),
                }
            )
        )

    return pd.concat(frames, ignore_index=True)


def currency(value: float) -> str:
    return f"${value:,.0f}"


def signed_currency(value: float) -> str:
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.0f}"


def percent(value: float) -> str:
    return f"{value:+.2f}%"


def metric_card(label: str, value: str, delta: str, status: str = "neutral") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta {status}">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def make_portfolio_frame(prices: pd.DataFrame, holdings: dict[str, int]) -> pd.DataFrame:
    portfolio = prices.copy()
    portfolio["Shares"] = portfolio["Ticker"].map(holdings).fillna(0)
    portfolio["Market Value"] = portfolio["Close"] * portfolio["Shares"]

    first_values = (
        portfolio.sort_values("Date")
        .groupby("Ticker", as_index=False)
        .first()[["Ticker", "Close"]]
        .rename(columns={"Close": "Cost Basis"})
    )
    portfolio = portfolio.merge(first_values, on="Ticker", how="left")
    portfolio["Invested Value"] = portfolio["Cost Basis"] * portfolio["Shares"]
    portfolio["Unrealized P/L"] = portfolio["Market Value"] - portfolio["Invested Value"]
    return portfolio


def latest_positions(portfolio: pd.DataFrame) -> pd.DataFrame:
    latest = portfolio.sort_values("Date").groupby("Ticker", as_index=False).tail(1)
    latest["Return %"] = np.where(
        latest["Invested Value"] > 0,
        latest["Unrealized P/L"] / latest["Invested Value"] * 100,
        0,
    )
    total_market_value = latest["Market Value"].sum()
    latest["Weight %"] = np.where(
        total_market_value > 0,
        latest["Market Value"] / total_market_value * 100,
        0,
    )
    return latest.sort_values("Market Value", ascending=False)


def portfolio_timeseries(portfolio: pd.DataFrame) -> pd.DataFrame:
    series = (
        portfolio.groupby("Date", as_index=False)
        .agg({"Market Value": "sum", "Invested Value": "sum"})
        .sort_values("Date")
    )
    series["Daily Return"] = series["Market Value"].pct_change().fillna(0)
    series["Cumulative Return %"] = (
        series["Market Value"] / series["Market Value"].iloc[0] - 1
    ) * 100
    return series


def sidebar_controls() -> tuple[list[str], date, date, dict[str, int]]:
    st.sidebar.title("Portfolio controls")
    st.sidebar.caption("Tune the sample portfolio and tracking window.")

    selected = st.sidebar.multiselect(
        "Tracked stocks",
        options=list(STOCKS.keys()),
        default=["AAPL", "MSFT", "GOOGL", "NVDA", "JPM"],
    )
    if not selected:
        st.sidebar.warning("Select at least one ticker to display the dashboard.")
        selected = ["AAPL"]

    today = date.today()
    default_start = today - timedelta(days=365)
    date_range = st.sidebar.date_input(
        "Performance window",
        value=(default_start, today),
        min_value=today - timedelta(days=5 * 365),
        max_value=today,
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
    else:
        start, end = default_start, today
    if start >= end:
        st.sidebar.error("Start date must be before end date.")
        start, end = default_start, today

    st.sidebar.divider()
    st.sidebar.subheader("Holdings")
    holdings = {
        ticker: int(
            st.sidebar.number_input(
                f"{ticker} shares",
                min_value=0,
                max_value=10_000,
                value=DEFAULT_SHARES.get(ticker, 10),
                step=1,
            )
        )
        for ticker in selected
    }

    return selected, start, end, holdings


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Finance dashboard</h1>
            <p>
                Track portfolio value, monitor stock prices, and review unrealized gains
                and losses in a clean, responsive Streamlit workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(series: pd.DataFrame, positions: pd.DataFrame) -> None:
    current_value = float(series["Market Value"].iloc[-1])
    invested_value = float(series["Invested Value"].iloc[-1])
    total_gain = current_value - invested_value
    total_return = (total_gain / invested_value * 100) if invested_value else 0
    daily_change = float(series["Daily Return"].iloc[-1] * 100)
    best_position = positions.sort_values("Return %", ascending=False).iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Portfolio value", currency(current_value), f"{percent(daily_change)} today", "positive" if daily_change >= 0 else "negative")
    with col2:
        metric_card("Total gain/loss", signed_currency(total_gain), percent(total_return), "positive" if total_gain >= 0 else "negative")
    with col3:
        metric_card("Invested capital", currency(invested_value), f"{len(positions)} active positions")
    with col4:
        metric_card("Top performer", best_position["Ticker"], percent(float(best_position["Return %"])), "positive" if best_position["Return %"] >= 0 else "negative")


def render_charts(prices: pd.DataFrame, series: pd.DataFrame, positions: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">Portfolio performance</div>', unsafe_allow_html=True)
    perf_fig = go.Figure()
    perf_fig.add_trace(
        go.Scatter(
            x=series["Date"],
            y=series["Market Value"],
            mode="lines",
            name="Market value",
            fill="tozeroy",
            line=dict(color="#2563eb", width=3),
        )
    )
    perf_fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=10),
        height=380,
        yaxis_tickprefix="$",
        hovermode="x unified",
        template="plotly_white",
    )
    st.plotly_chart(perf_fig, use_container_width=True)

    left, right = st.columns((1.45, 1))
    with left:
        st.markdown('<div class="section-title">Stock price tracking</div>', unsafe_allow_html=True)
        price_fig = px.line(
            prices,
            x="Date",
            y="Close",
            color="Ticker",
            hover_data={"Company": True, "Volume": ":,"},
            template="plotly_white",
        )
        price_fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            height=390,
            yaxis_title="Close price",
            yaxis_tickprefix="$",
            hovermode="x unified",
            legend_title_text="Ticker",
        )
        st.plotly_chart(price_fig, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Allocation by position</div>', unsafe_allow_html=True)
        allocation_fig = px.pie(
            positions,
            names="Ticker",
            values="Market Value",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        allocation_fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            height=390,
            showlegend=True,
            template="plotly_white",
        )
        st.plotly_chart(allocation_fig, use_container_width=True)

    st.markdown('<div class="section-title">Gains and losses overview</div>', unsafe_allow_html=True)
    gain_fig = px.bar(
        positions.sort_values("Unrealized P/L"),
        x="Unrealized P/L",
        y="Ticker",
        orientation="h",
        color="Unrealized P/L",
        color_continuous_scale=["#dc2626", "#f8fafc", "#059669"],
        template="plotly_white",
        hover_data={"Company": True, "Return %": ":.2f", "Market Value": ":$,.0f"},
    )
    gain_fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=10),
        height=330,
        xaxis_tickprefix="$",
        coloraxis_showscale=False,
    )
    st.plotly_chart(gain_fig, use_container_width=True)


def render_tables(positions: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">Position details</div>', unsafe_allow_html=True)
    display = positions[
        [
            "Ticker",
            "Company",
            "Sector",
            "Shares",
            "Close",
            "Market Value",
            "Invested Value",
            "Unrealized P/L",
            "Return %",
            "Weight %",
        ]
    ].rename(columns={"Close": "Last Price"})

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Last Price": st.column_config.NumberColumn(format="$%.2f"),
            "Market Value": st.column_config.NumberColumn(format="$%.0f"),
            "Invested Value": st.column_config.NumberColumn(format="$%.0f"),
            "Unrealized P/L": st.column_config.NumberColumn(format="$%.0f"),
            "Return %": st.column_config.NumberColumn(format="%.2f%%"),
            "Weight %": st.column_config.NumberColumn(format="%.2f%%"),
        },
    )


def main() -> None:
    inject_styles()
    selected, start, end, holdings = sidebar_controls()

    prices = build_price_history(tuple(selected), start, end)
    portfolio = make_portfolio_frame(prices, holdings)
    positions = latest_positions(portfolio)
    series = portfolio_timeseries(portfolio)

    render_header()
    render_metrics(series, positions)
    render_charts(prices, series, positions)
    render_tables(positions)

    st.caption(
        "Sample data is generated locally for demonstration. Replace the data generator with "
        "your market data provider to connect live pricing."
    )


if __name__ == "__main__":
    main()
