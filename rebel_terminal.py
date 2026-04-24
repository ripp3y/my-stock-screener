import os
import subprocess
import sys

# --- [0. THE SELF-INSTALLER] ---
# This forces the server to install scipy if it's missing
try:
    import scipy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy"])

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v11.5", layout="wide")

# --- [2. ENGINE] ---
@st.cache_data(ttl=600)
def get_data(ticker):
    try:
        # Standard fetch with repairs turned OFF to be safe
        df = yf.download(ticker, period="6mo", interval="1d", repair=False, progress=False)
        if df is not None and not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        return None
    except:
        return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v11.5")
st.caption("Engine: v11.5 Auto-Fix | Hub: Galax")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. MAIN INTERFACE] ---
tab1, tab2 = st.tabs(["📊 RECON", "₿ CRYPTO"])

with tab1:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    recon_list = []
    for t in portfolio:
        data = get_data(t)
        if data is not None:
            curr_p = float(data['Close'].iloc[-1])
            recon_list.append({"Ticker": t, "Price": f"${curr_p:.2f}", "Signal": "🟢"})
    
    if recon_list:
        st.table(pd.DataFrame(recon_list))
        nvts_data = get_data("NVTS")
        if nvts_data is not None:
            st.line_chart(nvts_data['Close'].tail(60))

with tab2:
    for c in ["BTC-USD", "MARA"]:
        data = get_data(c)
        if data is not None:
            st.metric(c, f"${float(data['Close'].iloc[-1]):,.2f}")
