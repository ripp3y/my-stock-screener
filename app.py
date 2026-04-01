import streamlit as st
import yfinance as yf

# --- CACHE ENGINE: Essential for preventing API lockouts ---
@st.cache_data(ttl=1800)
def get_alpha_terminal_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Fetching .info triggers the actual network request
        return ticker.info
    except Exception:
        return None

# --- UI LAYOUT ---
st.title("Alpha Terminal")
info = get_alpha_terminal_data("SLB")

if info:
    col1, col2, col3 = st.columns(3)
    
    # 1. Forward PE: Rounded to 1 decimal place
    f_pe = info.get('forwardPE')
    col1.metric("Forward PE", f"{round(f_pe, 1)}" if f_pe else "N/A")
    
    # 2. Beta: Market Sensitivity
    beta = info.get('beta')
    col2.metric("Beta", f"{round(beta, 2)}" if beta else "N/A")
    
    # 3. Alpha (50D): Trend Performance
    price = info.get('currentPrice')
    ma50 = info.get('fiftyDayAverage')
    if price and ma50:
        alpha_val = round(((price - ma50) / ma50) * 100, 1)
        col3.metric("Alpha (50D)", f"{alpha_val}%", delta=f"{alpha_val}%")
    else:
        col3.metric("Alpha (50D)", "N/A")
else:
    # Safe error handling if the rate limit is hit
    st.warning("Data sync cooling down. Metrics will restore automatically.")
