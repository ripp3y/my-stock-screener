import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# --- MOBILE-READY CONFIG ---
st.set_page_config(
    page_title="Strategic Mobile", 
    layout="centered", # Better for mobile scrolling
    initial_sidebar_state="collapsed" # Hides sidebar on phone by default
)

# Powered by Gemini Header
st.markdown("<p style='font-size: 10px; color: gray; text-align: center;'>Powered by Gemini</p>", unsafe_allow_html=True)

# --- FLUID DATA ENGINE ---
tickers = ["NVTS", "SNDK", "STX", "NXPI", "MRVL"]

@st.cache_data(ttl=3600)
def get_mobile_data(symbol_list):
    # Fetching data with ffill() to ensure CIEN/NVTS show even during low volume
    data = yf.download(symbol_list, period="5d", interval="1h")['Close']
    return data.ffill() 

def get_live_metrics(symbol):
    t = yf.Ticker(symbol)
    h = t.history(period="2d", interval="15m")
    if h.empty: return 0, 0, 0
    curr = h['Close'].iloc[-1]
    prev = h['Close'].iloc[-2]
    delta = curr - prev
    ath = t.history(period="max")['High'].max()
    return curr, delta, ath

# --- MOBILE NAVIGATION ---
# Use Tabs for easy thumb-switching on phones
tab1, tab2 = st.tabs(["📊 Portfolio", "🚀 Alerts"])

# --- TAB 1: CORE MOBILE BRIDGE ---
with tab1:
    st.subheader("Infrastructure Health")
    data = get_mobile_data(tickers)
    
    # Normalized chart for quick comparison
    norm_data = data / data.iloc[0]
    st.line_chart(norm_data, height=250)

    # Metric Cards: Optimized for mobile vertical stacking
    for s in ["NVTS", "SNDK", "NXPI"]:
        price, delta, ath = get_live_metrics(s)
        st.metric(label=f"{s} (ATH: ${round(ath, 2)})", 
                  value=f"${round(price, 2)}", 
                  delta=f"{round(delta, 2)}")
        st.divider()

# --- TAB 2: SKYLINE ALERTS ---
with tab2:
    st.subheader("Breakout Screener")
    st.info("Scanning hourly for High Alpha / ATH")
    
    for s in tickers:
        price, delta, ath = get_live_metrics(s)
        # Visual Breakout Alert
        if price >= (ath * 0.98): # Within 2% of ATH
            st.success(f"🔥 {s} SKYLINE ALERT: Testing ATH at ${round(price, 2)}")
            st.toast(f"Mobile Alert: {s} Breakout!", icon="🚀")

# --- REFRESH BUTTON (EASY FOR THUMBS) ---
if st.button("🔄 Refresh Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
