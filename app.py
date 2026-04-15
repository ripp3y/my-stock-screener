import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- [LIBRARY: DATA-CACHING-IRON] ---
@st.cache_data(ttl=300) # Increased TTL for broad scanning
def fetch_broad_market(ticker_string):
    tickers = ticker_string.split(',')
    return yf.download(tickers, period="5d", interval="60m", group_by='ticker', progress=False)

# --- BACKBONE: BROAD SPECTRUM SECTORS ---
# Reinstating the "All-Sectors" Radar list from weeks ago
RADAR_LIST = {
    "AI/TECH": ["NVDA", "SNDK", "MRVL", "CIEN", "AMD"],
    "ENERGY/GOLD": ["AUGO", "XLE", "GDM"],
    "BIOTECH": ["IBB", "VRTX", "AMGN"],
    "GROWTH": ["TSLA", "PLTR", "SNOW"]
}

st.set_page_config(page_title="Strategic Broad Scout v3.22", layout="wide")
st.title("📡 Broad Scout Radar v3.22")
st.caption(f"Neural Link: ACTIVE | Broad Scan Initiated: {datetime.now().strftime('%H:%M:%S')}")

# Flatten list for yfinance
all_tickers = [item for sublist in RADAR_LIST.values() for item in sublist]
master_df = fetch_broad_market(",".join(all_tickers))

# --- [MODULE: UI-MASTER-TABS] ---
tab_scout, tab_recon, tab_intel = st.tabs(["🔍 BROAD SCOUT", "📊 TARGET RECON", "📰 SECTOR INTEL"])

with tab_scout:
    st.subheader("High-Velocity Sector Radar (All Stocks)")
    
    # Original Scoring Logic (Volume + Trend + RSI + Institutional)
    scout_results = []
    for sector, tickers in RADAR_LIST.items():
        for t in tickers:
            try:
                t_df = master_df[t].dropna()
                curr_p = t_df['Close'].iloc[-1]
                
                # 5-Point Forerunner Score
                score = 0
                score += 1 if curr_p > t_df['Close'].iloc[0] else 0 # Weekly Trend
                score += 1 if t_df['Volume'].iloc[-1] > t_df['Volume'].mean() else 0 # Vol Spike
                # Quick RSI
                delta = t_df['Close'].diff()
                rsi = 100 - (100 / (1 + (delta.where(delta > 0, 0).mean() / (delta.where(delta < 0, 0).abs().mean() + 1e-9))))
                score += 1 if rsi < 65 else 0 # Runway
                score += 2 if sector == "AI/TECH" else 1 # Sector Weighting (Original 2026 Logic)
                
                scout_results.append({
                    "Sector": sector,
                    "Ticker": t,
                    "Price": f"${curr_p:.2f}",
                    "Velocity Score": f"{score}/5",
                    "Status": "🚀 LEAD" if score >= 4 else "⏳ SCAN"
                })
            except: continue
    
    st.table(pd.DataFrame(scout_results).sort_values(by="Velocity Score", ascending=False))

with tab_recon:
    # [LIBRARY: CHART-SYNTAX-SHIELD]
    sel = st.selectbox("🎯 Target Recon", all_tickers)
    df_sel = master_df[sel].dropna()
    if not df_sel.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
