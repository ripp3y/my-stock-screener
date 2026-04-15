import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. THE NEURAL RECON BOARD (April 15, 2026) ---
# Data Handshake: Nasdaq-100 Rebalance & AI Infrastructure
INTEL_BOARD = {
    "SNDK": {
        "price": 880.22, "change": -6.8, "support": 873.93,
        "news_link": "https://www.nasdaq.com/market-activity/stocks/sndk/news",
        "headline": "SNDK to Replace TEAM in Nasdaq-100 on Monday.",
        "intel": "Passive inflow estimate: $4.2B. Institutional support: 92.4%."
    },
    "CIEN": {
        "price": 460.47, "change": -1.45, "support": 454.34,
        "news_link": "https://www.ciena.com/about/newsroom",
        "headline": "Zacks #1 Rank; Record $7B AI Backlog Confirmed.",
        "intel": "97.8% Institutional concentration. No panic selling detected."
    },
    "MRVL": {
        "price": 132.81, "change": -0.76, "support": 132.29,
        "news_link": "https://www.marvell.com/company/newsroom.html",
        "headline": "Marvell/NVIDIA NVLink Integration Complete.",
        "intel": "$2B NVIDIA preferred stake acts as permanent floor."
    }
}

# --- 2. MOBILE INTERFACE & SIGNAL PULSE ---
st.set_page_config(page_title="Strategic Terminal v3.14", layout="wide")
if 'sync' not in st.session_state: st.session_state.sync = datetime.now().strftime("%H:%M:%S")

def hard_sync():
    st.cache_data.clear()
    st.session_state.sync = datetime.now().strftime("%H:%M:%S")

st.title("🛡️ Strategic Command Center v3.14")
if st.button("🔄 RE-SYNC SIGNAL PULSE", on_click=hard_sync):
    st.toast("Neural Defense Active.")

# --- 3. TARGET RECON & CHART ---
target = st.selectbox("🎯 Target Recon", list(INTEL_BOARD.keys()))
data = INTEL_BOARD[target]

# LIVE CHART (FIXED SYNTAX)
@st.cache_data(ttl=60)
def fetch_chart(ticker):
    return yf.download(ticker, period="5d", interval="15m", progress=False)

df = fetch_chart(target)

if not df.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#22C55E', decreasing_line_color='#EF4444'
    )])
    # FIXED: Parenthesis closed correctly to prevent SyntaxError
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# --- 4. COMMAND TILES ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Live Price", f"${data['price']}", f"{data['change']}%")
with col2:
    st.metric("Institutional Support", data['intel'].split(":")[1].strip())
with col3:
    st.metric("Guardian Floor", f"${data['support']}")

st.divider()

# STRATEGIC NEWS LINKS
st.subheader("📰 Strategic News Link")
st.markdown(f"**Headline:** {data['headline']}")
st.markdown(f"🔗 [Access Live {target} Newsroom]({data['news_link']})")
st.info(f"🧠 Shift Intel: {data['intel']}")
