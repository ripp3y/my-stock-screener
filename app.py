import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. NEURAL DATA RECON (April 15, 2026 | 13:00 EST) ---
# Data Sources: Nasdaq, Morningstar, Investing.com
GUARDIAN_INTEL = {
    "SNDK": {
        "price": 880.22, 
        "change": -6.80, 
        "support": 873.93, 
        "ownership": "92.4% Institutional",
        "news_link": "https://www.nasdaq.com/market-activity/stocks/sndk/news",
        "headline": "SNDK to Replace TEAM in Nasdaq-100 on Monday, April 20."
    },
    "MRVL": {
        "price": 132.81, 
        "change": -0.76, 
        "support": 132.29, 
        "ownership": "78.4% Institutional",
        "news_link": "https://www.marvell.com/company/newsroom.html",
        "headline": "Marvell/NVIDIA Partnership Deepens via NVLink Integration."
    },
    "CIEN": {
        "price": 460.47, 
        "change": -1.45, 
        "support": 454.34, 
        "ownership": "97.8% Institutional",
        "news_link": "https://www.ciena.com/about/newsroom",
        "headline": "Zacks #1 Rank; Record $7B Backlog for AI Infrastructure."
    }
}

# --- 2. THE SIGNAL PULSE ---
st.set_page_config(page_title="Strategic Terminal v3.13", layout="wide")
st.title("🛡️ Strategic Command Center v3.13")
st.caption(f"Neural Connection Active | Live Market Pulse: {datetime.now().strftime('%H:%M:%S')}")

# --- 3. TARGET RECON & CHART ---
target = st.selectbox("🎯 Target Analysis", list(GUARDIAN_INTEL.keys()))
intel = GUARDIAN_INTEL[target]

# Live Chart Integration (v3.13 Update)
@st.cache_data(ttl=60)
def get_chart_data(ticker):
    return yf.download(ticker, period="5d", interval="15m", progress=False)

df = get_chart_data(target)

if not df.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#22C55E', decreasing_line_color='#EF4444'
    )])
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0
