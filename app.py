import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. COMMAND CONFIG ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Static intel to prevent "0.0%" errors
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
        return yf.download(all_syms, period="1y", group_by='ticker')
    except: return None

def get_sentiment(news_list):
    bull = ["upgrade", "beat", "growth", "buy", "surge", "positive"]
    bear = ["downgrade", "miss", "negative", "loss", "sell", "drop"]
    score = 0
    for item in news_list:
        # Safety Filter: Prevents KeyError: 'title'
        title = item.get('title', '').lower()
        score += sum(1 for w in bull if w in title)
        score -= sum(1 for w in bear if w in title)
    return "BULLISH" if score > 0 else "BEARISH" if score < 0 else "NEUTRAL"

# --- 2. ENGINE ---
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
            # Accumulation (Vol > 120% of 20d avg)
            acc = df['Volume'].iloc[-1] > (df['Volume'].rolling(20).mean().iloc[-1] * 1.2)
            # Relative Strength (vs SPY over 20 days)
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            days = (datetime.strptime(team_intel[t]['earn'], "%Y-%m-%d") - datetime.now()).days
            stats.append({"ticker": t, "price": price, "rs": rs, "acc": acc, "days": days})
        except: continue

    # LEADERBOARD (Ranked by RS Score)
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['rs']*100:+.1f}% RS")
            if s['acc']: st.success("💎 ACCUM")
            if s['days'] < 7: st.warning("⚠️ EARN")

    st.divider()

    # --- 3. ANALYSIS ---
    sel = st.selectbox("Strategic Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3 = st.tabs(["📊 Technicals", "💰 Institutional", "📰 Sentiment"])

    with tab1:
        df_sel = data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.add_hline(y=team_intel[sel]['target'], line_dash="dot", line_color="white")
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        intel = team_intel[sel]
        try:
            info = yf.Ticker(sel).info
            pe = info.get('trailingPE', 0.0)
        except: pe = 0.0
        c1, c2, c3 = st.columns(3)
        c1.metric("Inst. Own", f"{intel['own']}%")
        c2.metric("P/E Ratio", f"{pe:.1f}x", delta="DANGER" if pe > 50 else "OK", delta_color="inverse")
        c3.metric("Earnings", intel['earn'])
        st.progress(min(intel['own']/100, 1.0))

    with tab3:
        raw_news = yf.Ticker(sel).news
        sent = get_sentiment(raw_news)
        st.metric("Sentiment Score", sent, delta="BULLISH" if sent == "BULLISH" else "CAUTION")
        for n in raw_news[:3]:
            st.write(f"**{n.get('title', 'No Title')}**")
            st.write(f"[Source]({n.get('link', '#')})")
            st.divider()
else:
    st.error("📡 Sync Issue: Yahoo is currently rate-limiting. Try again in 2 minutes.")
