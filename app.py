import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Standardized watchlist for Energy and Tech sectors
watchlists = {
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"]
}

@st.cache_data(ttl=300)
def fetch_stabilized_data(ticker, period="6mo"):
    """Fetch data with a retry loop to handle JSONDecodeErrors (cite: image_7521d8.png)"""
    for attempt in range(3):
        try:
            # Fix: Using '6mo' instead of '6m' (cite: image_720628.png)
            df = yf.download(ticker, period=period, progress=False)
            if not df.empty:
                return df['Close']
        except Exception:
            # Wait briefly before retrying to let the connection reset
            time.sleep(1)
    return None

def render_alpha_terminal(sector):
    st.subheader(f"Ranked: {sector}")
    tickers = watchlists.get(sector, [])
    
    for ticker in tickers:
        # Load charts inside expanders to prevent mass-request throttling (cite: image_71f9ed.png)
        with st.expander(f"⭐ {ticker}"):
            chart_data = fetch_stabilized_data(ticker)
            if chart_data is not None:
                # Area chart provides the 'Mountain' look seen in successful views (cite: image_753403.png)
                st.area_chart(chart_data)
            else:
                st.error("Data temporarily unavailable from Yahoo. Try again in a moment.")
