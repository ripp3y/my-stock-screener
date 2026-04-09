import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CONFIG & RECOVERY DATA ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Hardwired data to prevent 0.0% errors from Yahoo rate limiting
team_intel = {
    "FIX": {"target": 1800.0, "own": 96.5, "earn": "2026-05-01", "pe": 34.2},
    "ATRO": {"target": 95.0, "own": 82.1, "earn": "2026-04-28", "pe": 28.5},
    "CENX": {"target": 86.0, "own": 61.6, "earn": "2026-04-23", "pe": 12.4},
    "GEV": {"target": 1050.0, "own": 41.1, "earn": "2026-04-21", "pe": 45.1},
    "TPL": {"target": 639.0, "own": 58.2, "earn": "2026-05-06", "pe": 32.8},
    "CIEN": {"target": 430.0, "own": 88.4, "earn": "2026-06-04", "pe": 314.7},
    "STX": {"target": 620.0, "own": 79.5, "earn": "2026-04-16", "pe": 18.2},
    "PBRA": {"target": 16.2, "own": 25.4, "earn": "2026-05-14", "pe": 4.1}
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    try:
        # Fetching price data + SPY for Relative Strength
        all_syms = tickers + ["SPY"]
        return yf.download(all_syms, period="1y", interval="1d", group_by='ticker')
    except: return None

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
            # Accumulation Scout (Volume spike detection)
            avg_vol = df['Volume'].rolling(20).mean().iloc[-1]
            acc = df['Volume'].iloc[-1] > (avg_vol * 1.2)
            # Relative Strength (vs SPY over 20 days)
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            # Days to Earnings
            e_date = datetime.strptime(team_intel[t]['earn'], "%Y-%m-%d")
            days_left = (e_date - datetime.now()).days
            
            stats.append({"ticker": t, "price": price, "acc": acc, "rs": rs, "days": days_left})
        except: continue

    # LEADERBOARD (Ranked by RS)
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['rs']*100:+.1f}% RS")
            if s['acc']: st.success("💎 ACCUM")
            if s['days'] < 7: st.warning("⚠️ EARN")

    st.divider()

    # --- 3. SURPRISE SCOUT & P/E WARNINGS ---
    sel = st.selectbox("Strategic Analysis Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2 = st.tabs(["📊 Technical Floor", "💰 Institutional Scout"])

    with tab1:
        df_sel = data[sel].dropna()
        ema_9 = df_sel['Close'].ewm(span=9, adjust=False).mean()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.add_trace(go.Scatter(x=df_sel.index, y=ema_9, line=dict(color='orange', width=2), name="9-EMA"))
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        intel = team_intel[sel]
        c1, c2, c3 = st.columns(3)
        c1.metric("Inst. Own", f"{intel['own']}%")
        c2.metric("Earnings Date", intel['earn'])
        # P/E Danger Logic
        pe_val = intel['pe']
        c3.metric("P/E Ratio", f"{pe_val}x", delta="DANGER" if pe_val > 50 else "OK", delta_color="inverse")
        
        # SURPRISE ESTIMATE LOGIC
        st.subheader("Surprise Scout Estimate")
        if intel['own'] > 75 and pe_val < 40:
            st.success("✅ PROBABILITY: HIGH BEAT. Strong institutional floor and reasonable valuation.")
        elif pe_val > 100:
            st.error("🚨 RISK: HIGH. Priced for perfection. A surprise is required to avoid a drop.")
        else:
            st.warning("⚖️ PROBABILITY: MODERATE. Watch 9-EMA floor for support before the report.")

else:
    st.error("📡 Sync Issue: Yahoo Finance rate limit active. Refresh in 2 minutes.")
