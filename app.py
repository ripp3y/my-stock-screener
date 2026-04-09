import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & RECOVERY DATA ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Updated targets and "Hardwired" backup for when Yahoo rate limits you
team_intel = {
    "FIX": {"target": 1800.00, "own": 96.5, "earn": "May 01"},
    "ATRO": {"target": 95.00, "own": 82.1, "earn": "Apr 28"},
    "CENX": {"target": 86.00, "own": 61.6, "earn": "Apr 23"},
    "GEV": {"target": 1050.00, "own": 41.1, "earn": "Apr 21"},
    "BW": {"target": 20.33, "own": 34.2, "earn": "May 08"},
    "TPL": {"target": 639.00, "own": 58.2, "earn": "May 06"},
    "CIEN": {"target": 430.00, "own": 88.4, "earn": "Jun 04"},
    "STX": {"target": 620.00, "own": 79.5, "earn": "Apr 16"},
    "PBRA": {"target": 16.20, "own": 25.4, "earn": "May 14"},
    "MRNA": {"target": 115.00, "own": 62.0, "earn": "May 02"}
}

@st.cache_data(ttl=600)
def fetch_market_data(tickers):
    # Minimal fetch to avoid "Too Many Requests" errors
    try:
        data = yf.download(tickers, period="1y", interval="1d", group_by='ticker')
        return data
    except:
        return None

# --- 2. THE TERMINAL ENGINE ---
st.title("🚀 Alpha Scout: Strategic Command")
tickers = list(team_intel.keys())
data = fetch_market_data(tickers)

if data is not None:
    stats = []
    for t in tickers:
        try:
            df = data[t].dropna()
            price = df['Close'].iloc[-1]
            target = team_intel[t]['target']
            risk = ((price - target) / target) * 100
            stats.append({"ticker": t, "price": price, "risk": risk, "df": df})
        except:
            continue
    
    # MOBILE LEADERBOARD
    sorted_stats = sorted(stats, key=lambda x: x['risk'])
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['risk']:+.1f}%")

    st.divider()

    # --- 3. SURPRISE SCOUT & ANALYSIS ---
    sel = st.selectbox("Strategic Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2 = st.tabs(["📊 Technicals", "💰 Surprise Scout"])

    with tab1:
        # Candlestick Logic with fixed syntax
        df_sel = data[sel].dropna()
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close']))
        fig.add_hline(y=team_intel[sel]['target'], line_dash="dot", line_color="white")
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        intel = team_intel[sel]
        c1, c2, c3 = st.columns(3)
        c1.metric("Institutional Own", f"{intel['own']}%")
        c2.metric("Next Earnings", intel['earn'])
        c3.metric("Target Price", f"${intel['target']}")
        
        st.info(f"**Surprise Factor:** {sel} has high institutional support ({intel['own']}%).")
        st.progress(intel['own']/100)
else:
    st.error("📡 Sync Issue: Yahoo Finance rate limit active. Try again in 2 minutes.")
