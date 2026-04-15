import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- [LIBRARY: DATA-CACHING-IRON] ---
@st.cache_data(ttl=60)
def fetch_terminal_data(ticker_string):
    tickers = ticker_string.split(',')
    return yf.download(tickers, period="5d", interval="15m", group_by='ticker', progress=False)

# --- BACKBONE: THE GROWTH PORTFOLIO ---
TARGETS = {
    "SNDK": {"own": "92.4%", "floor": 873.93, "memo": "Nasdaq-100 Inclusion 4.20.26", "link": "https://www.nasdaq.com/market-activity/stocks/sndk/news"},
    "MRVL": {"own": "78.4%", "floor": 132.29, "memo": "$2B NVIDIA Stake", "link": "https://www.marvell.com/company/newsroom.html"},
    "CIEN": {"own": "97.8%", "floor": 454.34, "memo": "$7B AI Backlog", "link": "https://www.ciena.com/about/newsroom"},
    "STX":  {"own": "94.2%", "floor": 503.11, "memo": "AI Storage Leader", "link": "https://www.seagate.com/news/"},
    "AUGO": {"own": "42.0%", "floor": 103.47, "memo": "37% YoY Production Growth", "link": "https://auraminerals.com/investors/news-releases/"}
}

st.set_page_config(page_title="Strategic Forerunner v3.21", layout="wide")
st.title("🚀 Strategic Forerunner v3.21")
st.caption(f"Neural Link Active | Logged: {datetime.now().strftime('%H:%M:%S')}")

ticker_str = ",".join(TARGETS.keys())
master_df = fetch_terminal_data(ticker_str)

# --- [MODULE: UI-MASTER-TABS] ---
tab_scout, tab_recon, tab_intel = st.tabs(["🔍 MARKET SCOUT", "📊 LIVE RECON", "📰 INSIDER INTEL"])

with tab_scout:
    # [LIBRARY: SCOUT-5PT-LOGIC] - Optimized for 80-100% YoY Targets
    st.subheader("High-Velocity Growth Screener")
    scout_data = []
    for t in TARGETS.keys():
        try:
            t_df = master_df[t].dropna()
            p = t_df['Close'].iloc[-1]
            avg_p = t_df['Close'].mean()
            
            # Scoring Logic
            score = 0
            score += 1 if p > TARGETS[t]['floor'] else 0  # 1. Defense
            score += 1 if p > avg_p else 0               # 2. Momentum
            score += 1 if float(TARGETS[t]['own'].replace('%','')) > 70 else 0 # 3. Inst
            score += 1 if t_df['Volume'].iloc[-1] > t_df['Volume'].mean() else 0 # 4. Vol
            # Quick RSI Calc
            delta = t_df['Close'].diff()
            rsi = 100 - (100 / (1 + (delta.where(delta > 0, 0).mean() / (delta.where(delta < 0, 0).abs().mean() + 1e-9))))
            score += 1 if rsi < 70 else 0                # 5. Runway
            
            scout_data.append({
                "Ticker": t,
                "Price": f"${p:.2f}",
                "Scout Score": f"{score}/5",
                "Signal": "🔥 HIGH VELOCITY" if score >= 4 else "⚖️ STABLE" if score == 3 else "⏳ ACCUMULATING"
            })
        except: continue
    
    st.table(pd.DataFrame(scout_data))
    st.info("💡 Target Goal: Identifying assets with the technical and institutional backing for 80-100% YoY expansion.")

with tab_recon:
    # [LIBRARY: CHART-SYNTAX-SHIELD]
    sel = st.selectbox("🎯 Active Recon", list(TARGETS.keys()))
    df_sel = master_df[sel].dropna()
    if not df_sel.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Live Price", f"${df_sel['Close'].iloc[-1]:.2f}", f"{((df_sel['Close'].iloc[-1]/TARGETS[sel]['floor'])-1)*100:.2f}% vs Floor")

with tab_intel:
    i_sel = st.selectbox("🎯 Intelligence Select", list(TARGETS.keys()), key="intel_tab")
    st.markdown(f"### {i_sel} Catalyst: {TARGETS[i_sel]['memo']}")
    st.markdown(f"🔗 [Access Live {i_sel} Newsroom]({TARGETS[i_sel]['link']})")
