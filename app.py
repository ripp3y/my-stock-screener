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
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ff88; }
    div[data-testid="stMetricDelta"] { font-size: 16px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1f67da; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE PAGE FUNCTIONS ---

def home_page():
    st.title("🏠 Command Center")
    
    # 1. Top Metrics Dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("PBR.A Yield on Cost", "596.1%", delta="Income Anchor: SAFE")
    with col2:
        st.metric("Portfolio Diversification", "68.9%", delta="Target: 70.3%")
    with col3:
        # Energy is currently the #1 Sector YTD in April 2026
        st.metric("Sector Leader", "Energy (XLE)", delta="+32.9% YTD")

    st.divider()

    # 2. SECTOR ROTATION MATRIX (The "Foresee" Tool)
    st.subheader("🔄 Sector Rotation Matrix")
    st.caption("UP = Pulling Ahead of Market | DOWN = Pullback Incoming")
    
    # Compare your target sectors vs SPY (Market)
    sectors = {"Energy": "XLE", "Industrials": "XLI", "Materials": "XLB", "Tech": "XLK"}
    try:
        comp_data = yf.download(list(sectors.values()) + ["SPY"], period="6mo", interval="1d")['Close']
        rs_df = pd.DataFrame()
        for name, ticker in sectors.items():
            rs_df[name] = comp_data[ticker] / comp_data["SPY"]
        
        st.line_chart(rs_df)
    except:
        st.error("Market data sync delayed. Check connection.")

    st.divider()

    # 3. MANUAL HARVEST LOGGER
    st.subheader("📝 Manual Harvest Logger")
    with st.expander("Record your EQNR Sell here"):
        c1, c2 = st.columns(2)
        sell_p = c1.number_input("Actual Sell Price ($)", value=41.65)
        sell_q = c2.number_input("Total Shares Sold", value=49.15)
        if st.button("Confirm Harvest"):
            total = sell_p * sell_q
            st.success(f"Harvested ${total:,.2f}. Equity moved to 'Dry Powder' for next rotation.")

def alpha_guardian():
    st.title("🛡️ Alpha Guardian Tracker")
    
    # FIX: Using 'PBR-A' with a dash to bypass the "delisted" glitch
    tickers = ["EQNR", "PBR-A", "CENX", "CF", "GEV"]
    
    with st.status("Syncing Live Market Data...", expanded=False):
        data = yf.download(tickers, period="5d", interval="1h")['Close']
    
    # Momentum Chart
    fig = px.line(data, title="5-Day Strategy Momentum", color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(template="plotly_dark", legend_title="Holdings")
    st.plotly_chart(fig, use_container_width=True)

    # 100% Club Benchmarking
    st.subheader("🚀 2026 Leaders: The 100% Club")
    st.write("Current stocks hitting the 80-100% YoY goal:")
    col1, col2, col3 = st.columns(3)
    col1.info("**KOS (Energy)**: +227.1% YTD")
    col2.info("**BW (Industrials)**: +147.6% YTD")
    col3.info("**TROX (Materials)**: +115.0% YTD")

def research_hub():
    st.title("🔍 Deep Research Hub")
    ticker = st.text_input("Enter Ticker for News & Stats", value="GEV").upper()
    
    if ticker:
        t_obj = yf.Ticker(ticker)
        c1, c2 = st.columns([2, 1])
        
        with c1:
            hist = t_obj.history(period="1mo")
            st.line_chart(hist['Close'])
        
        with c2:
            st.write(f"**{ticker} Key Stats**")
            info = t_obj.info
            st.write(f"Sector: {info.get('sector', 'N/A')}")
            st.write(f"PE Ratio: {info.get('trailingPE', 'N/A')}")
            st.write(f"Div Yield: {info.get('dividendYield', 0)*100:.2f}%")

        st.subheader("📰 Latest Headlines")
        for news in t_obj.news[:4]:
            st.markdown(f"- [{news['title']}]({news['link']})")

# --- 3. NAVIGATION ENGINE (Streamlit 2026 API) ---

pg = st.navigation([
    st.Page(home_page, title="Home", icon="🏠"),
    st.Page(alpha_guardian, title="Guardian", icon="🛡️"),
    st.Page(research_hub, title="Research", icon="🔍")
])

pg.run()
