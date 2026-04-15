import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CORE INTELLIGENCE & NEWS LINKS ---
# Data locked for April 15, 2026 Shift
INTEL = {
    "SNDK": {"news": "https://www.nasdaq.com/market-activity/stocks/sndk/news", "memo": "Nasdaq-100 inclusion 4.20.26. $600B passive buy.", "own": "92.4%", "stop": 751.93},
    "MRVL": {"news": "https://www.marvell.com/company/newsroom.html", "memo": "$2B NVIDIA partnership. AI networking lead.", "own": "78.4%", "stop": 122.50},
    "CIEN": {"news": "https://www.ciena.com/about/newsroom", "memo": "Zacks #1. Record $7B AI backlog. Optical leader.", "own": "97.8%", "stop": 389.56},
    "STX": {"news": "https://www.seagate.com/news/", "memo": "AI storage surge. Earnings catalyst 4.28.26.", "own": "94.2%", "stop": 420.10},
    "AUGO": {"news": "https://auraminerals.com/investors/news-releases/", "memo": "Record Q1 production. $105 floor support.", "own": "42.0%", "stop": 98.40}
}
TICKERS = list(INTEL.keys())

# --- 2. LAYOUT & SYNC ---
st.set_page_config(page_title="Strategic Terminal v3.17", layout="wide")
st.markdown("<style>.main { background-color: #0E1117; } div[data-testid='stMetricValue'] { color: #93C5FD; }</style>", unsafe_allow_html=True)

if 'sync' not in st.session_state: st.session_state.sync = datetime.now().strftime("%H:%M:%S")

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=60)
def get_market_data(watchlist):
    return yf.download(watchlist, period="5d", interval="15m", group_by='ticker', progress=False)

# --- 4. HEADER ---
st.title("🛡️ Strategic Master Terminal v3.17")
c_sync, c_pulse = st.columns([1, 2])
if c_sync.button("🔄 RE-SYNC ALL SYSTEMS"):
    st.cache_data.clear()
    st.session_state.sync = datetime.now().strftime("%H:%M:%S")
c_pulse.caption(f"Neural Connection: ACTIVE | Pulse: {st.session_state.sync}")

master_data = get_market_data(TICKERS)

# --- 5. TABS (The "v3.7" Layout) ---
tab_recon, tab_intel, tab_scout = st.tabs(["📊 Live Recon", "📰 Insider & News", "🔍 Market Scout"])

with tab_recon:
    target = st.selectbox("🎯 Target Recon", TICKERS)
    df = master_data[target].dropna()
    
    if not df.empty:
        # Fixed Chart Logic (Closed Parentheses)
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                           low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        curr_price = df['Close'].iloc[-1]
        m1.metric("Live Price", f"${curr_price:.2f}")
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi_val = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
        m2.metric("RSI (14m)", f"{rsi_val:.2f}")
        m3.metric("STOP LOSS", f"${INTEL[target]['stop']}")

with tab_intel:
    i_target = st.selectbox("🎯 Intelligence Select", TICKERS)
    data = INTEL[i_target]
    st.subheader(f"Strategic Intelligence: {i_target}")
    st.info(f"**Brief:** {data['memo']}")
    st.warning(f"**Institutional Support:** {data['own']}")
    st.markdown(f"🔗 [Access Live {i_target} Newsroom]({data['news']})")

with tab_scout:
    st.subheader("🔍 Market Scout Screener")
    rows = []
    for t in TICKERS:
        t_df = master_data[t].dropna()
        p = t_df['Close'].iloc[-1]
        # Scoring logic based on v3.7 logic: Price vs Support & RSI
        score = 0
        score += 1 if p > INTEL[t]['stop'] else 0
        score += 1 if p < t_df['Close'].mean() else 0 # Buying the dip
        rows.append({"Ticker": t, "Price": f"${p:.2f}", "Score": f"{score}/2", "Status": "🔥 LEAD" if score == 2 else "⏳ HOLD"})
    st.table(pd.DataFrame(rows))
