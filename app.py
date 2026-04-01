import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 1. Setup the Layout
st.set_page_config(layout="wide", page_title="PRO US TERMINAL")

# 2. CACHING: This prevents the YFRateLimitError
@st.cache_data(ttl=300) # Data stays in memory for 300 seconds (5 mins)
def get_market_data(ticker):
    stock = yf.Ticker(ticker)
    # Fetch 6 months of historical data
    hist = stock.history(period="6mo")
    # Fetch basic info for metrics
    info = stock.info
    return hist, info

# 3. Header & Search
st.title("📊 Strategic US Terminal")
ticker_input = st.text_input("🔍 Command Center: Enter US Ticker", value="MU").upper()

# 4. Indices Metrics (Mar 31, 2026 Context)
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("S&P 500", "6,528.52", "+2.91%")
m_col2.metric("NASDAQ", "21,590.63", "+3.83%")
m_col3.metric("DOW", "46,341.51", "+2.49%")
m_col4.metric("VIX", "25.25", "-17.51%")

st.divider()

# 5. Main Analysis Engine
main_col, side_col = st.columns([3, 1])

with main_col:
    st.subheader(f"{ticker_input} 6M Mountain Chart")
    
    try:
        hist, info = get_market_data(ticker_input)
        
        if not hist.empty:
            # CLEAN DATA: Ensure the index is just dates and prices are floats
            chart_data = hist[['Close']].copy()
            chart_data.index = chart_data.index.date
            
            # Render the 'Mountain'
            st.area_chart(chart_data, color="#4eb3ff", use_container_width=True)
            
            # Live Price Info
            current_price = chart_data['Close'].iloc[-1]
            st.info(f"💡 {ticker_input} Closing Price: ${current_price:,.2f}")
        else:
            st.error("No historical data found. check ticker symbol.")
            
    except Exception as e:
        st.warning("Rate limit or connection issue. The cache will retry shortly.")

with side_col:
    st.write("### Fundamental Health")
    if 'info' in locals() and info:
        # Using .get() prevents crashes if a specific metric is missing
        st.metric("PE Ratio (Forward)", f"{info.get('forwardPE', 'N/A')}")
        st.metric("Profit Margin", f"{info.get('profitMargins', 0)*100:.2f}%")
        st.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
    
    st.divider()
    st.write("### Market Pulse")
    st.success("🔥 Leading: Tech (XLK) +3.8%")
    st.progress(85, text="Market Breadth: 85% Advancing")
