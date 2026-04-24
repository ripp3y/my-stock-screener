import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN CONFIGURATION
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v3.0 | April 24, 2026 | 6-Month Horizon Active</p>", unsafe_allow_html=True)

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
    # UPDATED: Pulling 6 months to see the macro-cycle better
    data = yf.download(ticker, period="6mo", interval="1d")
    comp_data = yf.download(comp_ticker, period="6mo", interval="1d")
    
    if not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if isinstance(comp_data.columns, pd.MultiIndex):
            comp_data.columns = comp_data.columns.get_level_values(0)

        # 📊 HEADLINE TAPE (The "Big Font" Metrics)
        col1, col2 = st.columns(2)
        
        # Primary Ticker Delta
        curr_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        price_delta = curr_price - prev_close
        pct_delta = (price_delta / prev_close) * 100
        
        col1.metric(
            label=f"{ticker} Current", 
            value=f"${curr_price:,.2f}", 
            delta=f"${price_delta:+.2f} ({pct_delta:+.2f}%)"
        )

        # Comparison Ticker Delta
        comp_price = comp_data['Close'].iloc[-1]
        comp_prev = comp_data['Close'].iloc[-2]
        comp_delta = comp_price - comp_prev
        comp_pct = (comp_delta / comp_prev) * 100
        
        col2.metric(
            label=f"{comp_ticker} Current", 
            value=f"${comp_price:,.2f}", 
            delta=f"${comp_delta:+.2f} ({comp_pct:+.2f}%)"
        )

        # 📈 THE 6-MONTH MOUNTAIN VIEW
        st.divider()
        st.subheader(f"The 6-Month Institutional Horizon: {ticker}")
        st.area_chart(data['Close'], use_container_width=True)

        # 🔍 THE SYNC MATRIX (The Bridge)
        st.subheader("The 'Inner Circle' Bridge (Relative Performance)")
        # Normalizing to 100 for true comparison
        norm_data = data['Close'] / data['Close'].iloc[0] * 100
        norm_comp = comp_data['Close'] / comp_data['Close'].iloc[0] * 100
        combined = pd.DataFrame({ticker: norm_data, comp_ticker: norm_comp})
        st.line_chart(combined, use_container_width=True)

        # 🛡️ SOVEREIGN INTEL (April 24, 2026)
        st.divider()
        if ticker == 'PBR':
            st.info("📊 EX-DIVIDEND: Today (Apr 24). Price adjusted for $0.248 extraction.")
        elif ticker == 'SDGR':
            st.warning("🕵️ GATES WATCH: Earnings May 5. Notice the 6-month support forming.")

except Exception as e:
    st.error(f"SYSTEM FAULT: {e}")
