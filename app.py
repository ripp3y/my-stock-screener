import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v6.30", layout="wide")

# --- [2. DATA LOADER] ---
@st.cache_data(ttl=300) # Faster refresh for live volume
def get_alpha_metrics(tickers):
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING: HEAT MAP LOGIC] ---
def volume_heat_map(row):
    # If Volume is 2.5x the 5-day average, it's an Institutional Spike
    try:
        ratio = float(row['Vol Ratio'].replace('x', ''))
        if ratio >= 2.5:
            return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
        elif ratio >= 1.5:
            return ['background-color: #ADFF2F; color: black'] * len(row) # Lime Green
    except: pass
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📡 Radar v6.30: Institutional Heat Map")

tab_recon, tab_heat = st.tabs(["📊 RECON", "🌪️ VOLUME HEAT"])

with tab_recon:
    # Restoring the clean v5.7 style for your core portfolio
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_alpha_metrics(portfolio)
    
    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            vol = data[t]['Volume'].iloc[-1]
            avg_vol = data[t]['Volume'].mean()
            ratio = vol / avg_vol
            
            recon_list.append({
                "Ticker": t,
                "Price": f"${curr:.2f}",
                "Vol Ratio": f"{ratio:.2f}x",
                "Mission Status": "⚡ Hyper-Growth" if t == "NVTS" else "Scanning"
            })
        except: continue
    
    st.table(pd.DataFrame(recon_list).style.apply(volume_heat_map, axis=1))

with tab_heat:
    st.subheader("🌪️ Alpha Scanner: Institutional Spikes")
    # Expanding to see where the rest of the market is moving
    market_leads = ["ALAB", "CRUS", "AMSC", "VRT", "SMCI", "NVTS"]
    lead_data = get_alpha_metrics(market_leads)
    
    heat_list = []
    for l in market_leads:
        try:
            v_curr = lead_data[l]['Volume'].iloc[-1]
            v_avg = lead_data[l]['Volume'].mean()
            v_ratio = v_curr / v_avg
            heat_list.append({
                "Ticker": l,
                "Vol Ratio": f"{v_ratio:.2f}x",
                "Intensity": "HIGH" if v_ratio > 2.0 else "Normal"
            })
        except: continue
    
    st.table(pd.DataFrame(heat_list).style.apply(volume_heat_map, axis=1))

st.caption("Strategy: v6.30 Core. Monitoring NVTS Volume Ratio for Institutional Exhaustion.")
