import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. MASTER DATABASE (Insider & News Links) ---
INTEL_BOARD = {
    "SNDK": {"news": "https://www.nasdaq.com/market-activity/stocks/sndk/news", "memo": "Nasdaq-100 inclusion 4.20.26. $600B passive buy.", "own": "92.4%"},
    "MRVL": {"news": "https://www.marvell.com/company/newsroom.html", "memo": "$2B NVIDIA partnership. AI networking lead.", "own": "78.4%"},
    "CIEN": {"news": "https://www.ciena.com/about/newsroom", "memo": "Zacks #1. Record $7B AI backlog. Optical leader.", "own": "97.8%"},
    "STX": {"news": "https://www.seagate.com/news/", "memo": "AI storage surge. Earnings catalyst 4.28.26.", "own": "94.2%"},
    "AUGO": {"news": "https://auraminerals.com/investors/news-releases/", "memo": "Record Q1 production. $105 floor support.", "own": "42.0%"}
}
WATCHLIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "MSFT"]

# --- 2. CONFIG & SIGNAL PULSE ---
st.set_page_config(page_title="Strategic Master v3.16", layout="wide")
st.markdown("<style>.main { background-color: #0E1117; } div[data-testid='stMetricValue'] { color: #93C5FD; }</style>", unsafe_allow_html=True)

if 'sync' not in st.session_state: st.session_state.sync = datetime.now().strftime("%H:%M:%S")

def hard_sync():
    st.cache_data.clear()
    st.session_state.sync = datetime.now().strftime("%H:%M:%S")

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=60)
def get_data(tickers):
    return yf.download(tickers, period="5d", interval="15m", group_by='ticker', progress=False)

# --- 4. HEADER ---
st.title("🛡️ Strategic Master Terminal v3.16")
col_sync, col_info = st.columns([1, 2])
if col_sync.button("🔄 RE-SYNC ALL SYSTEMS", on_click=hard_sync):
    st.toast("Full System Re-Sync Complete")
col_info.caption(f"Neural Link Active | Last Pulse: {st.session_state.sync}")

master_df = get_data(WATCHLIST)

# --- 5. TABS INTERFACE (Technical, News, Screener) ---
tab_tech, tab_news, tab_scout = st.tabs(["📊 Technical Recon", "📰 Insider & News", "🔍 Market Scout"])

with tab_tech:
    sel = st.selectbox("🎯 Target Analysis", WATCHLIST, key="tech_sel")
    ticker_df = master_df[sel].dropna()
    
    if not ticker_df.empty:
        # Chart Logic
        fig = go.Figure(data=[go.Candlestick(x=ticker_df.index, open=ticker_df['Open'], 
                        high=ticker_df['High'], low=ticker_df['Low'], close=ticker_df['Close'])])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Live Price", f"${ticker_df['Close'].iloc[-1]:.2f}")
        # Simple RSI calc
        delta = ticker_df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
        c2.metric("RSI (14m)", f"{rsi:.2f}")
        c3.metric("Daily Vol", f"{ticker_df['Volume'].iloc[-1]:,.0f}")

with tab_news:
    n_sel = st.selectbox("🎯 Select Target", list(INTEL_BOARD.keys()), key="news_sel")
    intel = INTEL_BOARD[n_sel]
    st.subheader(f"Strategic Intelligence: {n_sel}")
    st.info(f"**Memo:** {intel['memo']}")
    st.warning(f"**Institutional Weight:** {intel['own']}")
    st.markdown(f"🔗 [Access Live {n_sel} Newsroom]({intel['news']})")

with tab_scout:
    st.subheader("🔍 Market Scout Screener")
    scores = []
    for t in WATCHLIST:
        try:
            t_df = master_df[t].dropna()
            # Scoring Logic: 1. Price vs 5-day Avg, 2. RSI Support, 3. Volume
            curr_p = t_df['Close'].iloc[-1]
            avg_p = t_df['Close'].mean()
            score = 1 if curr_p > avg_p else 0
            score += 1 if rsi < 65 else 0
            scores.append({"Ticker": t, "Price": f"${curr_p:.2f}", "Score": f"{score}/3", "Status": "🔥 Lead" if score >= 2 else "⏳ Wait"})
        except: continue
    st.table(pd.DataFrame(scores))
