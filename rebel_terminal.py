import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN TERMINAL CONFIG
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

# Minimal Attribution
st.markdown("<p style='font-size:10px; color: #555;'>Powered by Gemini | Sovereignty v4.1 | Apr 24, 2026</p>", unsafe_allow_html=True)

# 🛠️ THE ARCHITECT SIDEBAR
with st.sidebar:
    st.title("Recon Controls")
    ticker = st.text_input("Primary Target", value="SDGR").upper()
    comp_ticker = st.text_input("Comparison Bridge", value="MSFT").upper()
    
    st.divider()
    st.subheader("Whale Tracking")
    st.page_link("https://unusualwhales.com/live-options-flow", label="Live Options Flow", icon="🐋")
    
    st.divider()
    st.subheader("May 5 Catalyst Watch")
    # Using triple quotes to prevent string errors
    st.info('''SDGR & NVTS both report earnings on May 5, 2026.''')

# 🏔️ MAIN ENGINE DATA PULL
try:
    data = yf.download(ticker, period="6mo", interval="1d")
    comp_data = yf.download(comp_ticker, period="6mo", interval="1d")

    if not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if isinstance(comp_data.columns, pd.MultiIndex):
            comp_data.columns = comp_data.columns.get_level_values(0)

        # 📟 TOP TAPE: METRICS
        st.title(f"Strategic Terminal: {ticker}")
        
        col1, col2 = st.columns(2)
        
        curr_p = data['Close'].iloc[-1]
        prev_p = data['Close'].iloc[-2]
        delta_p = curr_p - prev_p
        
        col1.metric(label=f"{ticker} Status", value=f"${curr_p:,.2f}", delta=f"{delta_p:+.2f}")
        
        comp_p = comp_data['Close'].iloc[-1]
        col2.metric(label=f"{comp_ticker} (The Bridge)", value=f"${comp_p:,.2f}")

        # 📈 THE 6-MONTH MOUNTAIN (Price)
        st.divider()
        st.subheader(f"Price Horizon: {ticker}")
        st.area_chart(data['Close'], color="#29b5e8")

        # 📊 THE VOLUME LEDGER (The Missing Bars)
        st.subheader(f"Volume Ledger (Architect Footprints)")
        st.bar_chart(data['Volume'], color="#f0f2f6")

        # 🔍 THE BRIDGE (Relative Strength)
        st.subheader("The Bridge (Normalized Performance)")
        norm_data = data['Close'] / data['Close'].iloc[0] * 100
        norm_comp = comp_data['Close'] / comp_data['Close'].iloc[0] * 100
        combined = pd.DataFrame({ticker: norm_data, comp_ticker: norm_comp})
        st.line_chart(combined)

except Exception as e:
    st.error(f"Waiting for Signal... {e}")
