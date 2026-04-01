import streamlit as st
import yfinance as yf

# 1. THE CACHE: Mandatory to stop the lockout loop
@st.cache_data(ttl=1200) # Remembers data for 20 minutes
def get_alpha_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# 2. UI RENDER
st.title("Alpha Terminal")
info = get_alpha_data("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Metric 1: Forward PE (Rounded)
    f_pe = info.get('forwardPE')
    col1.metric("Forward PE", f"{round(f_pe, 1)}" if f_pe else "N/A")
    
    # Metric 2: Beta (Volatility vs Market)
    # Beta > 1.0 means it's more volatile than the S&P 500
    beta = info.get('beta')
    col2.metric("Beta", f"{round(beta, 2)}" if beta else "N/A")
else:
    # Shown only if Yahoo is actively blocking your IP
    st.error("Terminal cooling down. Data will restore in ~15 minutes.")
