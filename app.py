import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v9.90", layout="wide")

# --- [2. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v9.90")
st.caption("Status: 🟢 COLOR ENGINE LOCKED")

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
                recon_list.append({"Ticker": t, "Price": f"${curr:.2f}", "Status": "🚀 Blue Sky" if t == "NVTS" else "🟢 Steady"})
            except: continue
        st.table(pd.DataFrame(recon_list))
        st.area_chart(data["NVTS"]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(crypto_list)
    if c_data is not None:
        for c in crypto_list:
            st.metric(c, f"${c_data[c]['Close'].iloc[-1]:,.2f}")
            st.area_chart(c_data[c]['Close'].tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")

# --- [TAB 3: HEAT MAP - COLOR-LOCK FIX] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Volume (RVOL)")
    
    # --- TEST BUTTON: Force red/green to prove they work on your phone ---
    if st.button("🧪 RUN COLOR TEST"):
        st.error("RED TEST: If you see this, Red is working.")
        st.success("GREEN TEST: If you see this, Green is working.")
    
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        st.write("---")
        for h in h_tickers:
            try:
                rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                price = h_data[h]['Close'].iloc[-1]
                
                col_t, col_v, col_p = st.columns([1, 2, 1])
                with col_t:
                    st.markdown(f"**{h}**")
                with col_v:
                    # Using Badges for better mobile visibility
                    if rvol > 2.2:
                        st.badge(f"EXTREME: {rvol:.2f}x", color="red", icon="🚨")
                    elif rvol > 1.5:
                        st.badge(f"HIGH: {rvol:.2f}x", color="green", icon="🔥")
                    else:
                        st.badge(f"Normal: {rvol:.2f}x", color="gray")
                with col_p:
                    st.write(f"${price:.2f}")
                st.write("---")
            except: continue

st.divider()
st.caption(f"v9.90 | NVTS Countdown: {max(0, days_left)} Days | Wytheville Hub")
