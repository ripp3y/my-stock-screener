import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime

# --- 1. GLOBAL CONFIG & STYLE ---
st.set_page_config(page_title="Strategic US Terminal", page_icon="🛡️", layout="wide")

# Custom CSS for that "Alpha" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE PAGES (Functions) ---

def home_page():
    st.title("🏠 Command Center")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("PBR.A Yield on Cost", "596.1%", delta="Anchor Safe", delta_color="normal")
    with col2:
        st.metric("Diversification", "68.9%", delta="Target: 70.3%")
    with col3:
        st.metric("Next Ex-Div", "Apr 23", delta="PBR.A")

    st.divider()
    
    # Manual Sell Logger
    st.subheader("📝 Manual Harvest Logger")
    with st.expander("Log a Sell (EQNR)"):
        sell_price = st.number_input("Enter EQNR Sell Price ($)", value=41.60)
        sell_qty = st.number_input("Shares Sold", value=48.99)
        if st.button("Calculate Harvest Impact"):
            total_cash = sell_price * sell_qty
            st.success(f"Harvest Value: ${total_cash:,.2f}. This move pushes Diversification closer to 70.3%.")

def alpha_guardian():
    st.title("🛡️ Alpha Guardian Tracker")
    st.info("Syncing live market momentum for Energy, Materials, and Industrials.")
    
    # Re-using your successful tracking logic
    tickers = ["EQNR", "PBR.A", "CENX", "CF", "GEV"]
    data = yf.download(tickers, period="5d", interval="1h")['Close']
    
    fig = px.line(data, title="Sector Momentum (5-Day Horizon)")
    st.plotly_chart(fig, on_select="ignore")
    
    st.subheader("🎯 Profit Harvest Calculation")
    st.write("Target: **$2,045.50** from EQNR")
    eqnr_price = data['EQNR'].iloc[-1]
    shares_needed = 2045.50 / eqnr_price
    st.warning(f"At current price (${eqnr_price:.2f}), sell **{shares_needed:.2f}** shares of EQNR.")

# --- 3. NAVIGATION ROUTER ---

# Define the pages using the 2026 Navigation API
pg = st.navigation([
    st.Page(home_page, title="Home", icon="🏠"),
    st.Page(alpha_guardian, title="Alpha Guardian", icon="🛡️")
])

# Run the selected page
pg.run()
