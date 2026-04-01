import streamlit as st
import yfinance as yf

# --- CACHE ENGINE: Prevents YFRateLimitError (cite: image_c59acc.png) ---
@st.cache_data(ttl=1800)
def get_alpha_terminal_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# --- UI RENDER ---
st.title("Alpha Terminal")
info = get_alpha_terminal_data("SLB")

if info:
    col1, col2, col3 = st.columns(3)
    
    # Metric 1: Forward PE (Rounded)
    f_pe = info.get('forwardPE')
    col1.metric("Forward PE", f"{round(f_pe, 1)}" if f_pe else "N/A")
    
    # Metric 2: Beta (Market Risk)
    beta = info.get('beta')
    col2.metric("Beta", f"{round(beta, 2)}" if beta else "N/A")
    
    # Metric 3: Alpha (Simplified Performance vs 50D Average)
    price = info.get('currentPrice')
    ma50 = info.get('fiftyDayAverage')
    if price and ma50:
        # Calculate % difference from 50-day average
        alpha_val = round(((price - ma50) / ma50) * 100, 1)
        col3.metric("Alpha (50D)", f"{alpha_val}%", delta=f"{alpha_val}%")
    else:
        col3.metric("Alpha (50D)", "N/A")
else:
    st.error("Connection Cooling. Data will restore shortly.")
