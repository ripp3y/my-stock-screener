import streamlit as st
import yfinance as yf

# 1. THE CACHE: This remembers data for 30 minutes to stop the lockout
@st.cache_data(ttl=1800) 
def get_clean_ticker_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Accessing info triggers the network request
        data = ticker.info
        return data if data else None
    except Exception:
        return None

# 2. THE UI ENGINE
st.title("Alpha Terminal")
info = get_clean_ticker_info("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Forward PE (Rounded for terminal look)
    f_pe = info.get('forwardPE')
    col1.metric("Forward PE", f"{round(f_pe, 1)}" if f_pe else "N/A")
    
    # Div Yield (Fixed logic to prevent 230.0% glitch)
    raw_yield = info.get('dividendYield')
    if raw_yield and 0 < raw_yield < 1.0:
        col2.metric("Div Yield", f"{round(raw_yield * 100, 2)}%")
    else:
        col2.metric("Div Yield", "N/A")
else:
    # Error state while Yahoo is actively blocking you
    st.error("Rate limit active. Terminal data will restore in ~20 minutes.")
