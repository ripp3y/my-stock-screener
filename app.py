import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- 1. CORE SETUP & DATA ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Energy/Industrial Portfolio
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
data = yf.download(portfolio, period="2mo")['Close']

# --- 2. YIELD ON COST TRACKER ---
st.sidebar.header("📊 Yield & Harvest Engine")
selected_ticker = st.sidebar.selectbox("Select Asset", portfolio)
my_cost_basis = st.sidebar.number_input(f"Avg Cost for {selected_ticker}", value=25.0)

# Fetch annual dividend data
ticker_obj = yf.Ticker(selected_ticker)
div_yield = ticker_obj.info.get('dividendYield', 0)
if div_yield:
    annual_div = div_yield * data[selected_ticker].iloc[-1]
    yoc = (annual_div / my_cost_basis) * 100
    st.sidebar.metric("Yield on Cost", f"{round(yoc, 2)}%")
else:
    st.sidebar.caption("No dividend data found for this asset.")

# --- 3. PROFIT HARVEST TOOL ---
st.sidebar.divider()
st.sidebar.header("💰 Profit Harvest Tool")
harvest_ticker = st.sidebar.selectbox("Trim Target", ["EQNR", "CF"])
shares = st.sidebar.number_input(f"Shares of {harvest_ticker}", value=98)
current_price = data[harvest_ticker].iloc[-1]
harvest_cash = (shares * 0.5) * current_price

st.sidebar.success(f"Harvested Cash: ${harvest_cash:,.2f}")
st.sidebar.caption(f"Trim Price: ${round(current_price, 2)}")

# --- 4. ALPHA GUARDIAN & MOMENTUM ---
st.subheader("🛡️ Portfolio Alpha Guardian")
returns = data.pct_change().dropna()
avg_corr = returns.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
st.write(f"### Diversification Score: {round((1-avg_corr)*100, 1)}%")

st.subheader("🔥 Sector Momentum (1mo)")
cols = st.columns(4)
for i, t in enumerate(portfolio):
    m_ret = round(((data[t].iloc[-1] - data[t].iloc[0]) / data[t].iloc[0]) * 100, 2)
    with cols[i % 4]:
        st.metric(t, f"{m_ret}%", delta=m_ret)

# --- 5. EXECUTIVE DIRECTIVES ---
st.sidebar.divider()
st.sidebar.header("👔 Executive Directives")
for t in portfolio:
    ret = round(((data[t].iloc[-1] - data[t].iloc[0]) / data[t].iloc[0]) * 100, 2)
    if ret > 45:
        st.sidebar.write(f"**{t}**: 🎯 TARGET HIT: Trim 50%")
    elif ret < 20:
        st.sidebar.write(f"**{t}**: ⏳ WATCH: Laggard")
