import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG ---
st.set_page_config(page_title="Alpha Scout: Command Center", layout="wide")

def get_technical_signals(data):
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Volume Spike
    avg_vol = data['Volume'].rolling(window=20).mean()
    vol_spike = data['Volume'].iloc[-1] > (avg_vol.iloc[-1] * 1.5)
    
    # Exit Marker: 9-Day EMA
    ema_9 = data['Close'].ewm(span=9, adjust=False).mean()
    
    return rsi.iloc[-1], vol_spike, ema_9

# --- 2. LIVE SCOUT ---
st.title("🚀 Alpha Scout: Interactive Command Center")
team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]

try:
    # Fetch 6mo data
    data = yf.download(team_tickers, period="6mo", group_by='ticker')
    cols = st.columns(len(team_tickers))
    
    latest_prices = {}
    for i, ticker in enumerate(team_tickers):
        ticker_df = data[ticker].dropna()
        price = ticker_df['Close'].iloc[-1]
        latest_prices[ticker] = price
        rsi, has_spike, ema_series = get_technical_signals(ticker_df)
        ema_9_val = ema_series.iloc[-1]
        
        with cols[i]:
            st.metric(ticker, f"${price:.2f}")
            if rsi > 70: st.error(f"RSI: {rsi:.1f}")
            elif rsi < 35: st.success(f"RSI: {rsi:.1f}")
            else: st.caption(f"RSI: {rsi:.1f}")
            
            # Trend Detection
            if price < ema_9_val and rsi > 60:
                st.warning("⚠️ TREND BREAK")
            else:
                st.write("Trend: Strong")

    st.divider()

    # --- 3. INTERACTIVE CHARTING ---
    st.subheader("📊 Deep Dive: Interactive Price Action")
    selected_ticker = st.selectbox("Select Ticker to View Chart", team_tickers)
    
    if selected_ticker:
        df = data[selected_ticker].dropna()
        ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
        
        fig = go.Figure()
        
        # Add Candlesticks
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name="Price"
        ))
        
        # Add 9-Day EMA (The "Boom" Floor)
        fig.add_trace(go.Scatter(
            x=df.index, y=ema_9, 
            line=dict(color='orange', width=2), 
            name="9-Day EMA"
        ))
        
        fig.update_layout(
            title=f"{selected_ticker} - Trend Analysis",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False,
            height=500,
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- 4. GOALS & STRATEGY ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💰 Harvest Calculator")
        shares = st.number_input("EQNR Shares", value=49)
        val = shares * latest_prices.get('EQNR', 0)
        st.success(f"Harvest: ${val:,.2f}")
        st.progress(min(val/2045.50, 1.0))
        
    with c2:
        st.subheader("🎯 Moonshot: 400% Club")
        st.table(pd.DataFrame({
            "Ticker": ["GEV", "BW", "SNDK", "TPL"],
            "Status": ["✅ Reached", "⏳ Near", "🚀 Running", "🎯 New Entry"]
        }))

except Exception as e:
    st.error(f"Sync Error: {e}")
