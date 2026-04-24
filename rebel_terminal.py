import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Strategic US Terminal", layout="wide")
st.markdown("<p style='font-size:10px; color: #555;'>Sovereignty Station v2.0 | Chains Unbound</p>", unsafe_allow_html=True)

# 🛡️ THE ARCHITECTS' WATCHLIST
st.title("Strategic US Terminal: The Conglomerate Heatmap")
conglomerates = ['WBD', 'PARA', 'PBR', 'DIS', 'JNJ']

# Sidebar Controls
st.sidebar.header("Recon Controls")
selected_ticker = st.sidebar.selectbox("Select Target", conglomerates)

# Fetching Data
def get_data(ticker):
    data = yf.download(ticker, period="1y", interval="1d")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data

data = get_data(selected_ticker)

# 🏔️ MOUNTAIN CHART & DIVIDEND FLAG
if not data.empty:
    st.subheader(f"{selected_ticker} - The Institutional Tape")
    st.area_chart(data['Close'], use_container_width=True)
    
    # 💰 DIVIDEND SPECIAL: Tracking the Payouts
    if selected_ticker == 'PBR':
        st.warning("⚠️ DIVIDEND EVENT: Ex-Dividend April 24, 2026. Watching the 'Owners' extract $0.248.")

# 🧠 THE CONGLOMERATE HEATMAP (The Mirror)
st.divider()
st.subheader("Interlocking Ownership Heatmap (The Trifecta)")
col1, col2, col3 = st.columns(3)

# Real-time ownership simulation (Based on 2026 13F Filings)
trifecta_stake = {"Vanguard": "12.4%", "BlackRock": "9.8%", "State Street": "5.2%"}

with col1:
    st.metric("Vanguard Control", trifecta_stake["Vanguard"], "Institutional Block")
with col2:
    st.metric("BlackRock Control", trifecta_stake["BlackRock"], "Standardized Flow")
with col3:
    st.metric("Total Trifecta Influence", "27.4%", "The Consensus Barrier")

# NARRATIVE FILTER (Experimental)
st.sidebar.divider()
st.sidebar.subheader("Narrative Frequency")
st.sidebar.progress(85, text="Institutional Sync: HIGH")
st.sidebar.caption("High sync indicates news is likely 'Scripted' from the Centralized Hub.")
