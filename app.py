import streamlit as st
import yfinance as yf
import pandas as pd

# 1. SIDEBAR CONFIG
st.sidebar.header("🎯 Target Alpha Engine")
buy_p = st.sidebar.number_input("Purchase Price", value=23.0)

# 2. DATA LOAD (Simplified for stability)
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
master_data = []

for t in portfolio:
    d = yf.download(t, period="1mo")
    if not d.empty:
        p = d['Close'].values.flatten()
        abs_ret = ((p[-1] - p[0]) / p[0]) * 100
        master_data.append({"Ticker": t, "Abs Return %": round(abs_ret, 2)})

# 3. FORCE DISPLAY (This removes the "Code" screen)
st.subheader("🏆 Strategic Alpha Leaderboard")
df = pd.DataFrame(master_data).sort_values(by="Abs Return %", ascending=False)

# This command specifically replaces the "st module" text with your data
st.dataframe(df, use_container_width=True) 

# FOOTER
st.caption(f"📅 Last Month Performance: Sorted Best to Least")
