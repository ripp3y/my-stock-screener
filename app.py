import streamlit as st
import pandas as pd
import yfinance as yf
import sys

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v7.20", layout="wide")

# --- [2. HARDENED DATA LOADER] ---
@st.cache_data(ttl=300)
def get_market_data(tickers):
    if not tickers: return None
    # period="5d" gives us enough history for the 'Sparkline' charts
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING: THE GREEN GLOW] ---
def apply_mission_style(row):
    triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(t in str(row['Mission Status']) for t in triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📟 Strategic Terminal v7.20")
st.caption(f"Engine: Python {sys.version.split()[0]} | Status: 🟢 STABLE")

# --- [5. THE TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_market_data(portfolio)
    
    status_map = {
        "NVTS": "⚡ Hyper-Growth", "FIX": "🔥 Institutional Spiking",
        "SNDK": "🚀 Blue Sky Breakout", "MRVL": "🚀 New 52W High",
        "STX": "🟢 Steady Accumulation", "MTZ": "🧱 Structural Markup",
        "CIEN": "🟡 Healthy Consolidation"
    }

    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[-8] 
            move = ((curr - prev) / prev) * 100
            recon_list.append({
                "Ticker": t, "Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%", "20% Target": f"${curr * 1.20:.2f}",
                "Mission Status": status_map.get(t, "Scanning...")
            })
        except: continue
    
    st.table(pd.DataFrame(recon_list).style.apply(apply_mission_style, axis=1))

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Alpha Search (Institutional Inflow)")
    alpha_list = ["ALAB", "CRUS", "AMSC", "VRT", "SMCI"]
    alpha_data = get_market_data(alpha_list)
    
    alpha_results = []
    for a in alpha_list:
        try:
            price = alpha_data[a]['Close'].iloc[-1]
            # Simple Volume Spike Logic
            vol_curr = alpha_data[a]['Volume'].iloc[-1]
            vol_avg = alpha_data[a]['Volume'].mean()
            status = "🔥 SPIKING" if vol_curr > vol_avg else "Accumulating"
            alpha_results.append({"Ticker": a, "Price": f"${price:.2f}", "Status": status})
        except: continue
    st.table(pd.DataFrame(alpha_results))

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 Breakthrough Monitor")
    for lead in ["NVTS", "FIX", "ALAB"]:
        st.markdown(f"**{lead}** Velocity Check:")
        if lead in data:
            # Native lightweight charts that won't buffer on 3.12
            st.area_chart(data[lead]['Close'], height=200, color="#00FF00")

st.divider()
st.caption("Strategy: v7.20 Restoration. NVTS $19.50 Pivot in play.")
