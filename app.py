import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v9.80", layout="wide")

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
st.title("📟 Strategic Terminal v9.80")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

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

# --- [TAB 3: HEAT MAP - THE NATIVE FIX] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Volume (RVOL)")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        # Instead of a table that might break, we use native "Columns"
        # This is guaranteed to work on every phone.
        st.write("---")
        for h in h_tickers:
            try:
                rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                price = h_data[h]['Close'].iloc[-1]
                
                col_t, col_v, col_p = st.columns([1, 2, 1])
                
                with col_t:
                    st.write(f"**{h}**")
                
                with col_v:
                    # Native Streamlit color boxes (Red/Green)
                    if rvol > 2.2:
                        st.error(f"🚨 EXTREME: {rvol:.2f}x")
                    elif rvol > 1.5:
                        st.success(f"🔥 HIGH: {rvol:.2f}x")
                    else:
                        st.info(f"Normal: {rvol:.2f}x")
                
                with col_p:
                    st.write(f"${price:.2f}")
                st.write("---") # Thin separator line
            except: continue

st.divider()
st.caption("v9.80 | Using Native Status Elements for Mobile Stability")
