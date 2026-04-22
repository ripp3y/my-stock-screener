import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v6.0", layout="wide")

# --- [2. DATA LOADER] ---
@st.cache_data(ttl=3600)
def get_live_metrics(tickers):
    if not tickers: return None
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING] ---
def highlight_velocity(row):
    triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(t in str(row['Mission Status']) for t in triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📡 Radar v6.0: Strategic Core")

# --- [5. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    st.subheader("Tactical Portfolio")
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    
    status_map = {
        "NVTS": "⚡ Hyper-Growth", "FIX": "🔥 Institutional Spiking",
        "SNDK": "🚀 Blue Sky Breakout", "MRVL": "🚀 New 52W High",
        "STX": "🟢 Steady Accumulation", "MTZ": "🧱 Structural Markup",
        "CIEN": "🟡 Healthy Consolidation"
    }

    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[-8]
            move = ((curr - prev) / prev) * 100
            recon_list.append({
                "Ticker": t,
                "Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Target": f"${curr * 1.20:.2f}",
                "Mission Status": status_map.get(t, "Scanning")
            })
        except: continue
    
    # RENDER CLEAN TABLE
    df_recon = pd.DataFrame(recon_list)
    st.table(df_recon.style.apply(highlight_velocity, axis=1))
    
    # EXTERNAL CHART DECK (Keeps table clean)
    st.write("### 📈 Open Charts")
    cols = st.columns(len(portfolio))
    for i, t in enumerate(portfolio):
        with cols[i]:
            st.link_button(f"{t}", f"https://finance.yahoo.com/quote/{t}/chart")

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Alpha Search")
    alpha_watchlist = ["ALAB", "CRUS", "AMSC", "FLR", "VRT", "SMCI"]
    alpha_data = get_live_metrics(alpha_watchlist)
    
    alpha_results = []
    for a in alpha_watchlist:
        try:
            price = alpha_data[a]['Close'].iloc[-1]
            alpha_results.append({"Ticker": a, "Price": f"${price:.2f}", "Status": "🔥 SCANNING"})
        except: continue
    st.table(pd.DataFrame(alpha_results))

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 High-Velocity Monitor")
    leads = ["NVTS", "FIX", "ALAB", "CRUS"]
    for l in leads:
        st.write(f"**{l}**: Institutional Momentum Active.")
        st.link_button(f"View {l} Chart", f"https://finance.yahoo.com/quote/{l}/chart")

st.divider()
st.caption("Strategy: v6.0 Baseline. Focus on NVTS $22 target and FIX/MTZ infrastructure rotation.")
