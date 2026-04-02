import streamlit as st
import yfinance as yf
import pandas as pd

# --- STEP 1: UI BASICS ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_p = st.sidebar.number_input("Purchase Price", value=23.0)

# --- STEP 2: ALPHA DATA ENGINE ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
master_data = []

for t in portfolio:
    tick = yf.Ticker(t)
    hist = tick.history(period="1mo")
    if not hist.empty:
        # Prevent ValueErrors by flattening
        p = hist['Close'].values.flatten()
        abs_ret = round(((p[-1] - p[0]) / p[0]) * 100, 2)
        
        # Pull first news item safely
        news = tick.news[0] if tick.news else {}
        
        master_data.append({
            "Ticker": t, 
            "Abs Return %": abs_ret,
            "News Title": news.get('title', 'No Recent Headlines'),
            "News Link": news.get('link', '#')
        })

# Sort Best to Least
sorted_data = sorted(master_data, key=lambda x: x['Abs Return %'], reverse=True)

# --- STEP 3: MOMENTUM GRID (HEATMAP) ---
st.subheader("🔥 Sector Momentum (1mo)")
cols = st.columns(4) 

for i, item in enumerate(sorted_data):
    with cols[i % 4]:
        # Green if positive, Red if negative
        color = "normal" if item['Abs Return %'] > 0 else "inverse"
        st.metric(label=item['Ticker'], value=f"{item['Abs Return %']}%", delta=item['Abs Return %'], delta_color=color)

# --- STEP 4: SAFE NEWS FEED ---
st.subheader("📰 Watchlist Intel")
for item in sorted_data[:4]:
    # Use expander to keep the UI clean
    with st.expander(f"Intel: {item['Ticker']}"):
        st.write(f"**{item['News Title']}**")
        if item['News Link'] != '#':
            st.caption(f"[Full Story]({item['News Link']})")

# --- STEP 5: RANKED FOOTER ---
footer_str = " | ".join([f"{i['Ticker']}: {i['Abs Return %']}%" for i in sorted_data])
st.caption(f"📅 **Last Month Performance (Ranked):** {footer_str}")
