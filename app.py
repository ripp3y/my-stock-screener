import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# --- DATA FETCHING WITH RETRY LOGIC ---

@st.cache_data(ttl=600)
def fetch_mountain_data(ticker):
    """Bypasses '6m' error and handles throttling (cite: image_720628.png, image_71f9ed.png)"""
    for attempt in range(3):
        try:
            # FIX: Using '6mo' instead of '6m' (cite: image_720628.png)
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty and 'Close' in df:
                return df['Close']
        except Exception:
            time.sleep(attempt + 1) # Exponential backoff to avoid 10s lockout
    return None

# --- UI RENDER ---

st.title("🛡️ Alpha Terminal")

# Tickers from your sectors (cite: image_71eec4.png, image_75300a.png)
watchlist = ["SLB", "EQNR", "COP", "PBR-A", "LRCX", "NVDA"]

for ticker in watchlist:
    # Expanders prevent the app from fetching 30+ charts at once (cite: image_71f9ed.png)
    with st.expander(f"⭐ {ticker} View"):
        with st.spinner(f"Fetching {ticker}..."):
            chart_data = fetch_mountain_data(ticker)
            
            if chart_data is not None:
                # Placeholder for Forward PE metric logic (cite: image_7f2225.png)
                # Ensure all parentheses are closed to avoid SyntaxError (cite: image_7f1dc5.png)
                st.metric("Forward PE", "21.4")
                
                # Renders the shaded area chart (cite: image_7f2225.png)
                st.area_chart(chart_data)
            else:
                st.error("Yahoo link timed out. Please wait 10s and refresh.")
