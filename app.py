import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. THE NEURAL RECON BOARD (April 15, 2026) ---
# Data Sources: Simply Wall St, Investing.com, Stock Titan
INTEL_BOARD = {
    "SNDK": {
        "memo": "Nasdaq-100 Inclusion set for Monday 4/20. $600B in passive funds must buy. Structural shift.",
        "ownership": "92.4% Institutional",
        "insider": "Zero sales in April. Holders are waiting for the index spike.",
        "news": "SanDisk replaces Atlassian (TEAM) in Nasdaq-100 on 4.20.26."
    },
    "MRVL": {
        "memo": "$2B NVIDIA partnership closed earlier this month. Tying closely to NVLink Fusion AI factories.",
        "ownership": "88.1% Institutional",
        "insider": "Strong retention. NVIDIA now a major preferred shareholder.",
        "news": "NVIDIA invests $2B in MRVL via Series A preferred stock."
    },
    "CIEN": {
        "memo": "Zacks #1 Rank. $7B backlog. WaveLogic 6 dominance in AI networking.",
        "ownership": "97.8% Institutional",
        "insider": "Pre-planned 10b5-1 sale by SVP Phipps (4.1.26); retention remains high.",
        "news": "Ciena reports record $5B+ AI order outlook for FY2026."
    },
    "STX": {
        "memo": "AI Storage demand surge. Fiscal Q3 earnings due late April. Buy-the-dip opportunity.",
        "ownership": "94.2% Institutional",
        "insider": "Consistent 10b5-1 selling by CEO Mosley; typical programmatic liquidation.",
        "news": "STX slides 4.5% on Tax Day profit-taking; fundamentals untouched."
    },
    "AUGO": {
        "memo": "Record Q1 production (82k oz). BB- Credit upgrade. $386M Guatemala project active.",
        "ownership": "42% Strategic/Inst.",
        "insider": "CEO option exercises in March; shares withheld only for taxes.",
        "news": "Aura Minerals reports 37% YoY production growth in Q1."
    }
}

# --- 2. THE SIGNAL PULSE & INTERFACE ---
st.set_page_config(page_title="Strategic Terminal v3.11", layout="wide")
st.markdown("<style>.main { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)

if 'sync' not in st.session_state: st.session_state.sync = datetime.now().strftime("%H:%M:%S")

def hard_sync():
    st.cache_data.clear()
    st.session_state.sync = datetime.now().strftime("%H:%M:%S")

st.title("🛡️ Neural Guardian Terminal")
if st.button("🔄 HARD SYNC / SIGNAL PULSE", on_click=hard_sync):
    st.toast("Neural Connection Verified.")

# --- 3. DATA & ANALYSIS ---
sel = st.selectbox("🎯 Target Recon", list(INTEL_BOARD.keys()))
intel = INTEL_BOARD[sel]

# THE RECON TILES
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader
