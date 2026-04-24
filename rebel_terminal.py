import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="RAW TERMINAL v11.7", layout="wide")

# --- [2. THE BARE-METAL ENGINE] ---
@st.cache_data(ttl=600)
def get_raw_numbers(ticker):
    """The most basic data fetch possible. No repairs. No scipy."""
    try:
        t_obj = yf.Ticker(ticker)
        # .history is the 'legacy' way - it bypasses the modern 'scipy' repair logic
        df = t_obj.history(period="1mo", interval="1d")
        if not df.empty:
            return df
        return None
    except:
        return None

# --- [3. HEADER] ---
st.title("📟 RAW TERMINAL v11.7")
st.caption("Engine: Bare Metal | Status: Total Bypass | Hub: Galax")

# --- [4. THE MONITOR] ---
# Just the essentials: NVTS and BTC
col1, col2 = st.columns(2)

with col1:
    st.subheader("NVTS")
    data_nvts = get_raw_numbers("NVTS")
    if data_nvts is not None:
        price = float(data_nvts['Close'].iloc[-1])
        st.metric("Price", f"${price:.2f}")
        st.line_chart(data_nvts['Close'])

with col2:
    st.subheader("BTC")
    data_btc = get_raw_numbers("BTC-USD")
    if data_btc is not None:
        price_btc = float(data_btc['Close'].iloc[-1])
        st.metric("Price", f"${price_btc:,.2f}")
        st.line_chart(data_btc['Close'])

# --- [5. SIMPLE RECON LIST] ---
st.divider()
portfolio = ["FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
recon_list = []

for t in portfolio:
    data = get_raw_numbers(t)
    if data is not None:
        recon_list.append({
            "Ticker": t, 
            "Price": f"${float(data['Close'].iloc[-1]):.2f}",
            "Vol": f"{int(data['Volume'].iloc[-1]):,}"
        })

if recon_list:
    st.table(pd.DataFrame(recon_list))

