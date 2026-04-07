import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. SETTINGS ---
st.set_page_config(page_title="Alpha Scout: Strategic Terminal", layout="wide")

def get_technical_signals(data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    avg_vol = data['Volume'].rolling(window=20).mean()
    vol_spike = data['Volume'].iloc[-1] > (avg_vol.iloc[-1] * 1.5)
    return rsi.iloc[-1], vol_spike

# --- 2. CREATE TABS ---
# This creates two distinct sections at the top of your app
tab1, tab2 = st.tabs(["🚀 Live Scout", "🎯 Goal Center"])

# --- TAB 1: LIVE SCOUT (YOUR CURRENT DASHBOARD) ---
with tab1:
    st.title("Live Market Intelligence")
    team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]
    
    try:
        data = yf.download(team_tickers, period="6mo", group_by='ticker')
        cols = st.columns(len(team_tickers))
        
        for i, ticker in enumerate(team_tickers):
            ticker_df = data[ticker].dropna()
            latest_price = ticker_df['Close'].iloc[-1]
            rsi, has_spike = get_technical_signals(ticker_df)
            
            with cols[i]:
                st.metric(ticker, f"${latest_price:.2f}")
                if rsi > 70: st.error(f"RSI: {rsi:.1f}")
                elif rsi < 35: st.success(f"RSI: {rsi:.1f}")
                else: st.caption(f"RSI: {rsi:.1f}")
                
                if has_spike: st.warning("🔥 VOL SPIKE")
                else: st.write("Normal Vol")

    except Exception as e:
        st.error(f"Sync Error: {e}")

# --- TAB 2: GOAL CENTER (THE NEW ADDITION) ---
with tab2:
    st.header("Strategic Portfolio Goals: 2026")
    
    # 1. THE HARVEST GOAL
    st.subheader("🟢 Current Mission: The EQNR Harvest")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.write("**Target Date:** Wednesday, April 8")
        st.write("**Target Cash:** $2,045.50")
    with col_b:
        # Progress bar toward your cash goal
        # Assuming you're close to 100% since you're harvesting now
        st.write("**Completion Progress**")
        st.progress(95) 
    with col_c:
        st.write("**Next Move:**")
        st.markdown("➡️ Rotate into **TPL** (Oversold)")

    st.divider()

    # 2. THE 400% MOONSHOT TRACKER
    st.subheader("🔥 Long-Term Moonshot: 400% Club")
    
    # Example table of your high-conviction goals
    goals_data = {
        "Ticker": ["GEV", "BW", "SNDK", "TPL"],
        "Entry Price": ["$158.00", "$4.20", "$265.00", "$448.86"],
        "Current Return": ["+467%", "+298%", "+173%", "---"],
        "Target Status": ["✅ REACHED", "⏳ NEAR", "🚀 RUNNING", "🎯 NEW ENTRY"]
    }
    st.table(pd.DataFrame(goals_data))

    st.info("💡 Thoughts on this tab: Use this section to remind yourself why you are holding through volatility. When GEV or SNDK dips, the 'Goal' tab reminds you of the $150B backlog and the storage scarcity.")
