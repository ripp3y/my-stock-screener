import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- BACKBONE: LEGACY DATABASE ---
TARGETS = {
    "SNDK": {"link": "https://www.nasdaq.com/market-activity/stocks/sndk/news", "own": "92.4%", "floor": 873.93, "memo": "Nasdaq-100 inclusion 4.20.26."},
    "MRVL": {"link": "https://www.marvell.com/company/newsroom.html", "own": "78.4%", "floor": 132.29, "memo": "$2B NVIDIA partnership."},
    "CIEN": {"link": "https://www.ciena.com/about/newsroom", "own": "97.8%", "floor": 454.34, "memo": "Record $7B AI backlog."},
    "STX":  {"link": "https://www.seagate.com/news/", "own": "94.2%", "floor": 503.11, "memo": "AI storage demand surge."},
    "AUGO": {"link": "https://auraminerals.com/investors/news-releases/", "own": "42.0%", "floor": 103.47, "memo": "Record Q1 production."}
}

# --- BACKBONE: MOBILE-IRON CONFIG ---
st.set_page_config(page_title="Strategic Master v3.20", layout="wide")

# [MODULE: DATA-CACHING-IRON]
@st.cache_data(ttl=60)
def fetch_terminal_data(ticker_string):
    tickers = ticker_string.split(',')
    return yf.download(tickers, period="5d", interval="15m", group_by='ticker', progress=False)

# --- HEADER LOGGING ---
st.title("🛡️ Strategic Master Terminal v3.20")
st.caption(f"Neural Link: ACTIVE | System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

ticker_str = ",".join(TARGETS.keys())
master_df = fetch_terminal_data(ticker_str)

# --- [MODULE: UI-MASTER-TABS] ---
tab_scout, tab_recon, tab_intel = st.tabs(["🔍 Market Scout", "📊 Live Recon", "📰 Insider & News"])

with tab_scout:
    # [MODULE: SCOUT-5PT-LOGIC]
    st.subheader("Original Market Scout Screener")
    rows = []
    for t in TARGETS.keys():
        try:
            t_df = master_df[t].dropna()
            price = t_df['Close'].iloc[-1]
            score = 0
            score += 1 if price > TARGETS[t]['floor'] else 0
            score += 1 if t_df['Volume'].iloc[-1] > t_df['Volume'].mean() else 0
            score += 1 if price > t_df['Close'].mean() else 0
            delta = t_df['Close'].diff()
            rsi = 100 - (100 / (1 + (delta.where(delta > 0, 0).mean() / (delta.where(delta < 0, 0).abs().mean() + 1e-9))))
            score += 1 if rsi < 70 else 0
            score += 1 if float(TARGETS[t]['own'].replace('%','')) > 80 else 0
            rows.append({"Target": t, "Price": f"${price:.2f}", "Score": f"{score}/5", "Status": "🚀 LEAD" if score >= 3 else "⏳ WAIT"})
        except: continue
    st.table(pd.DataFrame(rows))

with tab_recon:
    # [MODULE: CHART-SYNTAX-SHIELD]
    sel = st.selectbox("🎯 Target Recon", list(TARGETS.keys()))
    df_sel = master_df[sel].dropna()
    if not df_sel.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        c1, c2 = st.columns(2)
        c1.metric("Live Price", f"${df_sel['Close'].iloc[-1]:.2f}")
        c2.metric("Guardian Floor", f"${TARGETS[sel]['floor']}")

with tab_intel:
    i_sel = st.selectbox("🎯 Intelligence Select", list(TARGETS.keys()), key="intel_tab")
    st.info(f"**Brief:** {TARGETS[i_sel]['memo']}")
    st.warning(f"**Institutional Weight:** {TARGETS[i_sel]['own']}")
    st.markdown(f"🔗 [Access Live {i_sel} Newsroom]({TARGETS[i_sel]['link']})")
