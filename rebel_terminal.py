import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Strategic US Terminal", layout="wide")
st.markdown("<p style='font-size: 11px; color: gray;'>Powered by Gemini</p>", unsafe_allow_html=True)

# Define Core Tabs
terminal_tab, screener_tab = st.tabs(["📊 Strategic Terminal", "🔍 Breakout Screener"])

with terminal_tab:
    st.header("Core Infrastructure Monitor")
    # Mountain Chart and Bridge Chart logic here

with screener_tab:
    st.header("High Alpha / Tight Channel Screener")
    # logic to calculate (High/Low)/Close over 10 days to find 'Tight Channels'
