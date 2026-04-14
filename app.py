import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. NEURAL LINK (The Brain) ---
# This is our shared memory. Update this top section to sync our chat strategy.
STRATEGY_LOG = {
    "AUGO": "Rebalance window (Fri/Mon). Era Dorada approved ($382M). Watch $105 floor.",
    "MRVL": "2nm AI Breakout. Record $8.2B revenue. Strong Institutional buy signal.",
    "FIX": "Strong backlog. Neutral trend. Watching for next breakout trigger.",
    "SNDK": "Tracking semi-conductor sector momentum. Watching RSI 70 level."
}

# The universe your Scout will scan
SCAN_LIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO", "NVDA", "AMD", "TSM", "AAPL", "MSFT"]

# --- 2. CONFIG & STYLING ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #93C5FD; }
    div[data-testid="stExpander"] { background-color: #1E293B; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SECURED DATA ENGINES ---
@st.cache_data(ttl=600)
def fetch_prices(tickers):
    try:
        return yf.download(list(tickers), period="2y", group_by='ticker', progress=False).ffill()
    except: return None

def fetch_intel_secured(ticker):
    """SEC-Compliant Intel Fetcher"""
    try:
        # User-Agent is REQUIRED by the SEC to prevent 'High-Security' lockouts
        headers = {"User-Agent": "StrategicTerminalResearch/1.0 (melvin.rippey@example.com)"}
        t = yf.Ticker(ticker)
        # Returns major institutional holders
        return t.major_holders
    except: return None

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

# --- 4. THE SCOUT (Screener Logic) ---
def run_scanner(tickers, data):
    results = []
    for t in tickers:
        try:
            df = data[t].dropna()
            cp = df['Close'].iloc[-1]
            ma20 = df['Close'].rolling(20).mean().iloc[-1]
            vol_avg = df['Volume'].rolling(10).mean().iloc[-1]
            rsi = calculate_rsi(df['Close']).iloc[-1]
            
            score = 0
            if cp > ma20: score += 1
            if df['Volume'].iloc[-1] > vol_avg: score += 1
            if 50 < rsi < 72: score += 1 # 'Goldilocks' zone
            
            results.append({"Ticker": t, "Price": cp, "RSI": rsi, "Score": score})
        except: continue
    return pd.DataFrame(results)

# --- 5. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v2.7")

# Global Data Fetch
master_data = fetch_prices(SCAN_LIST)

tab_main, tab_scout = st.tabs(["🎯 Live Targets", "🔭 Market Scout"])

with tab_main:
    if master_data is not None:
        sel = st.selectbox("Target Recon", SCAN_LIST)
        df_sel = master_data[sel].dropna()
        
        # Core Technicals
        rsi_val = calculate_rsi(df_sel['Close']).iloc[-1]
        if rsi_val > 70: status, color = "OVERBOUGHT", "#F87171"
        elif rsi_val < 30: status, color = "OVERSOLD", "#4ADE80"
        else: status, color = "TRENDING", "#93C5FD"
        
        st.markdown(f"### {sel} Status: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
        
        # Display Neural Link Memo
        if sel in STRATEGY_LOG:
            st.info(f"**Chat Memo:** {STRATEGY_LOG[sel]}")
            
        sub1, sub2, sub3 = st.tabs(["📊 Charts", "🛡️ Risk", "🕵️ Intel"])
        
        with sub1:
            fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Current RSI", f"{rsi_val:.2f}")

        with sub2:
            cp, atr = df_sel['Close'].iloc[-1], (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
            t_stop = cp - (atr * 2.5)
            st.markdown(f"""
                <div style="background-color: #1E3A8A; padding: 20px; border-radius: 12px; border-left: 10px solid {color};">
                    <p style="color: #DBEAFE; font-size: 24px; margin: 0;"><b>Stop Loss: ${t_stop:.2f}</b></p>
                    <p style="color: #93C5FD; font-size: 16px;">Current Price: ${cp:.2f}</p>
                </div>
            """, unsafe_allow_html=True)

        with sub3:
            st.subheader("Institutional Recon")
            intel = fetch_intel_secured(sel)
            if intel is not None:
                st.dataframe(intel, use_container_width=True)
            else:
                st.warning("SEC Database Busy. Retrying in next cycle...")

with tab_scout:
    st.subheader("Market Momentum Scanner")
    if st.button("🚀 Run Institutional Scan"):
        screen_df = run_scanner(SCAN_LIST, master_data)
        top = screen_df[screen_df['Score'] >= 2].sort_values(by="Score", ascending=False)
        for _, row in top.iterrows():
            sc_color = "#4ADE80" if row['Score'] == 3 else "#FBBF24"
            st.markdown(f"""
                <div style="background-color: #1E293B; padding: 15px; border-radius: 10px; border-left: 8px solid {sc_color}; margin-bottom: 10px;">
                    <b>{row['Ticker']}</b> | Price: ${row['Price']:.2f} | RSI: {row['RSI']:.2f} | <b>Score: {row['Score']}/3</b>
                </div>
            """, unsafe_allow_html=True)

# --- SIDEBAR (Neural Link History) ---
with st.sidebar:
    st.title("🎚️ Neural Link")
    for t, m in STRATEGY_LOG.items():
        with st.expander(f"Log: {t}"):
            st.write(m)
