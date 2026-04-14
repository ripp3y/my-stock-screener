import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. NEURAL LINK (The Brain) ---
# This is our shared memory. Update this top section to sync our chat strategy.
STRATEGY_LOG = {
    "AUGO": "Rebalance window (Fri/Mon). Era Dorada approved ($382M). Watch $105 floor.",
    "MRVL": "2nm AI Breakout. Record $8.2B revenue. Strong Institutional buy signal.",
    "FIX": "Strong backlog. Neutral trend. Watching for next breakout trigger.",
    "SNDK": "Tracking semi-conductor sector momentum. Watching RSI 70 level."
}

# The universe your Scout will scan
SCAN_LIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO", "NVDA", "AMD", "TSM", "AAPL", "MSFT"]

# --- 2. CONFIG & STYLING ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #93C5FD; }
    div[data-testid="stExpander"] { background-color: #1E293B; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SECURED DATA ENGINES ---
@st.cache_data(ttl=600)
def fetch_prices(
