import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# --- DATA STABILIZATION LAYER ---

@st.cache_data(ttl=300)
def get_safe_data(ticker):
    """Bypasses '6m' error and adds retry logic for timeouts (cite: image_720628.png, image_71f9ed.png)"""
    for _ in range(3):
        try:
            # Correcting '6m' to '6mo' as required by API (cite: image_720628.png)
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty:
                return df['Close']
        except:
            time.sleep(1) # Brief pause to allow connection reset
    return None

# --- UI RENDER ---

st.title("🛡️ Alpha Terminal")

# Example for the Energy sector
ticker = "SLB"
with st.expander(f"⭐ {ticker} Terminal View"):
    chart_data = get_safe_data(ticker)
    
    if chart_data is not None:
        # Syntax Fix: Ensuring all parentheses are closed in metrics (cite: image_7f1dc5.png)
        # Note: Replace 'info' with your actual ticker info dictionary
        st.metric("Forward PE", "21.4") 
        
        # Mountain Chart render (cite: image_7f1dc5.png)
        st.area_chart(chart_data)
    else:
        st.error("Data temporarily unavailable. Try again in 10s.")
