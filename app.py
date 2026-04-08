import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & TEAM SETUP ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Your tactical targets
target_map = {
    "GEV": 863.61, "BW": 20.33, "PBR-A": 16.02, 
    "TPL": 639.00, "SNDK": 95.00, "MRNA": 115.00, 
    "CIEN": 354.01, "TIGO": 73.20, "STX": 582.00
}

@st.cache_data(ttl=600)
def fetch_ticker_data(tickers):
    # Fetching 1y history for trend analysis + fundamental data
    data = yf.download(tickers, period="1y", group_by='ticker')
    infos = {t: yf.Ticker(t).info for t in tickers}
    return data, infos

def get_signals(df):
    ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    price = df['Close'].iloc[-1]
    # Cushion: % distance from the short-term floor
    cushion = ((price - ema_9.iloc[-1]) / ema_9.iloc[-1]) * 100
    # Trend: Is the long-term floor moving up?
    is_up = ema_50.iloc[-1] > ema_50.iloc[-5]
    # Dip: Below 9-day floor but still in upward 50-day trend
    is_dip = price < ema_9.iloc[-1] and price > ema_50.iloc[-1]
    return cushion, is_up, is_dip

# --- 2. DATA PROCESSING ---
st.title("🚀 Alpha Scout: Strategic Terminal")
team_tickers = list(target_map.keys())

try:
    data, info_data = fetch_ticker_data(team_tickers)
    
    # Process all tickers for the Leaderboard
    stats = []
    for t in team_tickers:
        t_df = data[t].dropna()
        cush, up, dip = get_signals(t_df)
        stats.append({
            "ticker": t, 
            "cushion": cush, 
            "up": up, 
            "dip": dip, 
            "price": t_df['Close'].iloc[-1]
        })
    
    # Leaderboard Sorting: Best performers move to the left
    sorted_stats = sorted(stats, key=lambda x: x['cushion'], reverse=True)

    # --- 3. THE LEADERBOARD (Metrics Row) ---
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['cushion']:+.1f}%")
            if s['dip'] and s['up']: st.warning("💎 VALUE DIP")
            elif s['cushion'] < 0: st.error("📉 BREAK")
            else: st.info("🚀 STRONG")

    st.divider()

    # --- 4. TACTICAL DEEP DIVE TABS ---
    selected_ticker = st.selectbox("Strategic Analysis Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3 = st.tabs(["📊 Technical Chart", "💰 Financial Intel", "📰 News Feed"])

    with tab1:
        # Detailed Charting
        df = data[selected_ticker].dropna()
        ema_9_s = df['Close'].ewm(span=9, adjust=False).mean()
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
        
        # Candles and EMA Floor
