import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN CONFIGURATION
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v2.9 | April 24, 2026 | Headline Tape Active</p>", unsafe_allow_html=True)

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
    # Fetching Data (5d window to ensure we have previous close for delta)
    data = yf.download(ticker, period="5d", interval="1d")
    comp_data = yf.download(comp_ticker, period="5d", interval="1d")
    
    if not data.empty:
        # Standardize Columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if isinstance(comp_data.columns, pd.MultiIndex):
            comp_data.columns = comp_data.columns.get_level_values(0)

        # 📊 HEADLINE TAPE (Price & % Change)
        col1, col2 = st.columns(2)
        
        # --- Primary Metric Calculation ---
        curr_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        price_delta = curr_price - prev_close
        pct_delta = (price_delta / prev_close) * 100
        
        col1.metric(
            label=f"{ticker} Current", 
            value=f"${curr_price:,.2f}", 
            delta=f"${price_delta:+.2f} ({pct_delta:+.2f}%)"
        )

        # --- Comparison Metric Calculation ---
        comp_price = comp_data['Close'].iloc[-1]
        comp_prev = comp_data['Close'].iloc[-2]
        comp_delta = comp_price - comp_prev
        comp_pct = (comp_delta / comp_prev) * 100
        
        col2.metric(
            label=f"{comp_ticker} Current", 
            value=f"${comp_price:,.2f}", 
            delta=f"${comp_delta:+.2f} ({comp_pct:+.2f}%)"
        )

        # 📈 THE MOUNTAIN VIEW
        st.divider()
        st.area_chart(data['Close'], use_container_width=True)

        # 🔍 THE SYNC MATRIX (The Bridge)
        st.subheader("The 'Inner Circle' Bridge")
        # Pull 1y for long-term normalization
        full_hist = yf.download([ticker, comp_ticker], period="1y")['Close']
        norm_hist = full_hist / full_hist.iloc[0]
        st.line_chart(norm_hist, use_container_width=True)

        # 🛡️ SOVEREIGN INTEL (April 24, 2026 DATA)
        st.divider()
        if ticker == 'PBR':
            st.info("📊 EX-DIVIDEND: Today (Apr 24). Total Adjustment: $0.248. Capital extraction in progress.")
        elif ticker == 'SDGR':
            st.warning("🕵️ GATES WATCH: Earnings May 5. Consensus target $21.38 (~87% upside).")

except Exception as e:
    st.error(f"SYSTEM FAULT: {e}")
