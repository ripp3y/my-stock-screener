import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN CONFIGURATION
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v2.4 | April 24, 2026 | The 'Bridge' Update</p>", unsafe_allow_html=True)

# 🛠️ THE ARCHITECT RECON (SIDEBAR)
with st.sidebar:
    st.title("Recon Controls")
    ticker = st.text_input("Primary Target", value="SDGR").upper()
    comp_ticker = st.text_input("Comparison (The Bridge)", value="MSFT").upper()
    
    st.divider()
    st.subheader("Architect Ledger (SEC EDGAR)")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=1364742", label="BlackRock Filings", icon="🔍")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=102909", label="Vanguard Filings", icon="🔍")
    
    if st.button("Run Sync Check"):
        st.info(f"SIGNAL: Analyzing {ticker}/{comp_ticker} correlation for 'Inner Circle' movement.")

# 🏔️ THE MAIN TERMINAL ENGINE
st.title(f"Strategic Terminal: {ticker}")

try:
    # Fetching Data for both
    data = yf.download(ticker, period="1y", interval="1d")
    comp_data = yf.download(comp_ticker, period="1y", interval="1d")
    
    if not data.empty:
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
        # Normalize data to see correlation percentages
        norm_data = data['Close'] / data['Close'].iloc[0]
        norm_comp = comp_data['Close'] / comp_data['Close'].iloc[0]
        
        combined = pd.DataFrame({ticker: norm_data, comp_ticker: norm_comp})
        st.line_chart(combined, use_container_width=True)
        st.caption(f"Tracking how {ticker} mirrors {comp_ticker} institutional moves.")

        # 🛡️ GATES WATCH ALERTS
        if ticker == 'SDGR':
            st.warning("⚠️ MOONSHOT ALERT: Gates Trust is #1 Shareholder (~22%). Physics-AI platform play.")
        if ticker == 'WST':
            st.error("⚠️ BREAKOUT CONFIRMED: Infrastructure play for GLP-1/Vaccine delivery.")

except Exception as e:
    st.error(f"SYSTEM FAULT: {e}")
