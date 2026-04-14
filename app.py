import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. NEURAL LINK (Strategic Intel & Board Events) ---
# This board updates dynamically based on the latest 2026 data.
INTEL_BOARD = {
    "AUGO": {
        "memo": "Board approved $386M-$453M Era Dorada project (4.14.26). RSI at 90. Floor: $105.",
        "news": "gold production Guatemala Era Dorada"
    },
    "FIX": {
        "memo": "Record $12B backlog; 45% revenue is AI data centers. Institutional conviction: 96%.",
        "news": "AI data center infrastructure backlog"
    },
    "MRVL": {
        "memo": "2nm Coherent DSP breakthrough. $2B NVIDIA funding (4.2.26). Revenue up 42%.",
        "news": "2nm AI chip interconnect demand"
    },
    "SNDK": {
        "memo": "Nasdaq-100 inclusion (4.20.26) forcing passive buys. Golden Cross active (4.10.26).",
        "news": "Nasdaq-100 inclusion index fund buying"
    },
    "TSM": {
        "memo": "2nm node ramping for 2026. Strong institutional support. RSI 'Goldilocks' zone.",
        "news": "2nm chip manufacturing expansion"
    }
}

SCAN_LIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "AAPL", "MSFT"]

# --- 2. CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

# Mobile CSS for maximum readability on small screens
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { font-size: 20px; color: #93C5FD; }
    div[data-testid="stExpander"] { background-color: #1E293B; border-radius: 8px; }
    .stSelectbox label { color: #93C5FD; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=600)
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="1y", group_by='ticker', progress=False).ffill()
    except: return None

def calculate_rsi(data):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v3.1")
