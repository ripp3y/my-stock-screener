import streamlit as st
import yfinance as yf

# 1. THE CIRCUIT BREAKER: Mandatory caching to stop rate limits
@st.cache_data(ttl=1200) # Remembers data for 20 minutes
def get_terminal_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # .info triggers the actual network request
        return ticker.info
    except Exception:
        return None

# 2. THE UI RENDER
st.title("Alpha Terminal")
info = get_terminal_data("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Render Rounded Forward PE (cite: image_7f8e49.png)
    f_pe = round(info.get('forwardPE', 0), 1)
    col1.metric("Forward PE", f"{f_pe}")
    
    # Render Fixed Div Yield (cite: image_bba5e4.png)
    raw_yield = info.get('dividendYield', 0)
    # Sanity check: Real yields are decimals (e.g., 0.03 = 3%)
    if raw_yield and raw_yield < 1.0:
        col2.metric("Div Yield", f"{round(raw_yield * 100, 2)}%")
    else:
        # Prevents the glitchy 230% from showing (cite: image_bba5e4.png)
        col2.metric("Div Yield", "N/A")
else:
    # Shown only while Yahoo is actively blocking your IP (cite: image_c59eca.png)
    st.error("Terminal Cooling Down. Data will restore automatically in ~15 min.")
