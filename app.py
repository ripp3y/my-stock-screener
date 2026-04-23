import streamlit as st
import pandas as pd
import yfinance as yf
import sys

# --- [1. GLOBAL SAFETY] ---
if 'st' not in globals():
    import streamlit as st

# --- [2. TERMINAL CONFIG] ---
st.set_page_config(page_title="Radar v8.90", layout="wide")

# --- [3. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Standardizing on 3mo/1d for 60-day visual stability
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception:
        return None

# --- [4. UI STYLING] ---
def highlight_rows(row):
    if any(t in str(row['Mission Status']) for t in ["⚡", "🔥", "🚀"]):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [5. HEADER] ---
st.title("📟 Strategic Terminal v8.90")
st.caption(f"Engine: Python {sys.version.split()[0]} | Status: 🟢 CORE ACTIVE")

# --- [6. TABS] ---
tab_recon, tab_crypto, tab_alpha = st.tabs(["📊 RECON", "₿ CRYPTO", "🌪️ ALPHA"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                ticker_df = data[t]
                curr = ticker_df['Close'].iloc[-1]
                # Price Targets Restoration
                target_20 = curr * 1.20
                recon_list.append({
                    "Ticker": t, 
                    "Price": f"${curr:.2f}", 
                    "20% Target": f"${target_20:.2f}",
                    "Mission Status": "🚀 Blue Sky" if t == "NVTS" else "🟢 Steady"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list).style.apply(highlight_rows, axis=1))

        # DIRECT PRO LINKS (Restored from v6.00)
        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            target = st.selectbox("Select Ticker for 60-Day View:", portfolio)
            st.area_chart(data[target]['Close'].tail(60), color="#00FF00")
        with col_b:
            st.write("**External Intelligence**")
            st.link_button(f"Open {target} Pro Chart", f"https://finance.yahoo.com/quote/{target}/chart")
            st.link_button("VectorVest Strategy Check", "https://www.vectorvest.com/")

# --- [TAB 2: CRYPTO (NEW)] ---
with tab_crypto:
    st.subheader("₿ Digital Asset Monitor")
    # BTC is testing $78k today; MARA/IREN are the core miners to watch
    crypto_tickers = ["BTC-USD", "MARA", "IREN", "RIOT", "WULF"]
    c_data = get_clean_data(crypto_tickers)
    
    if c_data is not None:
        c_list = []
        for c in crypto_tickers:
            try:
                curr = c_data[c]['Close'].iloc[-1]
                c_list.append({"Asset": c, "Current Price": f"${curr:,.2f}", "Trend": "📈 Bullish Context"})
            except: continue
        st.table(pd.DataFrame(c_list))

# --- [TAB 3: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Alpha Scanner: RVOL & Inflow")
    alpha_list = ["ALAB", "CRUS", "VRT", "SMCI"]
    a_data = get_clean_data(alpha_list)
    if a_data is not None:
        alpha_rows = []
        for a in alpha_list:
            try:
                p = a_data[a]['Close'].iloc[-1]
                # RVOL Logic (Today's Vol vs 20-Day Average)
                rvol = a_data[a]['Volume'].iloc[-1] / a_data[a]['Volume'].tail(20).mean()
                alpha_rows.append({"Ticker": a, "Price": f"${p:.2f}", "RVOL": f"{rvol:.2f}x"})
            except: continue
        st.table(pd.DataFrame(alpha_rows))

st.divider()
st.caption("v8.90 Core | Target: NVTS $19.50 Pivot | BTC Resistance: $78,900")
