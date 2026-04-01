import streamlit as st
import yfinance as yf

# 1. Define a cached function to fetch data
@st.cache_data(ttl=600)  # Cache for 600 seconds (10 minutes)
def get_stock_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.info

# 2. Use the cached function
info = get_stock_data("SLB")

if info:
    col1, col2 = st.columns(2)
    
    # Render PE
    f_pe = round(info.get('forwardPE', 0), 1)
    col1.metric("Forward PE", f"{f_pe}")
    
    # Render Yield (with decimal correction)
    raw_yield = info.get('dividendYield', 0)
    if raw_yield:
        col2.metric("Div Yield", f"{round(raw_yield * 100, 2)}%")
    else:
        col2.metric("Div Yield", "0.0%")
