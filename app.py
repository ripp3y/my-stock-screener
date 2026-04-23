import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v9.40", layout="wide")

# --- [2. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [3. HEADER & COUNTDOWN] ---
earnings_date = datetime(2026, 5, 5)
days_to_earnings = (earnings_date - datetime.now()).days

st.title("📟 Strategic Terminal v9.40")
st.caption(f"Engine: Python 3.12 | Status: 🟢 HEAT MAP RE-LINKED")
st.metric("NVTS Earnings Countdown", f"{days_to_earnings} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                curr = data[t]['Close'].iloc[-1]
                recon_list.append({"Ticker": t, "Price": f"${curr:.2f}", "20% Target": f"${curr * 1.20:.2f}", "Status": "🚀 Blue Sky" if t == "NVTS" else "🟢 Steady"})
            except: continue
        st.table(pd.DataFrame(recon_list))
        st.divider()
        target = st.selectbox("Deep-Dive (60-Day):", portfolio)
        st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(crypto_list)
    if c_data is not None:
        for c in crypto_list:
            col1, col2 = st.columns([1, 3])
            with col1: st.metric(c, f"${c_data[c]['Close'].iloc[-1]:,.2f}")
            with col2: st.area_chart(c_data[c]['Close'].tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")

# --- [TAB 3: HEAT MAP - FIXED] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Momentum (RVOL)")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        h_list = []
        for h in h_tickers:
            try:
                # Calculate RVOL
                rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                h_list.append({
                    "Ticker": h,
                    "RVOL": rvol,
                    "Price": h_data[h]['Close'].iloc[-1],
                    "Intensity": "🚨 EXTREME" if rvol > 2.2 else "🔥 HIGH" if rvol > 1.5 else "Normal"
                })
            except: continue
        
        # SWAP: Using st.dataframe with use_container_width for reliable mobile rendering
        df_h = pd.DataFrame(h_list)
        st.dataframe(
            df_h.style.background_gradient(cmap='Greens', subset=['RVOL'])
            .format({"RVOL": "{:.2f}x", "Price": "${:.2f}"}),
            use_container_width=True,
            hide_index=True
        )
        st.caption("Gradients now powered by Canvas engine for stability.")
