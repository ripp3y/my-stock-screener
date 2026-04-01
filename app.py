import yfinance as yf
import streamlit as st

# 1. Create the ticker object
ticker_obj = yf.Ticker("SLB")

# 2. Fetch the info dictionary (This defines 'info')
info = ticker_obj.info 

# 3. Now the metric will work because 'info' exists
st.metric("Forward PE", f"{info.get('forwardPE', 'N/A')}")
# Get the value, default to 0 if missing, and round to 1 decimal place
f_pe = round(info.get('forwardPE', 0), 1)

# Display the polished metric
st.metric("Forward PE", f"{f_pe}")
