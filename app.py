import streamlit as st
import pandas as pd

# 1. Global Page Config & Styling
st.set_page_config(layout="wide", page_title="Professional Stock Terminal")

# Custom CSS for the "Best of the Best" look
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0e1117; border-right: 1px solid #30363d; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Global Search Bar (US Only)
ticker = st.text_input("🔍 Search US Equities (NYSE/NASDAQ)", value="MU").upper()

# 3. Sidebar - Sector Performance (Live Data Simulation for Mar 31, 2026)
with st.sidebar:
    st.title("Sector Pulse")
    st.metric("Technology", "+3.83%", "1.2%")
    st.metric("Energy", "+1.80%", "0.5%")
    st.metric("Industrials", "+2.49%", "0.8%")
    st.divider()
    st.caption("Market Status: Relief Rally In Progress")

# 4. Main Mountain Chart Area (Placeholder for your UI)
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"{ticker} Mountain Analysis")
    # This is where your custom chart logic goes
    st.image("image_726023.png", use_container_width=True) 
    
    # News Sentiment Ticker
    st.info(f"🗞️ {ticker} News: Market rebound drives recovery from recent lows.")

with col2:
    st.subheader("Quick Stats")
    st.write(f"Current Price: **$337.84**")
    st.write("RSI (14): 42.5 (Neutral)")
    
