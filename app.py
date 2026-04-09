import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# --- 1. CONFIG & API KEY ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

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
            elif vix < 30: st.warning(f"CAUTION (VIX: {vix:.1f})")
            else: st.error(f"BEAR REGIME (VIX: {vix:.1f})")
        except: st.info("VIX data unavailable.")

    stats = []
    spy_df = all_data["SPY"].dropna()
    for t in tickers:
        try:
            df = all_data[t].dropna()
            price = df['Close'].iloc[-1]
            # Daily % Change
            daily_change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            # RS Score (Relative Strength vs SPY 20d)
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": price, "rs": rs, "daily": daily_change})
        except: continue

    # LEADERBOARD (Sorted by Strength)
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            # Layout: Daily % to the right of price, RS Score directly underneath
            st.metric(
                label=s['ticker'], 
                value=f"${s['price']:.2f}", 
                delta=f"{s['daily']:+.2f}%"
            )
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
        high_cp = (df_r['High'] - df_r['Close'].shift()).abs()
        low_cp = (df_r['Low'] - df_r['Close'].shift()).abs()
        atr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1).rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        c1, c2 = st.columns(2)
        c1.metric("ATR Volatility", 
                  f"${atr:.2f}", 
                  help="ATR (Average True Range) measures the stock's 'daily noise'. A higher ATR means the stock is more volatile.")
        
        c2.metric("Trailing Stop", 
                  f"${t_stop:.2f}", 
                  delta=f"${df_r['Close'].iloc[-1] - t_stop:.2f} Buffer",
                  help="The safety floor. If price hits this, the 6-month trend is in jeopardy.")
        
        if df_r['Close'].iloc[-1] < t_stop: st.error("🚨 EXIT ALERT: Volatility floor breached.")
        else: st.success("✅ STATUS: Holding above volatility floor.")

    with tab3:
        st.subheader("Live Insider Tracker (SEC Form 4)")
        insider_df = fetch_insiders(sel)
        if not insider_df.empty:
            display_cols = [c for c in ['transactionDate', 'name', 'share', 'change', 'transactionPrice'] if c in insider_df.columns]
            st.dataframe(insider_df[display_cols], use_container_width=True)
        else:
            st.info("No recent insider transactions found.")

    with tab4:
        st.subheader("Portfolio Correlation Matrix")
        corr_df = pd.DataFrame()
        for t in tickers: corr_df[t] = all_data[t]['Close'].pct_change()
        st.plotly_chart(px.imshow(corr_df.corr(), text_auto=True, color_continuous_scale='RdBu_r'), use_container_width=True)

else:
    st.error("📡 Sync Issue
