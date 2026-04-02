import streamlit as st
import yfinance as yf
import pandas as pd

# --- STEP 1: DATA LOAD ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
master_data = []

for t in portfolio:
    tick = yf.Ticker(t)
    hist = tick.history(period="1mo")
    if not hist.empty:
        p = hist['Close'].values.flatten()
        abs_ret = round(((p[-1] - p[0]) / p[0]) * 100, 2)
        master_data.append({"Ticker": t, "Abs Return %": abs_ret})

df = pd.DataFrame(master_data).sort_values(by="Abs Return %", ascending=False)

# --- STEP 2: NATIVE HEATMAP (No Plotly Required) ---
st.subheader("🔥 Sector Momentum")
# Using a styled dataframe as a heatmap
st.dataframe(
    df.style.background_gradient(cmap='RdYlGn', subset=['Abs Return %']),
    use_container_width=True,
    hide_index=True
)

# --- STEP 3: NEWS SIDEBAR ---
st.sidebar.header("📰 Watchlist Intel")
for t in ["EQNR", "PBR", "CENX"]: # News for your top 3
    stories = yf.Ticker(t).news
    if stories:
        st.sidebar.write(f"**{t}**: {stories[0]['title']}")
        st.sidebar.caption(f"[Read More]({stories[0]['link']})")
