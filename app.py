import streamlit as st
import pandas as pd
import yfinance as yf

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
    
    return rsi.iloc[-1], vol_spike, ema_9.iloc[-1]

# --- 2. LIVE SCOUT ---
st.title("🚀 Alpha Scout: Strategic Command Center")
st.write(f"**Monday Night Intelligence:** April 6, 2026")

team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]

try:
    data = yf.download(team_tickers, period="6mo", group_by='ticker')
    cols = st.columns(len(team_tickers))
    
    latest_prices = {}
    for i, ticker in enumerate(team_tickers):
        ticker_df = data[ticker].dropna()
        price = ticker_df['Close'].iloc[-1]
        latest_prices[ticker] = price
        rsi, has_spike, ema_9 = get_technical_signals(ticker_df)
        
        with cols[i]:
            st.metric(ticker, f"${price:.2f}")
            if rsi > 70: st.error(f"RSI: {rsi:.1f}")
            elif rsi < 35: st.success(f"RSI: {rsi:.1f}")
            else: st.caption(f"RSI: {rsi:.1f}")
            
            # The Exit Marker Logic
            if price < ema_9 and rsi > 60:
                st.warning("⚠️ TREND BREAK")
                st.write(f"Below 9-EMA (${ema_9:.2f})")
            elif has_spike:
                st.info("🔥 VOL SPIKE")
            else:
                st.write("Trend: Strong")

    st.divider()

    # --- 3. GOALS & EXIT MARKERS ---
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.subheader("💰 Harvest Calculator")
        eqnr_price = latest_prices.get('EQNR', 41.95)
        shares_to_sell = st.number_input("EQNR Shares to Sell", value=49, step=1)
        harvest_value = shares_to_sell * eqnr_price
        st.success(f"Wednesday Harvest: **${harvest_value:,.2f}**")
        st.progress(min(harvest_value / 2045.50, 1.0))

    with col_right:
        st.subheader("🛡️ The Trend Guard: Exit Markers")
        st.markdown("""
        | Market Signal | Investor Action |
        | :--- | :--- |
        | **Close < 9-EMA** | **Exit Marker Triggered** - The 'boom' is cooling. |
        | **RSI Divergence** | **Tighten Stops** - Momentum is slowing down. |
        | **Volume Dry-up** | **Wait & Watch** - Retail is exhausted. |
        """)

    st.divider()
    st.subheader("🎯 Long-Term Moonshot: 400% Club")
    goals_df = pd.DataFrame({
        "Ticker": ["GEV", "BW", "SNDK", "TPL"],
        "Target Status": ["✅ REACHED", "⏳ NEAR", "🚀 RUNNING", "🎯 NEW ENTRY"],
        "Strategy": ["Hold for Divs", "Ride the Backlog", "AI Scarcity Play", "Buy the Oversold Dip"]
    })
    st.table(goals_df)

except Exception as e:
    st.error(f"Terminal Sync Error: {e}")
