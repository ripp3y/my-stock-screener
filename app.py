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
    except:
        return None

def fetch_insiders(symbol):
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}"
    try:
        r = requests.get(url).json()
        data_list = r.get('data', [])
        return pd.DataFrame(data_list) if data_list else pd.DataFrame()
    except:
        return pd.DataFrame()

# --- 2. THE ENGINE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers)

if all_data is not None:
    # Sidebar Logic
    with st.sidebar:
        st.header("🌐 Market Regime")
        try:
            vix = all_data["^VIX"]['Close'].iloc[-1]
            if vix < 20:
                st.success(f"BULL REGIME (VIX: {vix:.1f})")
            elif vix < 30:
                st.warning(f"CAUTION (VIX: {vix:.1f})")
            else:
                st.error(f"BEAR REGIME (VIX: {vix:.1f})")
        except:
            st.info("VIX data unavailable.")

    stats = []
    spy_df = all_data["SPY"].dropna()
    for t in tickers:
        try:
            df = all_data[t].dropna()
            price = df['Close'].iloc[-1]
            daily_chg = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": price, "rs": rs, "daily": daily_chg})
        except:
            continue

    # Main Metric Leaderboard
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(label=s['ticker'], value=f"${s['price']:.2f}", delta=f"{s['daily']:+.2f}%")
            st.caption(f"RS: {s['rs']*100:+.1f}%")

    st.divider()

    # --- 3. TACTICAL ANALYSIS ---
    sel = st.selectbox("Select Scout Target", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders", "🔗 Correlation"])

    with tab1:
        df_sel = all_data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        df_r = all_data[sel].dropna()
        high_low = df_r['High'] - df_r['Low']
        high_cp = (df_r['High'] - df_r['
