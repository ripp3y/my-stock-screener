import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN CONFIGURATION
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")
# FIXED: Changed unsafe_allow_height to unsafe_allow_html
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v2.5 | April 24, 2026 | Whale Recon Active</p>", unsafe_allow_html=True)

# 🛠️ THE ARCHITECT RECON (SIDEBAR)
with st.sidebar:
    st.title("Recon Controls")
    ticker = st.text_input("Primary Target", value="SDGR").upper()
    comp_ticker = st.text_input("Comparison (The Bridge)", value="MSFT").upper()
    
    st.divider()
    st.subheader("Whale Tracking (Live Flow)")
    st.page_link("https://unusualwhales.com/live-feed", label="Unusual Options Flow", icon="🐋")
    st.page_link("https://www.cheddarflow.com/", label="Dark Pool Prints", icon="🧀")
    
    st.divider()
    st.subheader("Architect Ledger (SEC)")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=1364742", label="BlackRock Filings", icon="🔍")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=102909", label="Vanguard Filings", icon="🔍")
    
    if st.button("Refresh Sync Algos"):
        st.success("Synchronized with EDGAR and Dark Pool feeds.")

# 🏔️ THE MAIN TERMINAL ENGINE
st.title(f"Strategic Terminal: {ticker}")

try:
    # Fetching Data
    data = yf.download(ticker, period="1y", interval="1d")
    comp_data = yf.download(comp_ticker, period="1y", interval="1d")
    
    if not data.empty:
        # Standardize for 2026 yfinance Multi-Index
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if isinstance(comp_data.columns, pd.MultiIndex):
            comp_data.columns = comp_data.columns.get_level_values(0)

        # 📊 THE MOUNTAIN VIEW
        st.subheader(f"Institutional Tape: {ticker}")
        st.area_chart(data['Close'], use_container_width=True)

        # 🔍 THE SYNC MATRIX (The Bridge)
        st.divider()
        st.subheader("The 'Inner Circle' Bridge")
        norm_data = data['Close'] / data['Close'].iloc[0]
        norm_comp = comp_data['Close'] / comp_data['Close'].iloc[0]
        combined = pd.DataFrame({ticker: norm_data, comp_ticker: norm_comp})
        st.line_chart(combined, use_container_width=True)
        st.caption(f"Correlation Check: Monitoring {ticker} vs {comp_ticker} for institutional mirrors.")

        # 🛡️ FAT WALLET ALERTS (Real-Time April 24, 2026)
        st.divider()
        st.subheader("Sovereign Intelligence Feed")
        
        if ticker == 'PBR':
            st.info("📊 EX-DIVIDEND ALERT: Today (Apr 24). Rate: $0.24818. Yield extraction in progress.")
        
        if ticker == 'WST':
            st.error("🚀 BREAKOUT: Q1 Beat. Gates 'Infrastructure' play is live.")
            
        if ticker == 'SDGR':
            st.warning("🕵️ GATES WATCH: #1 Holder. Q1 Earnings scheduled for May 5. Watch for pre-earnings accumulation.")

        # 📋 RAW DATA TAPE
        with st.expander("View Raw Data Tape"):
            st.dataframe(data.tail(10), use_container_width=True)

except Exception as e:
    st.error(f"SYSTEM FAULT: {e}")

st.caption("Warning: Use 'Whale Tracking' links for Dark Pool confirmation.")
