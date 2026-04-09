import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CONFIG & RECOVERY DATA ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Your current roster with hardwired 'Fail-Safe' data
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
    # Includes SPY to calculate your Relative Strength (RS)
    all_syms = tickers + ["SPY"]
    try:
        data = yf.download(all_syms, period="1y", interval="1d", group_by='ticker')
        return data
    except Exception:
        return None

# --- 2. THE COMMAND ENGINE ---
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
            # Accumulation Scout (Volume > 120% of 20-day avg)
            avg_vol = df['Volume'].rolling(20).mean().iloc[-1]
            acc = df['Volume'].iloc[-1] > (avg_vol * 1.2)
            # Relative Strength (vs SPY over 20 days)
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            # Days to Earnings
            e_date = datetime.strptime(team_intel[t]['earn'], "%Y-%m-%d")
            days_left = (e_date - datetime.now()).days
            
            stats.append({
                "ticker": t, "price": price, "rs": rs, "acc": acc, "days": days_left
            })
        except Exception: continue

    # LEADERBOARD (Sorted by Strength)
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['rs']*100:+.1f}% RS")
            if s['acc']: st.success("💎 ACCUM")
            if s['days'] < 7: st.warning("⚠️ EARN")

    st.divider()

    # --- 3. TACTICAL ANALYSIS ---
    sel = st.selectbox("Strategic Analysis Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2 = st.tabs(["📊 Technicals", "💰 Institutional Scout"])

    with tab1:
        df_sel = data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.add_hline(y=team_intel[sel]['target'], line_dash="dot", line_color="white")
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        intel = team_intel[sel]
        # P/E Warning Logic
        try:
            info = yf.Ticker(sel).info
            pe = info.get('trailingPE', 0.0)
            margin = info.get('profitMargins', 0.0) * 100
        except Exception: pe, margin = 0.0, 0.0

        c1, c2, c3 = st.columns(3)
        c1.metric("Inst. Own", f"{intel['own']}%")
        c2.metric("Earnings Date", intel['earn'])
        c3.metric("P/E Ratio", f"{pe:.1f}x", delta="EXTREME" if pe > 50 else "NORMAL", delta_color="inverse")
        
        st.progress(min(intel['own']/100, 1.0))
        if pe > 100: st.error(f"🚨 {sel} P/E ({pe:.1f}x) is dangerously high. It needs a huge surprise to hold this price.")
else:
    st.error("📡 Sync Issue: Yahoo is currently rate-limiting. Try again in 2 minutes.")
