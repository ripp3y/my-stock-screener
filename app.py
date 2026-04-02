import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. UI SETUP ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_p = st.sidebar.number_input("Purchase Price", value=23.0)

# --- 2. STABLE DATA ENGINE ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
raw_data = yf.download(portfolio, period="2mo")['Close']
returns_df = raw_data.pct_change().dropna()

# --- 3. CORRELATION MATRIX ---
st.subheader("🔗 Portfolio Correlation Matrix")
if not returns_df.empty:
    corr_matrix = returns_df.corr().round(2)
    # Using built-in styling to avoid matplotlib/plotly errors
    st.dataframe(
        corr_matrix.style.background_gradient(cmap='RdYlGn', vmin=-1, vmax=1),
        use_container_width=True
    )

# --- 4. MOMENTUM GRID ---
st.subheader("🔥 Sector Momentum (1mo)")
cols = st.columns(4)
grid_data = []

for t in portfolio:
    if t in raw_data.columns:
        prices = raw_data[t].dropna()
        if len(prices) > 1:
            abs_ret = round(((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100, 2)
            grid_data.append({"Ticker": t, "Return": abs_ret})

sorted_grid = sorted(grid_data, key=lambda x: x['Return'], reverse=True)

for i, item in enumerate(sorted_grid):
    with cols[i % 4]:
        color = "normal" if item['Return'] > 0 else "inverse"
        st.metric(label=item['Ticker'], value=f"{item['Return']}%", delta=item['Return'], delta_color=color)

# --- 5. FIXED RANKED FOOTER ---
# Resolved the SyntaxError by ensuring the f-string brace is closed
footer_str = " | ".join([f"{i['Ticker']}: {i['Return']}%" for i in sorted_grid])
st.caption(f"📅 **Last Month Performance (Ranked):** {footer_str}")
