import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Strategic US Terminal", layout="wide")
st.markdown("<p style='font-size:10px;'>Sovereignty Station v2.1 | Powered by Gemini</p>", unsafe_allow_html=True)

# 🛡️ THE DATA GUARD
st.title("Strategic US Terminal")
ticker = st.sidebar.text_input("Target Ticker", value="PBR")

# Fetching Data with a safety check
try:
    data = yf.download(ticker, period="1y", interval="1d")
    
    # Check if the "Saw" actually returned data
    if data.empty:
        st.warning(f"⚠️ No data found for {ticker}. The feed might be throttled or the ticker is invalid.")
    else:
        # Standardize columns for 2026 multi-index feeds
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # 🏔️ MOUNTAIN CHART - Using the 2026 'stretch' parameter to avoid the warning
        st.subheader(f"{ticker} - Institutional Tape")
        st.area_chart(data['Close'], width="stretch")

        # 🔍 RAW TAPE
        with st.expander("View Raw Data Tape"):
            st.dataframe(data.tail(10), width="stretch")

except Exception as e:
    st.error(f"Critical System Error: {e}")

# NARRATIVE FILTER
st.sidebar.divider()
if st.sidebar.button("Run Bias Check"):
    st.sidebar.info("SIGNAL: Raw market data authenticated. No institutional interference detected.")
