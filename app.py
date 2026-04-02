import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- 1. SETTINGS & DATA ENGINE ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
raw_data = yf.download(portfolio, period="2mo")['Close']

# --- 2. PROFIT HARVEST TOOL (SIDEBAR) ---
st.sidebar.header("💰 Profit Harvest Tool")
harvest_ticker = st.sidebar.selectbox("Select Ticker to Trim", ["EQNR", "CF"])
shares = st.sidebar.number_input(f"Shares of {harvest_ticker}", value=98)
current_p = raw_data[harvest_ticker].iloc[-1]
harvest_cash = (shares * 0.5) * current_p
st.sidebar.success(f"Harvested Cash: ${harvest_cash:,.2f}")
st.sidebar.caption(f"Based on 50% trim at ${round(current_p, 2)}")

# --- 3. RISK & MOMENTUM DISPLAY ---
st.subheader("🛡️ Portfolio Alpha Guardian")
# Correlation logic ensures a high Diversification Score
returns_df = raw_data.pct_change().dropna()
avg_corr = returns_df.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
st.write(f"### Diversification Score: {round((1-avg_corr)*100, 1)}%")

st.subheader("🔥 Sector Momentum (1mo)")
cols = st.columns(4)
grid_data = []
for i, t in enumerate(portfolio):
    ret = round(((raw_data[t].iloc[-1] - raw_data[t].iloc[0]) / raw_data[t].iloc[0]) * 100, 2)
    grid_data.append({"Ticker": t, "Return": ret, "Price": raw_data[t].iloc[-1]})
    with cols[i % 4]:
        st.metric(t, f"{ret}%", delta=ret)

# --- 4. EXECUTIVE DIRECTIVES ---
st.sidebar.divider()
st.sidebar.header("👔 Executive Directives")
for item in sorted(grid_data, key=lambda x: x['Return'], reverse=True):
    status = "🎯 TARGET HIT: Trim 50%" if item['Return'] > 45 else "✅ STRONG: Hold & Trail"
    if item['Return'] < 20: status = "⏳ WATCH: Laggard"
    st.sidebar.write(f"**{item['Ticker']}**: {status}")
