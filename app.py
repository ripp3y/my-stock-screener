import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Alpha Scout: Tactical Terminal", layout="wide")

# Updated Target Map for the new Team
target_map = {
    "GEV": 863.61, "BW": 20.33, "PBR-A": 16.02, 
    "EQNR": 29.50, "TPL": 639.00, "SNDK": 95.00, 
    "MRNA": 115.00, "CIEN": 354.01, "TIGO": 73.20, "STX": 582.00
}

@st.cache_data(ttl=600)
def fetch_ticker_data(tickers):
    return yf.download(tickers, period="6mo", group_by='ticker')

def get_technical_signals(data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    ema_9 = data['Close'].ewm(span=9, adjust=False).mean()
    current_price = data['Close'].iloc[-1]
    current_ema = ema_9.iloc[-1]
    pct_dist = ((current_price - current_ema) / current_ema) * 100
    is_bottoming = (rsi.iloc[-1] > 30) and (rsi.iloc[-2] <= 30)
    return rsi, ema_9, pct_dist, is_bottoming

st.title("🚀 Alpha Scout: Strategic Command Center")
team_tickers = list(target_map.keys()) # All 10 stocks now tracked

try:
    data = fetch_ticker_data(team_tickers)
    cols = st.columns(len(team_tickers))
    latest_prices = {}

    for i, ticker in enumerate(team_tickers):
        ticker_df = data[ticker].dropna()
        price = ticker_df['Close'].iloc[-1]
        latest_prices[ticker] = price
        rsi_series, _, pct_dist, bottom_signal = get_technical_signals(ticker_df)
        
        with cols[i]:
            st.metric(ticker, f"${price:.2f}", f"{pct_dist:+.1f}% Floor")
            if bottom_signal: st.success("🎯 BOTTOM FOUND")
            elif pct_dist < 0: st.error("📉 TREND BREAK")
            elif rsi_series.iloc[-1] > 70: st.warning("🔥 BOOMING")
            else: st.info("🚀 STRONG")

    st.divider()

    selected_ticker = st.selectbox("Select Ticker for Deep Dive", team_tickers)
    if selected_ticker:
        df = data[selected_ticker].dropna()
        rsi_s, ema_9_s, _, _ = get_technical_signals(df)
        
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.04, row_heights=[0.5, 0.2, 0.3])

        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ema_9_s, line=dict(color='orange', width=2), name="9-EMA"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=rsi_s, line=dict(color='#A020F0', width=2), name="RSI"), row=2, col=1)

        # ADDED: Target Price Dotted Line
        t_price = target_map.get(selected_ticker)
        fig.add_hline(y=t_price, line_dash="dot", line_color="white", row=1, col=1)
        fig.add_annotation(xref="paper", yref="y", x=0.98, y=t_price, text=f"TARGET: ${t_price}", showarrow=False, font=dict(size=10, color="white"), row=1, col=1)

        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="lime", row=2, col=1)

        vol_colors = ['#26a69a' if c >= o else '#ef5350' for o, c in zip(df['Open'], df['Close'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vol_colors, name="Volume"), row=3, col=1)
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=800, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Sync Error: {e}")
