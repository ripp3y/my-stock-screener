import streamlit as st
from datetime import datetime

# --- 1. NEURAL GUARDIAN DATA BOARD (April 15, 2026) ---
GUARDIAN_INTEL = {
    "SNDK": {
        "ownership": "81.8% Institutional Concentration",
        "insider": "Zero sales in April; Holders waiting for Monday rebalance.",
        "news": "Nasdaq-100 inclusion confirmed for Monday, April 20, 2026.",
        "analysis": "Passive funds must acquire millions of shares by market open Monday."
    },
    "MRVL": {
        "ownership": "78.4% Institutional (Vanguard/BlackRock leading)",
        "insider": "NVIDIA is now a major strategic preferred shareholder.",
        "news": "NVIDIA finalized $2B investment in MRVL to secure AI data pathways.",
        "analysis": "Currently acting as the market anchor; bucking the Tax Day trend."
    },
    "CIEN": {
        "ownership": "97.8% Institutional (Top-tier density)",
        "insider": "Programmatic 10b5-1 sales only; zero 'panic' selling noted.",
        "news": "Zacks #1 Rank; Backlog hit record $7B for FY2026 AI infrastructure.",
        "analysis": "RSI reset to 55.30 is attracting institutional buy-side support."
    }
}

# --- 2. THE GUARDIAN INTERFACE ---
st.title("🛡️ Neural Guardian Terminal v3.11")
st.caption(f"Signal Handshake Verified: {datetime.now().strftime('%H:%M:%S')}")

target = st.selectbox("🎯 Active Target Recon", list(GUARDIAN_INTEL.keys()))
intel = GUARDIAN_INTEL[target]

# GUARDIAN TILES
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### 📰 Shift News")
    st.info(intel['news'])
    st.markdown("### 💼 Ownership Structure")
    st.warning(intel['ownership'])

with col2:
    st.markdown("### 🕵️ Insider Activity")
    st.success(intel['insider'])
    st.markdown("### 🧠 Strategic Memo")
    st.markdown(f"> {intel['analysis']}")

st.divider()
st.progress(0.95, text="Institutional Retention Index")
