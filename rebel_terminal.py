import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Strategic Terminal", layout="wide")
st.markdown("<p style='font-size: 11px; color: gray;'>Powered by Gemini</p>", unsafe_allow_html=True)

# --- CORE DATA ENGINE ---
tickers = ["NVTS", "CIEN", "SNDK", "STX", "MRVL", "NXPI"]

@st.cache_data(ttl=3600)  # Hourly refresh as requested
def get_market_data(symbol_list):
    data = yf.download(symbol_list, period="1y", interval="1d")['Close']
    return data

def get_live_metrics(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="5d", interval="1h")
    current_price = hist['Close'].iloc[-1]
    ath = ticker.history(period="max")['High'].max()
    avg_vol = ticker.history(period="20d")['Volume'].mean()
    current_vol = hist['Volume'].iloc[-1]
    return current_price, ath, avg_vol, current_vol

# --- UI LAYOUT ---
tab1, tab2 = st.tabs(["📊 Strategic US Terminal", "🔍 Breakout Screener"])

# --- TAB 1: CORE MONITOR ---
with tab1:
    st.header("Core Infrastructure Monitor")
    core_data = get_market_data(["NVTS", "CIEN", "SNDK"])
    # Normalized "Bridge" View
    normalized = core_data / core_data.iloc[0]
    st.line_chart(normalized, height=400)
    
    st.info("Tracking the 'Metabolic Health' of the AI Backbone.")

# --- TAB 2: BREAKOUT SCREENER ---
with tab2:
    st.header("Skyline & High-Alpha Screener")
    col1, col2 = st.columns([2, 1])
    
    screener_results = []
    
    for s in tickers:
        price, ath, avg_vol, cur_vol = get_live_metrics(s)
        vol_ratio = cur_vol / avg_vol
        is_ath = price >= (ath * 0.99) # Within 1% of ATH
        
        # --- THE SILENT ALERT LOGIC ---
        if is_ath and vol_ratio > 1.5:
            st.toast(f"🚨 SKYLINE ALERT: {s} is testing All-Time Highs on 1.5x Volume!", icon="🚀")
        
        screener_results.append({
            "Ticker": s,
            "Price": round(price, 2),
            "ATH": round(ath, 2),
            "Vol Ratio": f"{round(vol_ratio, 2)}x",
            "Status": "🔥 BREAKOUT" if is_ath else "Consolidating"
        })

    df = pd.DataFrame(screener_results)
    st.table(df)

# --- SIDEBAR LOGS ---
with st.sidebar:
    st.subheader("Architect Logs")
    st.write(f"Last Update: {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.write("Filters: Hourly Refresh, ATH Tracker, US-Only Markets.")
