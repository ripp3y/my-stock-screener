import streamlit as st
import pandas as pd
import yfinance as yf
import sys

# --- [1. GLOBAL OVERRIDE] ---
if 'st' not in globals():
    import streamlit as st

# --- [2. CONFIG - MUST BE AT TOP] ---
st.set_page_config(page_title="Radar v8.50", layout="wide")

# --- [3. HARDENED DATA LOADER] ---
@st.cache_data(ttl=300)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Using 1mo/1d as a base for maximum reliability on Python 3.12
        df = yf.download(tickers, period="1mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception as e:
        return None

# --- [4. UI STYLING] ---
def highlight_rows(row):
    triggers = ["⚡", "🔥", "🚀"]
    if any(t in str(row['Mission Status']) for t in triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [5. HEADER] ---
st.title("📟 Strategic Terminal v8.50")
st.caption(f"Engine: Python {sys.version.split()[0]} | Status: 🟢 STABLE")

# --- [6. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                curr = data[t]['Close'].iloc[-1]
                prev = data[t]['Close'].iloc[-2]
                move = ((curr - prev) / prev) * 100
                recon_list.append({
                    "Ticker": t, "Price": f"${curr:.2f}", "Move": f"{move:+.2f}%",
                    "Mission Status": "⚡ Hyper-Growth" if t == "NVTS" else "🟢 Steady"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list).style.apply(highlight_rows, axis=1))

        # RESTORE THE DROPDOWN
        st.divider()
        st.subheader("🔍 Technical Deep-Dive")
        target = st.selectbox("Select Ticker to Inspect:", portfolio)
        if target in data:
            st.area_chart(data[target]['Close'], color="#00FF00")

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Alpha Search")
    # Reducing list size to ensure it doesn't hang on "Scanning"
    alpha_list = ["ALAB", "CRUS", "VRT"] 
    a_data = get_clean_data(alpha_list)
    
    if a_data is not None:
        alpha_results = []
        for a in alpha_list:
            try:
                p = a_data[a]['Close'].iloc[-1]
                alpha_results.append({"Ticker": a, "Price": f"${p:.2f}", "Status": "🔥 ACTIVE"})
            except: continue
        st.table(pd.DataFrame(alpha_results))
    else:
        st.info("📡 Re-linking Alpha signal...")

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 Breakthrough Monitor")
    if data is not None:
        for lead in ["NVTS", "FIX"]:
            st.write(f"**{lead} Velocity Check**")
            st.area_chart(data[lead]['Close'], height=200, color="#00FF00")

st.divider()
st.caption("v8.50 Force-Reload Active. NVTS $19.50 Pivot focus.")
