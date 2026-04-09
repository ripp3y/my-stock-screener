import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# --- 1. CONFIG & RECOVERY INTEL ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Your updated list with targets and backup data
team_intel = {
    "FIX": {"target": 1800.00, "own": 96.5, "earn": "2026-05-01"},
    "ATRO": {"target": 95.00, "own": 82.1, "earn": "2026-04-28"},
    "CENX": {"target": 86.00, "own": 61.6, "earn": "2026-04-23"},
    "GEV": {"target": 1050.00, "own": 41.1, "earn": "2026-04-21"},
    "TPL": {"target": 639.00, "own": 58.2, "earn": "2026-05-06"},
    "CIEN": {"target": 430.00, "own": 88.4, "earn": "2026-06-04"},
    "STX": {"target": 620.00, "own": 79.5, "earn": "2026-04-16"},
    "PBRA": {"target": 16.20, "own": 25.4, "earn": "2026-05-14"}
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    # Fetch team + SPY for Relative Strength comparison
    all_syms = tickers + ["SPY"]
    try:
        data = yf.download(all_syms, period="1y", interval="1d", group_by='ticker')
        return data
    except:
        return None

# --- 2. THE ENGINE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
data = fetch_scout_data(tickers)

if data is not None:
    stats = []
    spy_df = data["SPY"].dropna()
    
    for t in tickers:
        try:
            df = data[t].dropna()
            price = df['Close'].iloc[-1]
            # Technicals
            ema_9 = df['Close'].ewm(span=9, adjust=False).mean().iloc[-1]
            ema_50 = df['Close'].ewm(span=50, adjust=False).mean().iloc[-1]
            # Accumulation (Volume > 120% of 20-day avg)
            avg_vol = df['Volume'].rolling(20).mean().iloc[-1]
            acc = df['Volume'].iloc[-1] > (avg_vol * 1.2)
            # Relative Strength (vs SPY over last 20 days)
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            # Days to Earnings
            e_date = datetime.strptime(team_intel[t
