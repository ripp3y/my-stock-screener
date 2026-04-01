import streamlit as st
import yfinance as yf

# --- ENGINE: Stop the Rate Limits ---
@st.cache_data(ttl=600)  # Remembers data for 10 minutes
def get_clean_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# --- UI: Render the Metrics ---
st.title("Alpha Terminal")
info = get_clean_data("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # 1. Forward PE (Rounded for the terminal look)
    f_pe = round(info.get('forwardPE', 0), 1)
    col1.metric("Forward PE", f"{f_pe}")
    
    # 2. Div Yield (Fixed decimal logic)
    raw_yield = info.get('dividendYield', 0)
    # Most APIs return 0.03 for 3%. If it returns > 1, it's a glitch.
    if raw_yield and raw_yield < 1.0:
        formatted_yield = f"{round(raw_yield * 100, 2)}%"
    else:
        formatted_yield = "N/A"
    
    col2.metric("Div Yield", formatted_yield)
else:
    st.error("Terminal offline: Yahoo Rate Limit. Wait 5 minutes.")
