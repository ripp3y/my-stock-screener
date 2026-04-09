import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. CONFIG & TOOLTIP DEFINITIONS ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

# Tooltip content for easy reference
TIPS = {
    "ATR": "Average True Range: The average daily movement. High ATR means higher 'noise'.",
    "STOP": "Volatility floor. If price breaks this, the current trend is technically compromised.",
    "RS": "Relative Strength: Performance of this stock vs the S&P 500 over the last 20 sessions."
}

FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

# Cleaned list: PBRA removed to fix download failures
team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY", "^VIX"]
    try:
        df = yf.download(syms, period="1y", group_by='ticker')
        return df.ffill()
    except:
        return None

def fetch_insiders(symbol):
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}"
    try:
        r = requests.get(url).json()
        data = r.get('data', [])
        return pd.DataFrame(data) if data else pd.DataFrame()
    except:
        return pd.DataFrame()

# --- 2. THE COMMAND CENTER ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers)

if all_data is not None:
    stats = []
    spy_df = all_data["SPY"]
    
    for t in tickers:
        try:
            df = all_data[t].dropna()
            if df.empty: continue
            
            p = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            day_pct = ((p - prev) / prev) * 100
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            
            if not pd.isna(p) and p > 0:
                stats.append({"ticker": t, "price": p, "rs": rs, "daily": day_pct})
        except: continue

    # Rank by RS score
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # FORCED HORIZONTAL LAYOUT (Markdown Table Hack)
    for s in sorted_stats:
        color = "🟢" if s['daily'] >= 0 else "🔴"
        st.markdown(f"""
        **{s['ticker']}** | Price | Day Performance | RS Score |
        | :--- | :--- | :--- |
        | **${s['
