import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
raw_data = yf.download(portfolio, period="2mo")['Close']

# --- 2. YIELD & HARVEST ENGINE (SIDEBAR) ---
st.sidebar.header("📊 Yield & Harvest Engine")
selected = st.sidebar.selectbox("Select Asset", portfolio, index=0)
cost_basis = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)

# Real-time Dividend & YOC Logic
t_obj = yf.Ticker(selected)
div_y = t_obj.info.get('dividendYield', 0)
if div_y:
    ann_div = div_y * raw_data[selected].iloc[-1]
    yoc = (ann_div / cost_basis) * 100
    st.sidebar.metric("Yield on Cost", f"{round(yoc, 2)}%")

st.sidebar.divider()
st.sidebar.header("💰 Profit Harvest Tool")
h_ticker = st.sidebar.selectbox("Trim Target", ["EQNR", "CF"])
h_shares = st.sidebar.number_input(f"Shares of {h_ticker}", value=98)
h_cash = (h_shares * 0.5) * raw_data[h_ticker].iloc[-1]
st.sidebar.success(f"Harvested Cash: ${h_cash:,.2f}")

# --- 3. RISK & SECTOR VISUALIZATION ---
st.header("🛡️ Portfolio Alpha Guardian")
col_a, col_b = st.columns([1, 1])

with col_a:
    rets = raw_data.pct_change().dropna()
    avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
    # High-Resolution Risk Tracking
    st.write(f"## Diversification Score: {round((1-avg_corr)*100, 1)}%")

with col_b:
    # Sector Weighting Mapping
    sectors = {"Energy": ["PBR", "EQNR", "CNQ", "XOM", "CVX"], 
               "Materials": ["CENX", "CF"], 
               "Industrials": ["GEV"]}
    weight_data = pd.DataFrame([{"Sector": s, "Weight": len(t)} for s, t in sectors.items()])
    fig = px.pie(weight_data, values='Weight', names='Sector', hole=.4, height=350)
    st.plotly_chart(fig, use_container_width=True)
