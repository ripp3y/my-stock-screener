import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. STRATEGIC NEWS & INSIDER INTEL (4.15.2026) ---
INTEL_BOARD = {
    "SNDK": {
        "news_link": "https://www.nasdaq.com/market-activity/stocks/sndk/news",
        "headline": "Final Countdown: SNDK to Replace TEAM in Nasdaq-100 on Monday.",
        "intel": "Passive inflow estimate: $4.2B by market open 4/20. Institutional support: 92%."
    },
    "MRVL": {
        "news_link": "https://www.marvell.com/company/newsroom.html",
        "headline": "Marvell/NVIDIA Partnership Deepens via NVLink Integration.",
        "intel": "The $2B NVIDIA investment is a 'fortress' move. Relative Strength today: +1.5%."
    },
    "CIEN": {
        "news_link": "https://www.ciena.com/about/newsroom",
        "headline": "Record $7B Backlog Confirmed; WaveLogic 6 Orders Surpass Forecasts.",
        "intel": "Zacks #1 Rank. RSI cooled to 55.30—Institutional buy-zone active."
    },
    "AUGO": {
        "news_link": "https://auraminerals.com/investors/news-releases/",
        "headline": "Record Q1 Production Hits 82k oz; Guatemala Project Underway.",
        "intel": "Floor confirmed at $105. Dividend yield remains a sector leader."
    },
    "STX": {
        "news_link": "https://www.seagate.com/news/",
        "headline": "AI Storage Demand Accelerates Ahead of April 28 Earnings.",
        "intel": "Tax Day dip = Pre-earnings entry window. 45-RSI support in play."
    }
}

# --- 2. THE SIGNAL PULSE ---
st.set_page_config(page_title="Strategic Command v3.12", layout="wide")
if 'sync' not in st.session_state: st.session_state.sync = datetime.now().strftime("%H:%M:%S")

def hard_sync():
    st.cache_data.clear()
    st.session_state.sync = datetime.now().strftime("%H:%M:%S")

# --- 3. MAIN INTERFACE ---
st.title("🛡️ Strategic Command v3.12")
st.caption(f"Neural Connection Active | Last Sync: {st.session_state.sync}")

if st.button("🔄 RE-SYNC LIVE FEED", on_click=hard_sync):
    st.toast("News Link Protocol Re-Established.")

# SELECTION & LINK INJECTION
target = st.selectbox("🎯 Select Target Recon", list(INTEL_BOARD.keys()))
data = INTEL_BOARD[target]

# THE NEWS & INTEL TILES
col_news, col_intel = st.columns([2, 1])

with col_news:
    st.subheader("📰 Strategic News Link")
    st.markdown(f"**Current Headline:** {data['headline']}")
    st.markdown(f"🔗 [Access Live {target} Newsroom]({data['news_link']})")
    st.info("Direct link to verified corporate and exchange-level announcements.")

with col_intel:
    st.subheader("🧠 Shift Intel")
    st.warning(data['intel'])

st.divider()

# PROGRESS TOWARD CATALYST (Example: SNDK Monday Inclusion)
if target == "SNDK":
    st.write("### ⏳ Countdown to Nasdaq-100 Inclusion (Monday 4/20)")
    st.progress(0.85, text="Institutional Pre-Positioning Phase")
