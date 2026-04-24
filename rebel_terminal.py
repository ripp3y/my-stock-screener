import streamlit as st
import yfinance as yf
import pandas as pd

# 🛡️ SOVEREIGN TERMINAL CONFIG
st.set_page_config(page_title="Strategic US Terminal", layout="wide", initial_sidebar_state="collapsed")

# Minimal Attribution
st.markdown("<p style='font-size:10px; color: #555;'>Powered by Gemini | Sovereignty v4.0 | Apr 24, 2026</p>", unsafe_allow_True=True)

# 🛠️ THE ARCHITECT SIDEBAR (Ticker Control)
with st.sidebar:
    st.title("Recon Controls")
    # Change these text boxes to update the dashboard
    ticker = st.text_input("Primary Target", value="SDGR").upper()
    comp_ticker = st.text_input("Comparison Bridge", value="MSFT").upper()
    
    st.divider()
    st.subheader("Whale Tracking")
    st.page_link("https://unusualwhales.com/live-options-flow", label="Live Options Flow", icon="🐋")
    
    st.divider()
    st.subheader("May 5 Catalyst Watch")
    st.info("SDGR & NVTS both
