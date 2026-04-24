import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="HARDWIRE v11.8", layout="wide")

# --- [2. THE NO-LIBRARY ENGINE] ---
@st.cache_data(ttl=600)
def get_data_hardwired(ticker):
    """Bypasses yfinance entirely. Reads raw CSV data from Yahoo's backend."""
    try:
        # Create a Unix timestamp for today
        now = int(time.time())
        start = now - (30 * 24 * 60 * 60) # 30 days ago
        
        # This is a direct URL 'hardwire' to Yahoo's CSV server
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start}&period2={now}&interval=1d&events=history&includeAdjustedClose=true"
        
        # Browser simulation header
        df = pd.read_csv(url, storage_options={'User-Agent': 'Mozilla/5.0'})
        return df
    except:
        return None

# --- [3. HEADER] ---
st.title("📟 HARDWIRE TERMINAL v11.8")
st.caption("Engine: Direct CSV Injection | Status: Library-Free | Hub: Galax")

# --- [4. MONITOR] ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("NVTS")
    nvts = get_data_hardwired("NVTS")
    if nvts is not None:
        price = nvts['Close'].iloc[-1]
        st.metric("Current", f"${price:.2f}")
        st.line_chart(nvts.set_index('Date')['Close'])

with col2:
    st.subheader("BTC")
    btc = get_data_hardwired("BTC-USD")
    if btc is not None:
        price_btc = btc['Close'].iloc[-1]
        st.metric("Current", f"${price_btc:,.2f}")
        st.line_chart(btc.set_index('Date')['Close'])

# --- [5. RECON LIST] ---
st.divider()
portfolio = ["FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
recon_list = []

for t in portfolio:
    data = get_data_hardwired(t)
    if data is not None:
        recon_list.append({
            "Ticker": t, 
            "Price": f"${data['Close'].iloc[-1]:.2f}",
            "Date": data['Date'].iloc[-1]
        })

if recon_list:
    st.table(pd.DataFrame(recon_list))
