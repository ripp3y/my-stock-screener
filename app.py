import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import requests

# --- 1. SETTINGS ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

# API Key must be in quotes
FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0, "PBRA": 16.2
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY", "^VIX"]
    try:
        # Download and drop missing to prevent errors
        return yf.download(syms, period="1y", group_by='ticker').dropna(how='all')
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

# --- 2. DATA CORE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers) # Fixed name error

if all_data is not None:
    # Market Regime Sidebar
    with st.sidebar:
        st.header("🌐 Market Regime")
        try:
            vix = all_data["^VIX"]['Close'].iloc[-1]
            if vix < 20: st.success(f"BULL REGIME ({vix:.1f})")
            elif vix < 30: st.warning(f"CAUTION ({vix:.1f})")
            else: st.error(f"BEAR REGIME ({vix:.1f})")
        except: st.info("VIX data offline")

    # Metrics Engine
    stats = []
    spy_df = all_data["SPY"]
    for t in tickers:
        try:
            df = all_data[t]
            price = df['Close'].iloc[-1]
            # Daily Gain/Loss Calculation
            prev_close = df['Close'].iloc[-2]
            day_pct = ((price - prev_close) / prev_close) * 100
            # Relative Strength (RS) vs SPY
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": price, "rs": rs, "daily": day_pct})
        except: continue

    # Top Leaderboard
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            # Daily % to the right, RS below
            st.metric(label=s['ticker'], value=f"${s['price']:.2f}", delta=f"{s['daily']:+.2f}%")
            st.caption(f"RS: {s['rs']*100:+.1f}%")

    st.divider()

    # --- 3. TACTICAL TABS ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        df_sel = all_data[sel]
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], 
                        high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        df_r = all_data[sel]
        # ATR Calculation for Volatility Stop
        h_l = df_r['High'] - df_r['Low']
        atr = h_l.rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        c1, c2 = st.columns(2)
        c1.metric("ATR Volatility", f"${atr:.2f}", help="Daily 'noise' level.")
        c2.metric("Trailing Stop", f"${t_stop:.2f}", delta=f"${df_r['Close'].iloc[-1]-t_stop:.2f} Buffer")
        
        if df_r['Close'].iloc[-1] < t_stop: st.error("🚨 EXIT ALERT: Volatility Floor Breached")
        else: st.success("✅ STATUS: Trend Stable")

    with t3:
        st.subheader("Insider Form 4 Tracker")
        insider_df = fetch_insiders(sel)
        if not insider_df.empty:
            # Fixed column check
            view = [c for c in ['transactionDate', 'name', 'share', 'change'] if c in insider_df.columns]
            st.dataframe(insider_df[view], use_container_width=True)
        else: st.info("No recent insider data")

else:
    # Fixed string literal issue
    st.error("📡 Sync Issue: Check API or connection")
