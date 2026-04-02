import streamlit as st
import yfinance as yf
import pandas as pd

# --- STEP 1: SIDEBAR ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_p = st.sidebar.number_input("Purchase Price", value=23.0)

# --- STEP 2: DATA & ALPHA ENGINE ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
master_data = []

for t in portfolio:
    tick = yf.Ticker(t)
    hist = tick.history(period="1mo")
    if not hist.empty:
        # Flattening to prevent ValueErrors
        p = hist['Close'].values.flatten()
        abs_ret = round(((p[-1] - p[0]) / p[0]) * 100, 2)
        
        # Color Logic for Metrics (Simulated Heatmap)
        delta_color = "normal" if abs_ret > 0 else "inverse"
        
        master_data.append({
            "Ticker": t, 
            "Abs Return %": abs_ret,
            "Color": delta_color,
            "News": tick.news[0] if tick.news else None
        })

# --- STEP 3: NATIVE HEATMAP (METRIC GRID) ---
st.subheader("🔥 Sector Momentum (1mo)")
cols = st.columns(4) # 4 per row for Chromebook view
sorted_data = sorted(master_data, key=lambda x: x['Abs Return %'], reverse=True)

for i, item in enumerate(sorted_data):
    with cols[i % 4]:
        # Green/Red indicators based on absolute performance
        st.metric(label=item['Ticker'], value=f"{item['Abs Return %']}%", delta=item['Abs Return %'], delta_color=item['Color'])

# --- STEP 4: WATCHLIST NEWS ---
st.subheader("📰 Watchlist Intel")
for item in sorted_data[:4]: # Show news for top 4 winners
    if item['News']:
        with st.expander(f"Recent News: {item['Ticker']}"):
            st.write(f"**{item['News']['title']}**")
            st.caption(f"[Source/Full Article]({item['News']['link']})")

# --- STEP 5: RANKED FOOTER ---
footer_str = " | ".join([f"{i['Ticker']}: {i['Abs Return %']}%" for i in sorted_data])
st.caption(f"📅 **Last Month Performance (Ranked):** {footer_str}")
