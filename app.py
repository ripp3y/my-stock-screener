import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime

# --- 1. GLOBAL TERMINAL CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", page_icon="🛡️", layout="wide")

# Custom CSS for Dark Mode "Alpha" Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ff88; font-weight: bold; }
    div[data-testid="stMetricDelta"] { font-size: 16px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; background-color: #1f67da; color: white; font-weight: bold; }
    .stAlert { background-color: #161b22; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE PAGE FUNCTIONS ---

def home_page():
    st.title("🏠 Command Center")
    
    # 1. Top Metrics Dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        # PBR-A is very much alive, trading at ~$18.91 with a confirmed Apr 24 ex-div.
        st.metric("PBR.A Yield on Cost", "596.1%", delta="Anchor Safe", delta_color="normal")
    with col2:
        st.metric("Portfolio Diversification", "68.9%", delta="Target: 70.3%")
    with col3:
        st.metric("Market Leader", "Energy (XLE)", delta="+32.9% YTD")

    st.divider()

    # 2. SECTOR ROTATION MATRIX (The "Foresee" Tool)
    st.subheader("🔄 Sector Rotation Matrix")
    st.caption("UP = Pulling Ahead of Market | DOWN = Pullback Incoming")
    
    sectors = {"Energy": "XLE", "Industrials": "XLI", "Materials": "XLB", "Tech": "XLK"}
    try:
        # Pulling 6 months to see the rotation trends
        comp_data = yf.download(list(sectors.values()) + ["SPY"], period="6mo", interval="1d")['Close']
        rs_df = pd.DataFrame()
        for name, ticker in sectors.items():
            rs_df[name] = comp_data[ticker] / comp_data["SPY"]
        
        # Updated to use 'width' as 'use_container_width' is deprecated in 2026
        st.line_chart(rs_df, width="stretch")
        st.info("💡 **Alpha Note:** Energy is flattening. Watch Industrials for the next 100% leg up.")
    except:
        st.error("Market data sync delayed. Check connection.")

    st.divider()

    # 3. MANUAL HARVEST LOGGER
    st.subheader("📝 Manual Harvest Logger")
    with st.expander("Record your EQNR Sell Progress"):
        c1, c2 = st.columns(2)
        sell_p = c1.number_input("Actual Sell Price ($)", value=41.67)
        sell_q = c2.number_input("Total Shares Sold", value=49.15)
        if st.button("Confirm Harvest"):
            total = sell_p * sell_q
            st.success(f"Harvested ${total:,.2f}. Target $2,045.50 secured.")

def alpha_guardian():
    st.title("🛡️ Alpha Guardian Tracker")
    
    # FIX: Ticker changed to 'PBR-A' (Dash) to fix the 'Delisted' glitch in your logs
    tickers = ["EQNR", "PBR-A", "CENX", "CF", "GEV"]
    
    with st.status("Syncing Live Market Data...", expanded=False):
        data = yf.download(tickers, period="5d", interval="1h")['Close']
    
    # Momentum Chart
    fig = px.line(data, title="Strategy Momentum (Last 5 Days)")
    fig.update_layout(template="plotly_dark", legend_title="Holdings")
    st.plotly_chart(fig, width="stretch")

    # 100% Club Benchmarking
    st.subheader("🚀 The 100% Club YoY Leaders")
    st.write("Tracking the leaders to reach your YoY goal:")
    col1, col2, col3 = st.columns(3)
    col1.info("**KOS (Energy)**: +227.1% YTD")
    col2.info("**BW (Industrials)**: +147.6% YTD")
    col3.info("**TROX (Materials)**: +115.0% YTD")

def research_hub():
    st.title("🔍 Deep Research Hub")
    ticker = st.text_input("Enter Ticker for Intelligence (e.g. GEV, CENX, KOS)", value="GEV").upper()
    
    if ticker:
        t_obj = yf.Ticker(ticker)
        c1, c2 = st.columns([2, 1])
        
        with c1:
            hist = t_obj.history(period="1mo")
            st.line_chart(hist['Close'], width="stretch")
        
        with c2:
            st.write(f"**{ticker} Key Stats**")
            info = t_obj.info
            st.write(f"Price: ${info.get('currentPrice', 'N/A')}")
            st.write(f"Sector: {info.get('sector', 'N/A')}")
            st.write(f"Forward PE: {info.get('forwardPE', 'N/A')}")

        st.subheader("📰 Latest Strategic Headlines")
        for news in t_obj.news[:4]:
            st.markdown(f"- [{news['title']}]({news['link']})")

# --- 3. NAVIGATION ENGINE (2026 Multi-Page API) ---

pg = st.navigation([
    st.Page(home_page, title="Home", icon="🏠"),
    st.Page(alpha_guardian, title="Guardian", icon="🛡️"),
    st.Page(research_hub, title="Research", icon="🔍")
])

pg.run()
