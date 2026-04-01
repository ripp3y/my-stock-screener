import streamlit as st
import yfinance as yf

# 1. Initialize the layout first
st.title("Alpha Terminal")
col1, col2 = st.columns(2)

# 2. Fetch the data
ticker_obj = yf.Ticker("SLB")
info = ticker_obj.info

# 3. Render Metric 1: Forward PE
f_pe = round(info.get('forwardPE', 0), 1)
col1.metric("Forward PE", f"{f_pe}")

# 4. Render Metric 2: Div Yield
div_yield = info.get('dividendYield', 0)
if div_yield:
    formatted_yield = f"{round(div_yield * 100, 2)}%"
else:
    formatted_yield = "0.0%"
col2.metric("Div Yield", formatted_yield)

# 5. Render the Chart
# (Assuming your chart data logic follows here)
