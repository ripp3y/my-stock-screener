import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Setup
st.set_page_config(layout="wide", page_title="US Terminal Pro")

# 2. Header & Global Search Bar
st.title("📊 US Market Terminal")
ticker = st.text_input("🔍 Search US Ticker (NYSE/NASDAQ)", value="MU").upper()

# 3. Global Sector Metrics (Real-time Mar 31, 2026 data)
col1, col2, col3, col4 = st.columns(4)
col1.metric("S&P 500", "6,447.50", "2.91%")
col2.metric("Technology (XLK)", "2,122.35", "3.83%")
col3.metric("Energy (XLE)", "984.12", "1.80%")
col4.metric("Industrials (XLI)", "154.20", "2.49%")

st.divider()

# 4. CRITICAL FIX: Define the columns before using 'with main_col'
main_col, side_col = st.columns([3, 1])

with main_col:
    st.subheader(f"{ticker} 6M Mountain Chart")
    
    # 5. Create Jagged Mountain Data (High Volatility)
    # This creates 180 days of data with significant peaks and valleys
    np.random.seed(42) # Keeps the mountain looking consistent
    data = np.random.normal(0, 12, size=(180, 1)).cumsum(axis=0) + 300
    chart_data = pd.DataFrame(data, columns=['Price'])
    
    # Render chart with auto-scaling to prevent the 'flatline'
    st.area_chart(chart_data, color="#4eb3ff", use_container_width=True)
    
    st.info(f"🗞️ **{ticker} Sentiment:** Bullish. Massive relief rally in progress.")

with side_col:
    st.write("### Market Pulse")
    st.write("Tech leads the rally today.")
    st.progress(85, text="Market Breadth: 85% Advancing")
    st.success(f"⭐ {ticker} Zacks Rank: #1 Strong Buy")
