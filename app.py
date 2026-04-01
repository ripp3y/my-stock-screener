import streamlit as st
import yfinance as yf

# 1. THE CACHE: This stops the YFRateLimitError loop
@st.cache_data(ttl=600)  # Remembers data for 10 minutes
def fetch_ticker_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Accessing .info triggers the API call
        return ticker.info
    except Exception:
        return None

# 2. THE UI RENDER
st.title("Alpha Terminal")
info = fetch_ticker_info("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Render Rounded Forward PE
    f_pe = round(info.get('forwardPE', 0), 1)
    col1.metric("Forward PE", f"{f_pe}")
    
    # Render Fixed Div Yield
    raw_yield = info.get('dividendYield', 0)
    # Sanity check: Real yields are decimals (e.g., 0.03 = 3%)
    if raw_yield and raw_yield < 1.0: 
        col2.metric("Div Yield", f"{round(raw_yield * 100, 2)}%")
    else:
        col2.metric("Div Yield", "N/A")
else:
    # Shown only if you are currently blocked by Yahoo
    st.warning("Rate limit active. Data will restore automatically in ~10 min.")
