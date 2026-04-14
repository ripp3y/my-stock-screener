import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. NEURAL LINK (Top) ---
STRATEGY_LOG = {
    "AUGO": "Rebalance window (Fri/Mon). Era Dorada approved ($382M). Watch $105 floor.",
    "MRVL": "2nm AI Breakout. Record $8.2B revenue. Strong Institutional buy signal.",
    "FIX": "Strong backlog. Neutral trend. Watching for next breakout trigger."
}

# Expand the scanner's horizon
SCAN_LIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO", "NVDA", "AMD", "TSM", "AAPL", "MSFT"]

# --- 2. CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data(ttl=3600) # Cache scan for 1 hour to save battery/data
def run_scanner(tickers):
    results = []
    data = yf.download(tickers, period="2mo", group_by='ticker', progress=False)
    for t in tickers:
        try:
            df = data[t].dropna()
            cp = df['Close'].iloc[-1]
            # Technicals
            ma20 = df['Close'].rolling(20).mean().iloc[-1]
            vol_avg = df['Volume'].rolling(10).mean().iloc[-1]
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / (loss + 1e-9)
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # Screening Logic
            score = 0
            if cp > ma20: score += 1
            if df['Volume'].iloc[-1] > vol_avg: score += 1
            if 50 < rsi < 70: score += 1
            
            results.append({"Ticker": t, "Price": round(cp, 2), "RSI": round(rsi, 2), "Score": score})
        except: continue
    return pd.DataFrame(results)

# --- 3. MAIN APP ---
st.title("🛡️ Strategic Terminal")

tab_main, tab_scout = st.tabs(["🎯 Live Targets", "🔭 Market Scout"])

with tab_main:
    # (Previous Terminal Code for selected stock goes here)
    sel = st.selectbox("Select Target", SCAN_LIST)
    # ... [Insert the Technical/Risk/Intel code from v2.0 here] ...
    st.info(f"**Chat Memo:** {STRATEGY_LOG.get(sel, 'No active memo.')}")

with tab_scout:
    st.subheader("Automated Breakout Scanner")
    if st.button("🚀 Run Market Scan"):
        with st.spinner("Scanning for Institutional momentum..."):
            screen_df = run_scanner(SCAN_LIST)
            # Highlight high scores
            top_picks = screen_df[screen_df['Score'] >= 2].sort_values(by="Score", ascending=False)
            
            st.write("### Top Institutional Momentum Picks")
            for _, row in top_picks.iterrows():
                color = "#4ADE80" if row['Score'] == 3 else "#FBBF24"
                st.markdown(f"""
                    <div style="background-color: #1E293B; padding: 15px; border-radius: 10px; border-left: 8px solid {color}; margin-bottom: 10px;">
                        <span style="font-size: 20px;"><b>{row['Ticker']}</b></span> | 
                        Price: ${row['Price']} | 
                        RSI: {row['RSI']} | 
                        <b>Strength: {row['Score']}/3</b>
                    </div>
                """, unsafe_allow_html=True)
            
            if top_picks.empty:
                st.warning("No clear breakouts found. Market may be overextended.")
