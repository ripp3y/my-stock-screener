import streamlit as st
import yfinance as yf

# 1. THE CACHE: This is mandatory to stop the YFRateLimitError
@st.cache_data(ttl=600)  # Remembers data for 10 minutes
def get_ticker_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# 2. THE UI RENDER
st.title("Alpha Terminal")
info = get_ticker_data("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Render Rounded Forward PE (cite: image_7f8e49.png)
    f_pe = round(info.get('forwardPE', 0), 1)
    col1.metric("Forward PE", f"{f_pe}")
    
    # Render Fixed Div Yield
    raw_yield = info.get('dividendYield', 0)
    # Check if yield is valid and under 100% (cite: image_bba5e4.png)
    if raw_yield and raw_yield < 1.0:
        col2.metric("Div Yield", f"{round(raw_yield * 100, 2)}%")
    else:
        col2.metric("Div Yield", "N/A")
else:
    # Error state if Yahoo is still blocking you (cite: image_c596d2.png)
    st.error("Rate limit active. Terminal cooling down for 10 minutes.")
