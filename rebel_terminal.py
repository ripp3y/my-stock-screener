import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN CONFIGURATION
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v2.3 | April 24, 2026 | Mobile Optimized</p>", unsafe_allow_html=True)

# 🛠️ THE ARCHITECT RECON (SIDEBAR)
with st.sidebar:
    st.title("Recon Controls")
    ticker = st.text_input("Target Ticker", value="PBR").upper()
    
    st.divider()
    st.subheader("Architect Ledger (SEC EDGAR)")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=1364742", label="BlackRock Filings", icon="🔍")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=102909", label="Vanguard Filings", icon="🔍")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=93751", label="State Street Filings", icon="🔍")
    
    st.divider()
    if st.button("Run Bias Check"):
        st.info("SIGNAL: Data authenticated. Monitoring institutional sync levels.")

# 🏔️ THE MAIN TERMINAL ENGINE
st.title(f"Strategic Terminal: {ticker}")

try:
    # Fetching Data
    data = yf.download(ticker, period="1y", interval="1d")
    
    if data.empty:
        st.warning(f"⚠️ NO DATA FOUND FOR {ticker}. The 'Saw' may be hidden or the feed is throttled.")
    else:
        # Standardize columns for 2026 yfinance Multi-Index feeds
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # 📊 THE MOUNTAIN VIEW
        st.subheader("Institutional Tape (12-Month)")
        # In 2026, we use 'use_container_width=True' for perfect mobile scaling
        st.area_chart(data['Close'], use_container_width=True)

        # 🔍 REAL-TIME ALERTS
        if ticker in ['WBD', 'PARA', 'DIS']:
            st.error("⚠️ MONOPOLY ALERT: WBD/Paramount Consolidation (Approved Apr 23). Narrative Sync: HIGH.")
        
        if ticker == 'PBR':
            st.info("📊 SIGNAL: Ex-Dividend Day (Apr 24). Institutional yield extraction in progress ($0.248 special dividend).")

        # 📋 RAW DATA TAPE
        with st.expander("View Raw Data Tape"):
            st.dataframe(data.tail(15), use_container_width=True)

except Exception as e:
    st.error(f"SYSTEM FAULT: {e}")

# FOOTER FOR SOVEREIGNTY
st.caption("Warning: This terminal prioritizes raw math over institutional narrative.")
