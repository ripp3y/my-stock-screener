import streamlit as st
import yfinance as yf

# --- DATA ENGINE (Stops the YFRateLimitError) ---
@st.cache_data(ttl=600) # Cache for 10 minutes
def get_ticker_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# --- UI RENDER ---
st.title("Alpha Terminal")
info = get_ticker_info("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Rounded PE
    f_pe = round(info.get('forwardPE', 0), 1)
    col1.metric("Forward PE", f"{f_pe}")
    
    # Fixed Div Yield Logic
    raw_yield = info.get('dividendYield', 0)
    # Sanity check: Yields > 100% are usually API errors
    if raw_yield and raw_yield < 1.0: 
        formatted_yield = f"{round(raw_yield * 100, 2)}%"
    else:
        formatted_yield = "N/A"
    
    col2.metric("Div Yield", formatted_yield)
else:
    st.warning("Yahoo Rate Limit active. Cooling down...")
