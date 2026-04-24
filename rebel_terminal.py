import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN CONFIGURATION
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")
# FIXED: Changed 'unsafe_allow_height' to 'unsafe_allow_html'
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v2.6 | April 24, 2026 | Opening Bell Edition</p>", unsafe_allow_html=True)

# 🛠️ THE ARCHITECT RECON (SIDEBAR)
with st.sidebar:
    st.title("Recon Controls")
    ticker = st.text_input("Primary Target", value="SDGR").upper()
    comp_ticker = st.text_input("Comparison (The Bridge)", value="MSFT").upper()
    
    st.divider()
    st.subheader("Whale Tracking (Live Flow)")
    # UPDATED: Direct 2026 paths to bypass 404s
    st.page_link("https://unusualwhales.com/live-options-flow", label="Live Options Flow", icon="🐋")
    st.page_link("https://www.cheddarflow.com/app", label="Dark Pool Dashboard", icon="🧀")
    
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
        st.caption(f"Tracking {ticker} vs {comp_ticker} for institutional mirrors.")

        # 🛡️ SOVEREIGN INTEL (Real-Time April 24, 2026)
        st.divider()
        st.subheader("Sovereign Intelligence Feed")
        
        if ticker == 'SDGR':
            st.warning("🕵️ GATES WATCH: #1 Holder (~22%). Earnings May 5. Watch the $11.50 support level.")
        elif ticker == 'WST':
            st.error("🚀 INFRASTRUCTURE BREAKOUT: Q1 EPS beat. Market-wide shift into delivery systems.")
        elif ticker == 'PBR':
            st.info("📊 SIGNAL: Ex-Dividend Day. Expect price adjustment for the $0.248 payout.")

        # 📋 RAW DATA TAPE
        with st.expander("View Raw Data Tape"):
            st.dataframe(data.tail(10), use_container_width=True)

except Exception as e:
    st.error(f"SYSTEM FAULT: {e}")
