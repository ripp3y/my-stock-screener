import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN CONFIGURATION
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v2.8 | April 24, 2026 | Live KPI Layer Active</p>", unsafe_allow_html=True)

# 🛠️ THE ARCHITECT RECON (SIDEBAR)
with st.sidebar:
    st.title("Recon Controls")
    ticker = st.text_input("Primary Target", value="SDGR").upper()
    comp_ticker = st.text_input("Comparison (The Bridge)", value="MSFT").upper()
    
    st.divider()
    st.subheader("Whale Tracking (2026 Verified)")
    st.page_link("https://unusualwhales.com/live-options-flow", label="Live Options Flow", icon="🐋")
    st.page_link("https://www.cheddarflow.com/features/dark-pool-data", label="Dark Pool Ledger", icon="🧀")
    
    st.divider()
    st.subheader("Architect Ledger (SEC)")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=1364742", label="BlackRock Filings", icon="🔍")
    st.page_link("https://www.sec.gov/edgar/browse/?CIK=102909", label="Vanguard Filings", icon="🔍")

# 🏔️ THE MAIN TERMINAL ENGINE
st.title(f"Strategic Terminal: {ticker}")

try:
    # Fetching Data
    data = yf.download(ticker, period="5d", interval="1d")
    comp_data = yf.download(comp_ticker, period="5d", interval="1d")
    
    if not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if isinstance(comp_data.columns, pd.MultiIndex):
            comp_data.columns = comp_data.columns.get_level_values(0)

        # 📊 LIVE KPI LAYER (Price & Percent Change)
        col1, col2 = st.columns(2)
        
        # Primary Ticker Calc
        last_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        change = last_price - prev_close
        pct_change = (change / prev_close) * 100
        
        col1.metric(f"{ticker} Price", f"${last_price:,.2f}", f"{pct_change:+.2f}%")

        # Comp Ticker Calc
        comp_last = comp_data['Close'].iloc[-1]
        comp_prev = comp_data['Close'].iloc[-2]
        comp_pct = ((comp_last - comp_prev) / comp_prev) * 100
        
        col2.metric(f"{comp_ticker} Price", f"${comp_last:,.2f}", f"{comp_pct:+.2f}%")

        # 📈 THE MOUNTAIN VIEW
        st.divider()
        st.area_chart(data['Close'], use_container_width=True)

        # 🔍 THE SYNC MATRIX
        st.subheader("The 'Inner Circle' Bridge")
        full_data = yf.download([ticker, comp_ticker], period="1y")['Close']
        norm_data = full_data / full_data.iloc[0]
        st.line_chart(norm_data, use_container_width=True)

        # 🛡️ SOVEREIGN INTEL (April 24, 2026 DATA)
        st.divider()
        if ticker == 'PBR':
            st.info("📊 EX-DIVIDEND: Today (Apr 24). Price adjusted for $0.248 extraction.")
        elif ticker == 'SDGR':
            st.warning("🕵️ GATES WATCH: Earnings May 5. Watch for accumulation at current levels.")

except Exception as e:
    st.error(f"SYSTEM FAULT: {e}")
