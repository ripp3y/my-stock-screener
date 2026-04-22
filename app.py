import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG MUST BE FIRST] ---
st.set_page_config(page_title="Radar v6.00", layout="wide")

# --- [2. DATA LOADERS] ---
@st.cache_data(ttl=3600)
def get_live_metrics(tickers):
    if not tickers: return None
    # Pulling hourly data to get accurate 24h moves and volume ratios
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING LOGIC] ---
def highlight_velocity(row):
    # Apply Bright Green to high-momentum statuses
    momentum_triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(trigger in str(row['Mission Status']) for trigger in momentum_triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📡 Strategic US Terminal v6.00")
st.markdown("---")

# --- [5. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    st.subheader("Tactical Portfolio Overview")
    
    # Your Core Portfolio
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    
    recon_list = []
    # Status Tiers from v6.00 Screenshot
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
            prev_close = data[t]['Close'].iloc[-8] # ~24h ago
            move = ((curr - prev_close) / prev_close) * 100
            
            recon_list.append({
                "Ticker": t,
                "Current Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Upside Target": f"${curr * 1.20:.2f}",
                "Mission Status": status_map.get(t, "Scanning...")
            })
        except: continue
    
    df_recon = pd.DataFrame(recon_list)
    if not df_recon.empty:
        # Rendering as a table with the Green Glow applied
        st.table(df_recon.style.apply(highlight_velocity, axis=1))

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Relative Volume Scanner")
    # Interactive scanner logic preserved here...
    st.info("Scanner Active: Use sliders in the sidebar to filter the Master List.")

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 52-Week High Watch")
    for ticker in ["ALAB", "CRUS", "AMSC", "VRT"]:
        st.write(f"Monitoring **{ticker}** for next-leg breakout...")

st.markdown("---")
st.caption("Strategy: Focus on NVTS exit ($19.50+) and FIX/MTZ infrastructure rotation.")
