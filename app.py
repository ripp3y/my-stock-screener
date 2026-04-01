import yfinance as yf
import streamlit as st

# 1. Create the ticker object
ticker_obj = yf.Ticker("SLB")

# 2. Fetch the info dictionary (This defines 'info')
info = ticker_obj.info 

# 3. Now the metric will work because 'info' exists
st.metric("Forward PE", f"{info.get('forwardPE', 'N/A')}")
