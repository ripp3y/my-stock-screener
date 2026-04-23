import streamlit as st
import pandas as pd
import yfinance as yf
import sys
from datetime import datetime

# --- [1. GLOBAL SAFETY] ---
if 'st' not in globals():
    import streamlit as st

# --- [2. CONFIG] ---
st.set_page_config(page_title="Radar v9.10", layout="wide")

# --- [3. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Standardized on 3mo/1d for 60-day stability across all tabs
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [4. UI STYLING] ---
def highlight_rows(row):
    if any(t in str(row['Mission Status']) for t in ["⚡", "🔥", "🚀"]):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [5. HEADER & COUNTDOWN] ---
earnings_date = datetime(2026, 5, 5)
days_to_earnings = (earnings_date - datetime.now()).days

st.title("📟 Strategic Terminal v9.10")
col_info, col_countdown = st.columns([3, 1])
with col_info:
    st.caption(f"Engine: Python {sys.version.split()[0]} | View: 60-Day Scaled")
with col_countdown:
    st.metric("NVTS Earnings Countdown", f"{days_to_earnings} Days")

# --- [6. TABS] ---
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
                    "Ticker": t, "Price": f"${curr:.2f}", 
                    "20% Target": f"${curr * 1.20:.2f}",
                    "Mission Status": "🚀 Blue Sky" if t == "NVTS" else "🟢 Steady"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list).style.apply(highlight_rows, axis=1))
        
        st.divider()
        target = st.selectbox("Deep-Dive Inspection:", portfolio)
        st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO SCALED] ---
with tab_crypto:
    st.subheader("₿ 60-Day Asset Velocity")
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF", "RIOT"]
    c_data = get_clean_data(crypto_list)
    
    if c_data is not None:
        for c in crypto_list:
            col_c1, col_c2 = st.columns([1, 3])
            with col_c1:
                price = c_data[c]['Close'].iloc[-1]
                # Calculate 60-day move for crypto
                start_60 = c_data[c]['Close'].iloc[-42] if len(c_data[c]) >= 42 else c_data[c]['Close'].iloc[0]
                move_60 = ((price - start_60) / start_60) * 100
                st.metric(c, f"${price:,.2f}", f"{move_60:+.2f}% (60d)")
            with col_c2:
                # Scaled out chart
                st.area_chart(c_data[c]['Close'].tail(60), height=150, color="#FF9900" if "BTC" in c else "#00FF00")

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Relative Volume & Momentum Heat Map")
    all_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(all_tickers)
    
    if h_data is not None:
        heat_rows = []
        for h in all_tickers:
            try:
                # RVOL Calculation
                recent_vol = h_data[h]['Volume'].iloc[-1]
                avg_vol = h_data[h]['Volume'].tail(20).mean()
                rvol = recent_vol / avg_vol
                
                # Performance
                curr_p = h_data[h]['Close'].iloc[-1]
                prev_p = h_data[h]['Close'].iloc[-2]
                day_move = ((curr_p - prev_p) / prev_p) * 100
                
                heat_rows.append({
                    "Ticker": h,
                    "RVOL": f"{rvol:.2f}x",
                    "Daily %": f"{day_move:+.2f}%",
                    "Intensity": "🚨 EXTREME" if rvol > 2.5 else "🔥 HIGH" if rvol > 1.5 else "Normal"
                })
            except: continue
        
        # Display as a styled table for high-intensity visual
        df_heat = pd.DataFrame(heat_rows)
        st.table(df_heat.style.background_gradient(cmap='Greens', subset=['RVOL']))

st.divider()
st.caption("v9.10 | Core Intelligence Saved | BTC Target: $82,000 Support Flip")
