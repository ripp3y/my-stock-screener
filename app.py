import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG & GLOBAL MEMORY ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")
# UPDATE THIS BLOCK IN YOUR v2.0 SCRIPT
STRATEGY_LOG = {
    "AUGO": "Rebalance window (Fri/Mon). Era Dorada approved ($382M). Watch $105 floor.",
    "MRVL": "2nm AI Breakout. Record $8.2B revenue. Strong Institutional buy signal.",
    "FIX": "Strong backlog. Neutral trend. Watching for next breakout trigger."
}

# This acts as our "Neural Link" - Put our latest chat strategy here
STRATEGY_LOG = {
    "AUGO": "Forced-buy window active (Fri/Mon). RSI 89 (Extreme). Watch $105 floor.",
    "MRVL": "2nm AI Breakout confirmed. RSI 79. Riding with Vanguard/BlackRock.",
    "FIX": "Backlog play ($12B). Neutral Trending. Z-Score Reset."
}

WATCHLIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO"]

@st.cache_data(ttl=600)
def fetch_prices(ticker_list):
    try: return yf.download(list(ticker_list), period="2y", group_by='ticker').ffill()
    except: return None

# --- 2. SIDEBAR COMMAND CENTER (The Bridge) ---
with st.sidebar:
    st.title("🎚️ Neural Link")
    st.info("Everything discussed in Finviz/Chat is logged here for the Terminal to 'hear'.")
    
    st.subheader("Latest Strategic Orders")
    for ticker, note in STRATEGY_LOG.items():
        with st.expander(f"Order: {ticker}"):
            st.write(note)
    
    st.divider()
    st.write("✅ System Synced: April 14, 2026")

# --- 3. MAIN TERMINAL ---
all_data = fetch_prices(WATCHLIST)

if all_data is not None:
    sel = st.selectbox("Select Target", WATCHLIST)
    df_sel = all_data[sel].dropna()
    
    # RSI & Status Logic
    delta = df_sel['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    current_rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    if current_rsi > 70: status, s_color = "OVERBOUGHT", "#F87171"
    elif current_rsi < 30: status, s_color = "OVERSOLD", "#4ADE80"
    else: status, s_color = "NEUTRAL", "#93C5FD"

    st.markdown(f"### {sel} Status: <span style='color:{s_color}'>{status}</span>", unsafe_allow_html=True)
    
    # Show active Strategy Note right at the top
    if sel in STRATEGY_LOG:
        st.warning(f"**Chat Memo:** {STRATEGY_LOG[sel]}")

    t1, t2 = st.tabs(["📊 Technicals", "🛡️ Risk Scout"])

    with t1:
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        cp, atr = df_sel['Close'].iloc[-1], (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # Risk Box
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 12px; border-left: 10px solid {s_color};">
                <p style="color: #DBEAFE; font-size: 26px; margin: 0;"><b>Live Target</b></p>
                <p style="color: #93C5FD; font-size: 18px; margin: 5px 0;">Stop Loss: <b>${t_stop:.2f}</b></p>
                <p style="color: #BFDBFE; font-size: 14px; margin: 0;">RSI: {current_rsi:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("📡 Sync Issue.")
