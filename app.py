import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v9.30", layout="wide")

# --- [2. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # 60-day standard lookback for all tabs
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [3. HEADER & COUNTDOWN] ---
earnings_date = datetime(2026, 5, 5)
days_to_earnings = (earnings_date - datetime.now()).days

st.title("📟 Strategic Terminal v9.30")
col_info, col_countdown = st.columns([3, 1])
with col_info:
    st.caption(f"Engine: Python 3.12 | Status: 🟢 SCALED INTELLIGENCE")
with col_countdown:
    # Highlighting the critical countdown to May 5th
    st.metric("NVTS Earnings Countdown", f"{days_to_earnings} Days", border=True)

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO SCALED", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                curr = data[t]['Close'].iloc[-1]
                recon_list.append({
                    "Ticker": t, 
                    "Price": f"${curr:.2f}", 
                    "20% Target": f"${curr * 1.20:.2f}",
                    "Mission Status": "🚀 Blue Sky" if t == "NVTS" else "🟢 Steady"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list))
        st.divider()
        target = st.selectbox("Deep-Dive (60-Day):", portfolio)
        st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO SCALED] ---
with tab_crypto:
    st.subheader("₿ 60-Day Miner Velocity")
    # MARA ($11.91) and IREN ($51.17) are showing high 60-day relative strength
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF", "RIOT"]
    c_data = get_clean_data(crypto_list)
    
    if c_data is not None:
        for c in crypto_list:
            col_c1, col_c2 = st.columns([1, 3])
            with col_c1:
                price = c_data[c]['Close'].iloc[-1]
                st.metric(c, f"${price:,.2f}")
                st.caption("60-Day Trendline ➔")
            with col_c2:
                # Orange for BTC, Green for Mining Equities
                chart_color = "#FF9900" if "BTC" in c else "#00FF00"
                st.area_chart(c_data[c]['Close'].tail(60), height=140, color=chart_color)

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Inflow (RVOL)")
    watch_list = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(watch_list)
    
    if h_data is not None:
        heat_rows = []
        for h in watch_list:
            try:
                # RVOL: Is volume significantly higher than the 20-day average?
                rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                intensity = "🚨 EXTREME" if rvol > 2.2 else "🔥 HIGH" if rvol > 1.5 else "Normal"
                
                heat_rows.append({
                    "Ticker": h,
                    "RVOL": rvol,
                    "Intensity": intensity,
                    "Price": h_data[h]['Close'].iloc[-1]
                })
            except: continue
        
        df_heat = pd.DataFrame(heat_rows)
        # Visual intensity scaling via background gradient
        st.dataframe(
            df_heat.style.background_gradient(cmap='Greens', subset=['RVOL'])
            .format({"RVOL": "{:.2f}x", "Price": "${:.2f}"}),
            use_container_width=True, hide_index=True
        )
        st.info("Strategy: RVOL > 1.5x identifies potential 'Smart Money' accumulation.")

st.divider()
st.caption("v9.30 | BTC Resistance: $78,900 | NVTS Pivot: $19.50")
