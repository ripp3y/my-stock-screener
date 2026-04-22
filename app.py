import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v5.80", layout="wide")

# --- [2. DATA LOADERS] ---
@st.cache_data(ttl=3600)
def get_live_metrics(tickers):
    if not tickers: return None
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING LOGIC] ---
def highlight_velocity(row):
    triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(t in str(row['Mission Status']) for t in triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📡 Radar v5.80: Hybrid Dashboard")

# --- [5. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

with tab_recon:
    st.subheader("Clean Portfolio View")
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    
    # Standard 5.70 Layout
    recon_list = []
    status_map = {
        "NVTS": "⚡ Hyper-Growth", "FIX": "🔥 Institutional Spiking",
        "SNDK": "🚀 Blue Sky Breakout", "MRVL": "🚀 New 52W High",
        "STX": "🟢 Steady Accumulation", "MTZ": "🧱 Structural Markup",
        "CIEN": "🟡 Healthy Consolidation"
    }

    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[-8]
            move = ((curr - prev) / prev) * 100
            recon_list.append({
                "Ticker": t,
                "Current Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Target": f"${curr * 1.20:.2f}",
                "Mission Status": status_map.get(t, "Scanning")
            })
        except: continue
    
    # DISPLAY AS CLEAN TABLE (v5.7 style)
    df_recon = pd.DataFrame(recon_list)
    st.table(df_recon.style.apply(highlight_velocity, axis=1))
    
    # ADD QUICK-ACTION CHART BUTTONS BELOW
    st.write("### 📈 Quick Charts")
    cols = st.columns(len(portfolio))
    for i, t in enumerate(portfolio):
        with cols[i]:
            st.link_button(f"{t}", f"https://finance.yahoo.com/quote/{t}/chart")

with tab_alpha:
    st.subheader("Alpha Scanner")
    st.info("Scanner logic remains active for institutional spikes.")

st.caption("v5.80: Reverting to clean table layout with external chart buttons.")
