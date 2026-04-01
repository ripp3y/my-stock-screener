import streamlit as st
import yfinance as yf

# --- CACHE ENGINE: Prevents Yahoo Finance lockouts ---
@st.cache_data(ttl=1800)
def get_terminal_metrics(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# --- UI DISPLAY ---
st.title("Alpha Terminal")
info = get_terminal_metrics("SLB")

if info:
    col1, col2, col3 = st.columns(3)
    
    # Forward PE (cite: image_7f8e49)
    f_pe = info.get('forwardPE')
    col1.metric("Forward PE", f"{round(f_pe, 1)}" if f_pe else "N/A")
    
    # Beta: Market Sensitivity
    beta = info.get('beta')
    col2.metric("Beta", f"{round(beta, 2)}" if beta else "N/A")
    
    # Alpha (50D): Performance vs. Moving Average
    price = info.get('currentPrice')
    ma50 = info.get('fiftyDayAverage')
    if price and ma50:
        alpha_val = round(((price - ma50) / ma50) * 100, 1)
        col3.metric("Alpha (50D)", f"{alpha_val}%", delta=f"{alpha_val}%")
    else:
        col3.metric("Alpha (50D)", "N/A")
else:
    # Safe fallback if rate limited
    st.warning("Syncing data... metrics will update shortly.")
