import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime, timedelta

# --- 1. CONFIG & API KEYS ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")
FINNHUB_KEY = d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0 # Paste your free key here

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
    all_syms = tickers + ["SPY"]
    try:
        return yf.download(all_syms, period="1y", interval="1d", group_by='ticker')
    except: return None

def fetch_insiders(symbol):
    if FINNHUB_KEY == "YOUR_FINNHUB_KEY_HERE": return None
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}"
    try:
        r = requests.get(url).json()
        return pd.DataFrame(r.get('data', []))
    except: return None

# --- 2. THE ENGINE ---
st.title("🚀 Alpha Scout: Institutional Command")
tickers = list(team_intel.keys())
data = fetch_scout_data(tickers)

if data is not None:
    stats = []
    spy_df = data["SPY"].dropna()
    for t in tickers:
        try:
            df = data[t].dropna()
            price = df['Close'].iloc[-1]
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": price, "rs": rs})
        except: continue

    # LEADERBOARD
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['rs']*100:+.1f}% RS")

    st.divider()

    # --- 3. ADVANCED TACTICAL ANALYSIS ---
    sel = st.selectbox("Select Scout Target", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insider Transactions", "🔗 Correlation", "💰 Institutional"])

    with tab1:
        df_sel = data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Volatility Floor & Money Flow")
        df_r = data[sel].dropna()
        
        # 1. ATR Trailing Stop
        high_low = df_r['High'] - df_r['Low']
        high_cp = (df_r['High'] - df_r['Close'].shift()).abs()
        low_cp = (df_r['Low'] - df_r['Close'].shift()).abs()
        atr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1).rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        # 2. Chaikin Money Flow (CMF) - Institutional Footprint
        mfv = ((df_r['Close'] - df_r['Low']) - (df_r['High'] - df_r['Close'])) / (df_r['High'] - df_r['Low'])
        mfv = mfv * df_r['Volume']
        cmf = mfv.rolling(20).sum() / df_r['Volume'].rolling(20).sum()
        curr_cmf = cmf.iloc[-1]

        c1, c2 = st.columns(2)
        c1.metric("Money Flow (CMF)", f"{curr_cmf:.2f}", delta="ACCUMULATION" if curr_cmf > 0 else "DISTRIBUTION")
        c2.metric("Trailing Stop", f"${t_stop:.2f}", delta=f"${df_r['Close'].iloc[-1] - t_stop:.2f} Buffer")
        
        if curr_cmf > 0: st.success("💎 WHALE WATCH: Institutions are actively accumulating shares.")
        else: st.warning("⚖️ BALANCE: Distribution is currently outweighing accumulation.")

    with tab3:
        st.subheader("Live Insider Tracker (SEC Form 4)")
        insider_df = fetch_insiders(sel)
        if insider_df is not None and not insider_df.empty:
            st.dataframe(insider_df[['transactionDate', 'name', 'share', 'change', 'transactionPrice']], use_container_width=True)
            st.info("💡 High-conviction signal: Multiple insiders buying at market price.")
        else:
            st.info("Paste your Finnhub API Key at the top of the code to see live Insider Buys.")

    with tab4:
        st.subheader("Portfolio Correlation")
        corr_df = pd.DataFrame()
        for t in tickers: corr_df[t] = data[t]['Close'].pct_change()
        matrix = corr_df.corr()
        st.plotly_chart(px.imshow(matrix, text_auto=True, color_continuous_scale='RdBu_r'), use_container_width=True)

    with tab5:
        intel = team_intel[sel]
        st.metric("Institutional Ownership", f"{intel['own']}%")
        st.progress(min(intel['own']/100, 1.0))

else:
    st.error("Rate limit active. Refresh in 2m.")
