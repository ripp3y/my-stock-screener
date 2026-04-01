import streamlit as st

# --- STYLED METRICS WITH TOOLTIPS ---
st.title("🛡️ Alpha Terminal: Pro View")
col1, col2, col3 = st.columns(3)

# Metric 1: Forward PE
col1.metric(
    label="Forward PE", 
    value="15.1", 
    help="Price-to-Earnings ratio based on forecasted earnings. Lower = Better Value."
)

# Metric 2: Beta
col2.metric(
    label="Beta", 
    value="0.71", 
    help="Market Sensitivity. 0.71 means the stock is 29% less volatile than the S&P 500."
)

# Metric 3: Alpha (50D)
col3.metric(
    label="Alpha (50D)", 
    value="1.3%", 
    help="Relative performance against the 50-day moving average. Positive = Upward Momentum."
)

# --- SMALL FONT SUB-DESCRIPTION ---
st.caption("Values updated as of 21:03:29. Benchmarked against XLE.")
