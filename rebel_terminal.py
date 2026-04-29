import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Strategic Terminal", layout="wide")
st.markdown("<p style='font-size: 12px;'>Powered by Gemini</p>", unsafe_allow_html=True)

# Define Core Tabs
tab1, tab2 = st.tabs(["📊 Strategic US Terminal", "🔍 Infrastructure Screener"])

with tab1:
    st.header("Strategic US Terminal")
    # Terminal logic (Mountain Chart, Bridge Chart) goes here...

with tab2:
    st.header("Infrastructure Screener")
    # Screener logic (Volume, RSI filters) goes here...
