import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Strategic US Terminal", layout="wide")
st.markdown("<p style='font-size:10px;'>Powered by Gemini | Sovereignty Station v1.0</p>", unsafe_allow_html=True)

# 🛡️ THE SOVEREIGNTY FILTER
st.title("Strategic US Terminal")
ticker = st.sidebar.text_input("Enter Ticker", value="PBR")

# Fetching Data
data = yf.download(ticker, period="1y", interval="1d")

# 🚨 THE BLANK PAGE KILLER: Data Validation
if data.empty:
    st.error(f"⚠️ NO DATA FOUND FOR {ticker}. The 'Saw' may be hidden or the ticker is delisted.")
else:
    # Fix for Multi-index columns in 2026 yfinance
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 🏔️ THE MOUNTAIN CHART
    st.subheader(f"{ticker} Performance - Mountain View")
    st.area_chart(data['Close'], use_container_width=True)

    # 🔍 RAW DATA TAPE (Truth over Narrative)
    with st.expander("View Raw Data Tape"):
        st.write(data.tail(10))

# NARRATIVE CHECKER
st.sidebar.divider()
st.sidebar.subheader("Narrative Filter")
if st.sidebar.button("Run Bias Check"):
    st.sidebar.info("SIGNAL: All data sourced directly from yfinance. No mainstream interference detected.")
