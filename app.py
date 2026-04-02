import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. SIDEBAR ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_p = st.sidebar.number_input("Purchase Price", value=23.0)

# --- 2. DATA ENGINE ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
# Downloading together prevents mismatched index errors
raw_data = yf.download(portfolio, period="2mo")['Close']
returns_df = raw_data.pct_change().dropna()

# --- 3. CORRELATION MATRIX (CRASH-PROOF) ---
st.subheader("🔗 Portfolio Correlation Matrix")
if not returns_df.empty:
    corr_matrix = returns_df.corr().round(2)
    # Removed .style.background_gradient to prevent matplotlib errors
    st.dataframe(corr_matrix, use_container_width=True)
    st.info("💡 High numbers (0.7+) mean stocks move together; low numbers (below 0.3) provide safety.")

# --- 4. MOMENTUM GRID ---
st.subheader("🔥 Sector Momentum (1mo)")
cols = st.columns(4)
grid_data = []

for t in portfolio:
    if t in raw_data.columns:
        prices = raw_data[t].dropna()
        if len(prices) > 1:
            ret = round(((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100, 2)
            grid_data.append({"Ticker": t, "Return": ret})

sorted_grid = sorted(grid_data, key=lambda x: x['Return'], reverse=True)

for i, item in enumerate(sorted_grid):
    with cols[i % 4]:
        # Native metric colors don't require extra libraries
        st.metric(label=item['Ticker'], value=f"{item['Return']}%", delta=item['Return'])

# --- 5. RANKED FOOTER ---
footer_str = " | ".join([f"{i['Ticker']}: {i['Return']}%" for i in sorted_grid])
st.caption(f"📅 **Last Month Performance (Ranked):** {footer_str}")
