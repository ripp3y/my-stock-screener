import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- 1. SETTINGS & SIDEBAR ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")
st.sidebar.header("🎯 Target Alpha Engine")
buy_p = st.sidebar.number_input("Purchase Price", value=23.0)

# --- 2. DATA ENGINE ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
# Downloading all at once prevents index mismatched ValueErrors
raw_data = yf.download(portfolio, period="2mo")['Close']
returns_df = raw_data.pct_change().dropna()

# --- 3. RISK GUARDIAN ---
if not returns_df.empty:
    corr_matrix = returns_df.corr()
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    avg_corr = upper_tri.stack().mean()
    div_score = round((1 - avg_corr) * 100, 1)
    
    st.subheader("🛡️ Portfolio Alpha Guardian")
    st.caption(f"**Current Status:** Moderate (Avg Correlation: {round(avg_corr, 2)})")
    
    with st.expander("🔗 View Correlation Matrix"):
        # Displaying raw matrix to avoid matplotlib dependencies
        st.dataframe(corr_matrix.round(2), use_container_width=True)

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
        st.metric(label=item['Ticker'], value=f"{item['Return']}%", delta=item['Return'])

# --- 5. EXECUTIVE DIRECTIVES (SIDEBAR) ---
st.sidebar.divider()
st.sidebar.header("👔 Executive Directives")

for item in sorted_grid:
    ticker, ret = item['Ticker'], item['Return']
    
    if ret > 45: # Adjusted for your high-flyers
        icon, note = "🎯", "TARGET HIT: Trim 50%"
    elif ret > 20:
        icon, note = "✅", "STRONG: Hold & Trail"
    elif ret < 10:
        icon, note = "📈", "TRENDING: Neutral"
    else:
        icon, note = "⏳", "WATCH: Laggard"
        
    st.sidebar.write(f"**{ticker}**: {icon} {note}")

# --- 6. RANKED ALPHA FOOTER ---
footer_str = " | ".join([f"{i['Ticker']}: {i['Return']}%" for i in sorted_grid])
st.caption(f"📅 **Ranked Alpha:** {footer_str}")
