import streamlit as st

# --- DASHBOARD HEADER ---
st.title("🚀 Alpha Terminal: 80% Strategy")
col1, col2, col3 = st.columns(3)

# Metric 1: Forward PE
col1.metric(
    label="Forward PE", 
    value="15.1", 
    help="Valuation Check: Forecasted price-to-earnings. We look for < 20 to ensure we aren't overpaying for growth."
)

# Metric 2: Beta
col2.metric(
    label="Beta", 
    value="0.71", 
    help="The Volatility Buffer: 0.71 means the stock is 29% less volatile than the S&P 500."
)

# Metric 3: Alpha (50D)
col3.metric(
    label="Alpha (50D)", 
    value="1.3%", 
    help="Momentum Tracker: Performance vs. the 50-day moving average. We want this positive for a 'breakout' confirmation."
)

# --- SMALL FONT CAPTION ---
st.caption("⚡ Benchmarked against Energy Sector (XLE) | Last Sync: 17:34:02")
