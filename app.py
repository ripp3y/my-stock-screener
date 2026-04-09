import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# --- 1. CONFIG & API KEY ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# API Key must be wrapped in quotes
FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

team_intel = {
    "FIX": {"target": 1800.0, "own": 96.5, "earn": "2026-05-01"},
    "ATRO": {"target": 95.0, "own": 82.1, "earn": "2026-04-28"},
    "CENX": {"target": 86.0, "own": 61.6, "earn": "2026-04-23"},
    "GEV": {"target": 1050.0, "own": 41.1, "earn": "2026-04-21"},
    "TPL": {"target": 639.0, "own": 58.2, "earn": "2026-05-06"},
    "CIEN": {"target": 430.0, "own": 88.4, "earn": "2026-06-04"},
    "STX": {"target": 620.0, "own": 79.5, "earn": "2026-04-16"},
    "PBRA": {"target": 16.2, "own": 25.4, "earn": "2026-05-14"}
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    all_syms = tickers + ["SPY", "^VIX"]
    try:
        return yf.download(all_syms, period="1y", interval="1d", group_by='ticker')
    except: return None

def fetch_insiders(symbol):
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}"
    try:
        r = requests.get(url).json()
        data_list = r.get('data', [])
        return pd.DataFrame(data_list) if data_list else pd.DataFrame()
    except: return pd.DataFrame()

# --- 2. ENGINE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers)

if all_data is not None:
    with st.sidebar:
        st.header("🌐 Market Regime")
        try:
            vix = all_data["^VIX"]['Close'].iloc[-1]
            if vix < 20: st.success(f"BULL REGIME (VIX: {vix:.1f})")
