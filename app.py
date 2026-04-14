import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. NEURAL LINK (Strategic Data) ---
# Update this board whenever we get new board-level or insider intel
INTEL_BOARD = {
    "AUGO": "Board approved $382M Era Dorada project (4.13.26). Projected 111k oz gold/yr (2028). Floor: $105.",
    "FIX": "Record $12B backlog. 45% revenue now tech/AI-infrastructure based. Backlog tripled vs LY.",
    "MRVL": "2nm AI Breakthrough. Electra/Libra DSPs shipping to AI clusters. Institutional conviction: 96%.",
    "MSFT": "Sustained Azure/AI growth. Institutional Goldilocks zone. RSI trending perfectly.",
    "TSM": "2nm node ramping up for 2026 delivery. Massive demand from NVDA/AAPL clusters."
}

SCAN_LIST = list(INTEL_BOARD.keys())

# --- 2. CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

# --- 3. THE ENGINE ---
@st.cache_data(ttl=600)
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="1y", group_by='ticker', progress=False).ffill()
    except: return None

def calculate_rsi(data):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v3.0")
master_data = fetch_prices(SCAN_LIST)

if master_data is not None:
    sel = st.selectbox("🎯 Select Target Recon", SCAN_LIST)
    df_sel = master_data[sel].dropna()
    rsi_val = calculate_rsi(df_sel['Close']).iloc[-1]
    
    # --- DYNAMIC INTEL BOARD (The 'Share Line') ---
    # This box now automatically pulls info from INTEL_BOARD based on your selection
    intel_text = INTEL_BOARD.get(sel, "Gathering active board intel...")
    
    st.markdown(f"""
        <div style="background-color: #1e3a8a; padding: 15px; border-radius: 10px; border-left: 10px solid #3b82f6; margin-bottom: 20px;">
            <p style="color: #93c5fd; font-size: 14px; margin: 0;"><b>STRATEGIC INTEL BOARD: {sel}</b></p>
            <p style="color: white; font-size: 16px; margin: 5px 0;">{intel_text}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- CHART SECTION ---
    tab1, tab2 = st.tabs(["📊 Charts", "🛡️ Risk"])
    
    with tab1:
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # Combined RSI + Alert Line
        col_rsi, col_alert = st.columns([1, 2])
        col_rsi.metric("RSI", f"{rsi_val:.2f}")
        
        # Dynamic Alert Logic
        if rsi_val > 80: a_msg, a_bg = "🔥 EXTREME MOMENTUM: Watch stops.", "#7f1d1d"
        elif rsi_val > 70: a_msg, a_bg = "⚠️ OVERBOUGHT: Forced-buy peak.", "#991b1b"
        elif rsi_val > 55: a_msg, a_bg = "🚀 BULLISH: Strong support.", "#1e3a8a"
        else: a_msg, a_bg = "⚖️ NEUTRAL: Consolidating.", "#1f2937"
        
        col_alert.markdown(f'<div style="background-color: {a_bg}; padding: 10px; border-radius: 8px; text-align: center; color: white;"><b>{a_msg}</b></div>', unsafe_allow_html=True)
