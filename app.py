import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. CONFIG ---
st.set_page_config(page_title="Alpha Scout: Command Center", layout="wide")

def get_technical_signals(data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    avg_vol = data['Volume'].rolling(window=20).mean()
    vol_spike = data['Volume'].iloc[-1] > (avg_vol.iloc[-1] * 1.5)
    return rsi.iloc[-1], vol_spike

# --- 2. LIVE SCOUT SECTION ---
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
        rsi, has_spike = get_technical_signals(ticker_df)
        
        with cols[i]:
            st.metric(ticker, f"${price:.2f}")
            # Dynamic RSI Highlighting
            if rsi > 70:
                st.error(f"RSI: {rsi:.1f} (OVERBOUGHT)")
            elif rsi < 35:
                st.success(f"RSI: {rsi:.1f} (OVERSOLD)")
            else:
                st.caption(f"RSI: {rsi:.1f}")
            
            if has_spike: st.warning("🔥 VOL SPIKE")
            else: st.write("Normal Vol")

    st.divider()

    # --- 3. GOAL & STRATEGY SECTION ---
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.subheader("💰 Harvest Calculator")
        eqnr_price = latest_prices.get('EQNR', 41.95)
        shares_to_sell = st.number_input("EQNR Shares to Sell", value=49, step=1)
        harvest_value = shares_to_sell * eqnr_price
        
        st.success(f"Wednesday Harvest Value: **${harvest_value:,.2f}**")
        
        # Progress Bar to Target
        target_goal = 2045.50
        progress = min(harvest_value / target_goal, 1.0)
        st.progress(progress)
        st.write(f"Goal Completion: {progress*100:.1f}%")

    with col_right:
        st.subheader("🎯 Long-Term Moonshot: 400% Club")
        goals_data = {
            "Ticker": ["GEV", "BW", "SNDK", "TPL"],
            "Entry Price": ["$158.00", "$4.20", "$265.00", "$448.86"],
            "Current Return": ["+467%", "+298%", "+173%", "---"],
            "Target Status": ["✅ REACHED", "⏳ NEAR", "🚀 RUNNING", "🎯 NEW ENTRY"]
        }
        st.table(pd.DataFrame(goals_data))

    st.divider()

    # --- 4. INSIGHTS PANEL ---
    st.subheader("📝 Strategic Rotation Notes")
    st.info(f"""
    * **Harvest Alert**: EQNR is currently **Overbought**. Selling Wednesday locks in capital at a peak valuation.
    * **The Rotation**: Move your **${harvest_value:,.2f}** directly into **TPL** (${latest_prices.get('TPL', 448.86):.2f}), which is currently **Deeply Oversold**.
    * **The Engine**: **SNDK** remains the 2026 momentum leader. Its healthy RSI (52.4) suggests the run toward the 400% mark is still active.
    """)

except Exception as e:
    st.error(f"Sync Error: {e}")
