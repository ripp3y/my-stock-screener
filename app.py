import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- 1. CORE INTERFACE & SETTINGS ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")
st.sidebar.header("🎯 Target Alpha Engine")
# Global purchase target for your energy/industrial pivot
buy_p = st.sidebar.number_input("Global Purchase Price", value=23.0)

# --- 2. DATA ENGINE ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
raw_data = yf.download(portfolio, period="2mo")['Close']
returns_df = raw_data.pct_change().dropna()

# --- 3. RISK GUARDIAN ---
if not returns_df.empty:
    corr_matrix = returns_df.corr()
    avg_corr = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)).stack().mean()
    div_score = round((1 - avg_corr) * 100, 1)
    
    st.subheader("🛡️ Portfolio Alpha Guardian")
    st.write(f"### Diversification Score: {div_score}%")
    st.caption(f"**Current Status:** Moderate (Avg Correlation: {round(avg_corr, 2)})")

# --- 4. MOMENTUM GRID ---
st.subheader("🔥 Sector Momentum (1mo)")
cols = st.columns(4)
grid_data = []

for t in portfolio:
    if t in raw_data.columns:
        prices = raw_data[t].dropna()
        if len(prices) > 1:
            ret = round(((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100, 2)
            grid_data.append({"Ticker": t, "Return": ret, "Price": prices.iloc[-1]})

sorted_grid = sorted(grid_data, key=lambda x: x['Return'], reverse=True)

for i, item in enumerate(sorted_grid):
    with cols[i % 4]:
        st.metric(label=item['Ticker'], value=f"{item['Return']}%", delta=item['Return'])

# --- 5. PROFIT HARVEST TOOL ---
st.sidebar.divider()
st.sidebar.header("💰 Profit Harvest Tool")
# Dynamically selecting from your current top performers
harvest_ticker = st.sidebar.selectbox("Select Ticker to Trim", ["EQNR", "CF"])
shares = st.sidebar.number_input(f"Shares of {harvest_ticker}", value=100)

current_p = raw_data[harvest_ticker].iloc[-1]
harvest_cash = (shares * 0.5) * current_p
st.sidebar.success(f"Harvested Cash: ${harvest_cash:,.2f}")
st.sidebar.caption(f"Based on 50% trim at ${round(current_p, 2)}")

# --- 6. EXECUTIVE DIRECTIVES (Fixed Syntax) ---
st.sidebar.divider()
st.sidebar.header("👔 Executive Directives")
for item in sorted_grid:
    ticker, ret = item['Ticker'], item['Return']
    if ret > 45:
        st.sidebar.write(f"**{ticker}**: 🎯 TARGET HIT: Trim 50%")
    elif ret > 20:
        st.sidebar.write(f"**{ticker}**: ✅ STRONG: Hold & Trail")
    else:
        st.sidebar.write(f"**{ticker}**: ⏳ WATCH: Laggard")

# --- 7. TACTICAL BUY ZONES ---
st.sidebar.divider()
st.sidebar.header("🛒 Tactical Buy Zones")
for item in sorted_grid:
    if item['Return'] < 20:
        st.sidebar.warning(f"**{item['Ticker']}**: Accumulation Zone")
        # Direct calculation of rotation power
        can_buy = int(harvest_cash / item['Price'])
        st.sidebar.caption(f"Rotate cash into ~{can_buy} shares of {item['Ticker']}")
