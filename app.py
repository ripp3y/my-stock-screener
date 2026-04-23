import streamlit as st
import pandas as pd
import yfinance as yf
import sys

# --- [1. CONFIG - MUST BE FIRST] ---
st.set_page_config(page_title="Radar v8.00", layout="wide")

# --- [2. CLEAN DATA LOADER] ---
@st.cache_data(ttl=300)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # yfinance 0.2.64 handles handshakes automatically on Python 3.12
        # We avoid 'session' or 'proxies' to prevent YFDataException
        df = yf.download(
            tickers=tickers, 
            period="5d", 
            interval="1h", 
            group_by='ticker', 
            auto_adjust=True,
            progress=False
        )
        return df
    except Exception as e:
        st.error(f"📡 Connection Interrupted: {e}")
        return None

# --- [3. STYLING LOGIC] ---
def highlight_rows(row):
    # Restores the iconic bright green glow for high-priority movers
    triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(t in str(row['Mission Status']) for t in triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📟 Strategic Terminal v8.00")
st.caption(f"Engine: Python {sys.version.split()[0]} | Status: 🟢 STABLE")
st.markdown("---")

# --- [5. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    # Status Mapping from your v6.00 design
    status_map = {
        "NVTS": "⚡ Hyper-Growth", "FIX": "🔥 Institutional Spiking",
        "SNDK": "🚀 Blue Sky Breakout", "MRVL": "🚀 New 52W High",
        "STX": "🟢 Steady Accumulation", "MTZ": "🧱 Structural Markup",
        "CIEN": "🟡 Healthy Consolidation"
    }

    if data is not None and not data.empty:
        recon_list = []
        for t in portfolio:
            try:
                # Handle Multi-Index Data correctly
                ticker_data = data[t]
                curr = ticker_data['Close'].iloc[-1]
                prev = ticker_data['Close'].iloc[-8] # Approx 24h ago
                move = ((curr - prev) / prev) * 100
                
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${curr:.2f}",
                    "24h Move": f"{move:+.2f}%",
                    "20% Target": f"${curr * 1.20:.2f}",
                    "Mission Status": status_map.get(t, "Scanning...")
                })
            except: continue
        
        # DISPLAY MAIN TABLE
        st.table(pd.DataFrame(recon_list).style.apply(highlight_rows, axis=1))

        # RESTORE AUTOMATIC CHARTS TO RECON TAB
        st.divider()
        st.subheader("📈 Core Momentum")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**NVTS: 5-Day Trend**")
            st.area_chart(data["NVTS"]['Close'], color="#00FF00")
        with c2:
            st.write("**FIX: 5-Day Trend**")
            st.area_chart(data["FIX"]['Close'], color="#00FF00")

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Alpha Scanner")
    alpha_list = ["ALAB", "CRUS", "AMSC", "VRT", "SMCI"]
    a_data = get_clean_data(alpha_list)
    
    if a_data is not None:
        alpha_rows = []
        for a in alpha_list:
            try:
                price = a_data[a]['Close'].iloc[-1]
                alpha_rows.append({"Ticker": a, "Price": f"${price:.2f}", "Status": "🔥 SCANNING"})
            except: continue
        st.table(pd.DataFrame(alpha_rows))

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 Rocket Monitor")
    for lead in ["NVTS", "FIX", "ALAB"]:
        st.markdown(f"**{lead}** Breakthrough Strength:")
        if data is not None and lead in data:
            st.line_chart(data[lead]['Close'], height=200, color="#00FF00")

st.divider()
st.caption("Strategy: v8.00 Restoration Complete. Focusing on NVTS $19.50 Pivot.")
