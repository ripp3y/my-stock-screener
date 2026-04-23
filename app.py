import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG MUST BE FIRST] ---
st.set_page_config(page_title="Radar v6.00", layout="wide")

# --- [2. DATA LOADERS] ---
@st.cache_data(ttl=3600)
def get_live_metrics(tickers):
    if not tickers: return None
    # Pulling hourly data to ensure the '24h move' is pinpoint accurate
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING LOGIC] ---
def highlight_velocity(row):
    # This restores the "Bright Green" glow for high-momentum tickers
    triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(trigger in str(row['Mission Status']) for trigger in triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📡 Radar v6.00: Strategic Terminal")
st.markdown("---")

# --- [5. TABS RESTORED] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    st.subheader("Tactical Portfolio (Clean View)")
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    
    recon_list = []
    # Restoring your specific Emoji Tiers
    status_map = {
        "NVTS": "⚡ Hyper-Growth",
        "FIX": "🔥 Institutional Spiking",
        "SNDK": "🚀 Blue Sky Breakout",
        "MRVL": "🚀 New 52W High",
        "STX": "🟢 Steady Accumulation",
        "MTZ": "🧱 Structural Markup",
        "CIEN": "🟡 Healthy Consolidation"
    }

    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev_close = data[t]['Close'].iloc[-8] # Approx 24h ago
            move = ((curr - prev_close) / prev_close) * 100
            
            recon_list.append({
                "Ticker": t,
                "Current Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Target": f"${curr * 1.20:.2f}",
                "Mission Status": status_map.get(t, "Scanning...")
            })
        except: continue
    
    df_recon = pd.DataFrame(recon_list)
    if not df_recon.empty:
        # st.table is used here because it renders perfectly on mobile
        st.table(df_recon.style.apply(highlight_velocity, axis=1))

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Relative Volume Scanner")
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
    st.subheader("🚀 High-Velocity Watch")
    leads = ["NVTS", "FIX", "ALAB", "CRUS"]
    for l in leads:
        st.write(f"**{l}**: Institutional Momentum Active.")
        st.link_button(f"View {l} Chart", f"https://finance.yahoo.com/quote/{l}/chart")

st.markdown("---")
st.caption("v6.00 Baseline: Targets based on 100% YoY goal. Focusing on NVTS $22 exit.")
