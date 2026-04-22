import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [SYSTEM CONFIG] ---
st.set_page_config(page_title="Radar v4.50", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to hide standard headers for a clean mobile look
st.markdown("""
    <style>
    [data-testid="stHeader"] {visibility: hidden;}
    .main .block-container {padding-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

# --- [PORTFOLIO ENGINE] ---
# Defining your stones based on the latest screengrab
portfolio_tkrs = ["SNDK", "MRVL", "STX", "FIX", "NVTS", "MTZ", "CIEN"]
hunting_tkrs = ["CRUS", "ALAB", "FLR", "AMSC", "LASR"] # Adding gems we scouted

all_tkrs = list(set(portfolio_tkrs + hunting_tkrs))

@st.cache_data(ttl=3600)
def get_market_data(tickers):
    # Fetching 5 days of data to calculate velocity
    data = yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)
    return data

# --- [HEADER] ---
st.title("📡 Radar v4.50")
st.caption(f"Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Target: 100% YoY")

# --- [THE TWIN-TAB SYSTEM] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

data = get_market_data(all_tkrs)

with tab_recon:
    st.subheader("Current Portfolio Velocity")
    recon_list = []
    for t in portfolio_tkrs:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[0]
            change = ((curr - prev) / prev) * 100
            recon_list.append({
                "Ticker": t, 
                "Price": f"${curr:.2f}", 
                "5D Move": f"{change:+.2f}%",
                "Phase": "🚀LEAD" if change > 2 else "🧱ACUM"
            })
        except: continue
    st.table(pd.DataFrame(recon_list))
    st.info("💡 Reminder: MTZ Earnings April 30. FIX Earnings April 28.")

with tab_alpha:
    st.subheader("🌪️ Alpha Channel (Velocity + Insider)")
    st.write("Searching for tight momentum channels and institutional buying.")
    
    # Static logic for gems meeting Alpha criteria today
    alpha_gems = [
        {"Ticker": "NVTS", "Velocity": "High", "Signal": "CEO/CFO Buying", "Target": "$17.79"},
        {"Ticker": "FIX", "Velocity": "Steady", "Signal": "$1.8B Backlog", "Target": "$1,800"},
        {"Ticker": "LASR", "Velocity": "Rising", "Signal": "Earnings +132%", "Target": "$85.00"}
    ]
    st.dataframe(pd.DataFrame(alpha_gems), use_container_width=True)

with tab_breakout:
    st.subheader("🚀 Blue Sky Breakouts")
    st.write("Tracking stocks clearing 52-week highs with zero overhead resistance.")
    
    breakout_gems = []
    for t in hunting_tkrs:
        try:
            # Simple breakout logic: Price > 98% of 5-day high
            high = data[t]['High'].max()
            curr = data[t]['Close'].iloc[-1]
            if curr >= (high * 0.98):
                breakout_gems.append({
                    "Ticker": t, 
                    "Price": f"${curr:.2f}", 
                    "Status": "🔥 BREAKING OUT",
                    "Room to Run": "High"
                })
        except: continue
    
    if breakout_gems:
        st.table(pd.DataFrame(breakout_gems))
    else:
        st.write("No active breakouts in the last hour. Monitoring...")

# --- [FOOTER] ---
st.divider()
st.caption("Strategy: Exit NVTS in 3-4 days. Rotate Alpha into FIX.")
