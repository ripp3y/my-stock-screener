import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CORE INTELLIGENCE DATABASE (Consolidated from v3.7 - v3.14) ---
# Current Date: April 15, 2026
INTEL_BOARD = {
    "SNDK": {
        "memo": "Nasdaq-100 inclusion set for Monday 4/20. $600B in passive funds must buy. Front-running target: $1k.",
        "ownership": "92.4% Institutional",
        "insider": "Zero sales in April. Holders waiting for the index spike.",
        "news_link": "https://www.nasdaq.com/market-activity/stocks/sndk/news",
        "support": 873.93
    },
    "MRVL": {
        "memo": "$2B NVIDIA partnership (4.1.26). Networking lead for NVLink Fusion AI clusters.",
        "ownership": "78.4% Institutional",
        "insider": "NVIDIA now a major preferred shareholder. Strategic lock-up active.",
        "news_link": "https://www.marvell.com/company/newsroom.html",
        "support": 132.29
    },
    "CIEN": {
        "memo": "Zacks #1 Rank. Optical AI networking leader. $7B in backlogged AI orders expected in FY2026.",
        "ownership": "97.8% Institutional",
        "insider": "Pre-planned 10b5-1 sales only. High retention index.",
        "news_link": "https://www.ciena.com/about/newsroom",
        "support": 454.34
    },
    "AUGO": {
        "memo": "Record Q1 production (82k oz). BB- Credit upgrade. $386M Guatemala project greenlit.",
        "ownership": "42% Strategic/Inst.",
        "insider": "CEO option exercises in March. No panic selling.",
        "news_link": "https://auraminerals.com/investors/news-releases/",
        "support": 103.47
    }
}

# --- 2. MOBILE-OPTIMIZED UI SETTINGS ---
st.set_page_config(page_title="Strategic Master v3.15", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for dark-mode high contrast
st.markdown("""<style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { color: #93C5FD; font-size: 24px; }
    div[data-testid="stExpander"] { background-color: #1E293B; border: 1px solid #3B82F6; }
    </style>""", unsafe_allow_html=True)

# Signal Pulse Sync Logic
if 'sync_time' not in st.session_state:
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

def hard_sync():
    st.cache_data.clear()
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

# --- 3. HEADER & SIGNAL PULSE ---
st.title("🛡️ Strategic Master Build v3.15")
st.caption(f"Neural Connection: ACTIVE | Last Hard-Sync: {st.session_state.sync_time}")

if st.button("🔄 WAKE CONNECTION / RE-SYNC", on_click=hard_sync):
    st.toast("Neural Link Re-Established.")

# --- 4. DATA ENGINE ---
@st.cache_data(ttl=60)
def fetch_live_data(ticker):
    # Fetching 5 days of 15-minute intervals for intraday precision
    return yf.download(ticker, period="5d", interval="15m", progress=False)

# --- 5. TARGET RECON INTERFACE ---
sel = st.selectbox("🎯 Target Recon", list(INTEL_BOARD.keys()))
intel = INTEL_BOARD[sel]
df = fetch_live_data(sel)

# DYNAMIC CHART (Fixed Parenthesis from v3.14)
if not df.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#22C55E', decreasing_line_color='#EF4444'
    )])
    fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# --- 6. COMMAND TILES (Consolidated Metrics) ---
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Live Price", f"${df['Close'].iloc[-1]:.2f}")
with c2:
    st.metric("Inst. Weight", intel['ownership'])
with c3:
    st.metric("Guardian Floor", f"${intel['support']}")

# --- 7. STRATEGIC INSIDER BOARD ---
with st.expander("📝 Strategic Insider Board & News", expanded=True):
    st.markdown(f"**Strategy Memo:** {intel['memo']}")
    st.divider()
    st.write(f"**News:** {intel['headline'] if 'headline' in intel else 'Checking latest feeds...'}")
    st.markdown(f"🔗 [Access Live {sel} Newsroom]({intel['news_link']})")
    st.write(f"**Insider Intel:** {intel['insider']}")

# --- 8. RSI ALERT SYSTEM ---
delta = df['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rsi_val = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]

st.divider()
st.progress(min(float(rsi_val)/100, 1.0), text=f"Current RSI: {rsi_val:.2f}")
