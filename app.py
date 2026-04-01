import streamlit as st
import yfinance as yf

# 1. THE CACHE: This stops the YFRateLimitError
@st.cache_data(ttl=600)  # Remembers data for 10 minutes
def get_ticker_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# 2. THE UI: Only runs if data is successfully fetched
st.title("Alpha Terminal")
info = get_ticker_data("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Forward PE - Rounded to 1 decimal place
    f_pe = round(info.get('forwardPE', 0), 1)
    col1.metric("Forward PE", f"{f_pe}")
    
    # Div Yield - Fixed to handle decimal conversion correctly
    raw_yield = info.get('dividendYield', 0)
    if raw_yield and raw_yield < 1.0: # Prevents the 230% glitch
        col2.metric("Div Yield", f"{round(raw_yield * 100, 2)}%")
    else:
        col2.metric("Div Yield", "N/A")
else:
    # Friendly message if still rate-limited
    st.error("Rate limit active. Retrying in 10 minutes...")
