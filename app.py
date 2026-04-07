import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG ---
# Set the page to wide mode for your Chromebook screen
st.set_page_config(page_title="Alpha Scout: Tactical Terminal", layout="wide")

def get_technical_signals(data):
    # RSI Calculation (14-period)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # 9-Day EMA (The Boom Floor/Exit Marker)
    ema_9 = data['Close'].ewm(span=9, adjust=False).mean()
    
    # % Cushion Metric (Distance from the 9-EMA)
    current_price = data['Close'].iloc[-1]
    current_ema = ema_9.iloc[-1]
    pct_dist = ((current_price - current_ema) / current_ema) * 100
    
    return rsi.iloc[-1], ema_9, pct_dist

# --- 2. LIVE SCOUT ---
st.title("🚀 Alpha Scout: Institutional Command Center")
st.write("**Market Intelligence:** Monday, April 6, 2026")

# Your Strategic Ticker Team
team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]

try:
    # Fetch 6 months of data for stability in technicals
    data = yf.download(team_tickers, period="6mo", group_by='ticker')
    cols = st.columns(len(team_tickers))
    
    latest_prices = {}
    for i, ticker in enumerate(team_tickers):
        ticker_df = data[ticker].dropna()
        price = ticker_df['Close'].iloc[-1]
        latest_prices[ticker] = price
        rsi, ema_series, pct_dist = get_technical_signals(ticker_df)
        
        with cols[i]:
            # Metric shows price and the % distance to the 9-EMA floor
            st.metric(ticker, f"${price:.2f}", f"{pct_dist:+.1f}% Cushion")
            
            # Status Logic
            if pct_dist < 0: 
                st.error("📉 TREND BREAK")
            elif rsi > 70: 
                st.warning("🔥 BOOMING")
            else: 
                st.success("🚀 STRONG")

    st.divider()

    # --- 3. DIRECTIONAL ANALYSIS & VOLUME ---
    st.subheader("📊 Directional Analysis: Price & Institutional Volume")
    selected_ticker = st.selectbox("Select Ticker for Deep Dive", team_tickers)
    
    if selected_ticker:
        df = data[selected_ticker].dropna()
        _, ema_9_series, _ = get_technical_signals(df)
        
        # Setup Subplots (70% Price Chart, 30% Volume Bars)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.7, 0.3])

        # A. Candlesticks (The primary direction)
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name="Price"
        ), row=1, col=1)

        # B. 9-Day EMA (The orange floor line)
        fig.add_trace(go.Scatter(
            x=df.index, y=ema_9_series, 
            line=dict(color='orange', width=2), name="9-Day EMA"
        ), row=1, col=1)

        # C. Volume Bars (Color-coded: Green for up, Red for down)
        vol_colors = ['#26a69a' if c >= o else '#ef5350' for o, c in zip(df['Open'], df['Close'])]
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'], 
            marker_color=vol_colors, name="Volume"
        ), row=2, col=1)

        # Layout & Formatting
        fig.update_layout(
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            height=700,
            showlegend=False,
            margin=dict(t=30, b=10)
        )
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        # Updated plotly_chart call to fix recent Streamlit warnings
        st.plotly_chart(fig, use_container_width=
