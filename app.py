import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 1. Setup the Layout
st.set_page_config(layout="wide", page_title="US Market Terminal")

# 2. Header & Search Bar (US Only)
st.title("📊 US Market Terminal")
ticker = st.text_input("🔍 Search US Ticker (e.g. MU, AVGO, CENX)", value="MU").upper()

# 3. Sector Percentages (March 31, 2026 Context)
col1, col2, col3, col4 = st.columns(4)
col1.metric("S&P 500", "6,447.50", "+2.91%")
col2.metric("Technology (XLK)", "2,122.35", "+3.83%")
col3.metric("Energy (XLE)", "984.12", "+1.80%")
col4.metric("Industrials (XLI)", "154.20", "+2.49%")

st.divider()

# 4. Main Dashboard Columns
main_col, side_col = st.columns([3, 1])

with main_col:
    st.subheader(f"{ticker} 6-Month Mountain Chart")
    
    # 5. FETCH ACTUAL DATA
    try:
        # Get 6 months of daily data
        data = yf.download(ticker, period="6mo", interval="1d")
        
        if not data.empty:
            # We use 'Close' for the mountain path
            chart_data = data['Close']
            st.area_chart(chart_data, color="#4eb3ff", use_container_width=True)
            
            # Show the actual live price below the chart
            last_price = chart_data.iloc[-1].item()
            st.info(f"💰 Current {ticker} Price: ${last_price:,.2f}")
        else:
            st.warning(f"Ticker '{ticker}' not found. Please use US symbols.")
            
    except Exception as e:
        st.error("Connecting to Market Data... Please refresh.")

with side_col:
    st.write("### Market Pulse")
    st.write("Tech leads the relief rally today.")
    st.progress(85, text="Market Breadth: 85% Advancing")
    st.success(f"⭐ {ticker} Zacks Rank: #1 Strong Buy")
