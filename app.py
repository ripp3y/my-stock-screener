import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. NEURAL LINK ---
STRATEGY_LOG = {
    "AUGO": "Rebalance window (Fri/Mon). Era Dorada approved ($382M). Watch $105 floor.",
    "MRVL": "2nm AI Breakout. Record $8.2B revenue. Strong Institutional buy signal.",
    "FIX": "Strong backlog. Neutral trend. Watching for next breakout trigger.",
    "SNDK": "Tracking semi-conductor sector momentum. Watching RSI 70 level."
}

SCAN_LIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO", "NVDA", "AMD", "TSM", "AAPL", "MSFT"]

# --- 2. CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

# Mobile UI Cleanup
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { font-size: 22px; color: #93C5FD; }
    div[data-testid="stExpander"] { background-color: #1E293B; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINES ---
@st.cache_data(ttl=600)
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="2y", group_by='ticker', progress=False).ffill()
    except: return None

def fetch_intel_secured(ticker):
    try:
        headers = {"User-Agent": "StrategicTerminalResearch/1.0 (melvin.rippey@example.com)"}
        t = yf.Ticker(ticker)
        return t.major_holders
    except: return None

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v2.9")
master_data = fetch_prices(SCAN_LIST)

tab_main, tab_scout = st.tabs(["🎯 Live Targets", "🔭 Market Scout"])

with tab_main:
    if master_data is not None:
        sel = st.selectbox("Target Recon", SCAN_LIST)
        df_sel = master_data[sel].dropna()
        rsi_val = calculate_rsi(df_sel['Close']).iloc[-1]
        
        if sel in STRATEGY_LOG:
            st.info(f"**Chat Memo:** {STRATEGY_LOG[sel]}")
            
        sub1, sub2, sub3 = st.tabs(["📊 Charts", "🛡️ Risk", "🕵️ Intel"])
        
        with sub1:
            fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
            
            # --- STRATEGY ALERT SECTION (FIXED QUOTES) ---
            col_rsi, col_alert = st.columns([1, 2])
            with col_rsi:
                st.metric("RSI", f"{rsi_val:.2f}")
            with col_alert:
                if rsi_val > 80:
                    a_msg, a_bg = "🔥 EXTREME MOMENTUM: Tighten stops.", "#7f1d1d"
                elif rsi_val > 70:
                    a_msg, a_bg = "⚠️ OVERBOUGHT: Forced-buying peaking.", "#991b1b"
                elif rsi_val > 55:
                    a_msg, a_bg = "🚀 BULLISH TREND: Strong support.", "#1e3a8a"
                elif rsi_val < 30:
                    a_msg, a_bg = "💎 OVERSOLD: Watch for buy point.", "#064e3b"
                else:
                    a_msg, a_bg = "⚖️ NEUTRAL: Consolidating.", "#1f2937"

                # Wrapped in triple quotes for safety
                st.markdown(f"""
                    <div style="background-color: {a_bg}; padding: 10px; border-radius: 8px; text-align: center; color: white; font-size: 13px;">
                        <b>{a_msg}</b>
                    </div>
                    """, unsafe_allow_html=True)

        with sub2:
            cp, atr = df_sel['Close'].iloc[-1], (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
            t_stop = cp - (atr * 2.5)
            st.success(f"**Active Stop Loss: ${t_stop:.2f}**")

        with sub3:
            st.subheader("Institutional Recon")
            intel = fetch_intel_secured(sel)
            if intel is not None: st.dataframe(intel, use_container_width=True)
            else: st.warning("SEC Database Busy.")

with tab_scout:
    st.subheader("Momentum Scout")
    if st.button("🚀 Run Institutional Scan"):
        results = []
        for t in SCAN_LIST:
            try:
                df = master_data[t].dropna()
                rsi = calculate_rsi(df['Close']).iloc[-1]
                score = 0
                if df['Close'].iloc[-1] > df['Close'].rolling(20).mean().iloc[-1]: score += 1
                if df['Volume'].iloc[-1] > df['Volume'].rolling(10).mean().iloc[-1]: score += 1
                if 50 < rsi < 72: score += 1
                results.append({"Ticker": t, "Price": df['Close'].iloc[-1], "Score": score})
            except: continue
        
        top = pd.DataFrame(results).sort_values(by="Score", ascending=False)
        for _, row in top[top['Score'] >= 2].iterrows():
            st.markdown(f"**{row['Ticker']}** | Price: ${row['Price']:.2f} | Strength: {row['Score']}/3")
