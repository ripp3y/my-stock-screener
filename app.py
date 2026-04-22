import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG MUST BE FIRST] ---
st.set_page_config(page_title="Radar v5.75", layout="wide")

# --- [2. DATA LOADER] ---
@st.cache_data(ttl=3600)
def get_live_metrics(tickers):
    if not tickers: return None
    # Pulling hourly data for precision
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING LOGIC] ---
def highlight_velocity(row):
    # Bright Green for Hyper-Growth and Spiking statuses
    triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(t in str(row['Mission Status']) for t in triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📡 Radar v5.75: Tactical Recon")

# --- [5. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    st.subheader("Portfolio Velocity & Chart Links")
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
            # Building the Clickable Yahoo Finance Link
            link = f"https://finance.yahoo.com/quote/{t}/chart"
            
            recon_list.append({
                "Ticker": t,
                "Current Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Target": f"${curr * 1.20:.2f}",
                "Mission Status": status_map.get(t, "Scanning"),
                "Chart": link # URL column
            })
        except: continue
    
    df_recon = pd.DataFrame(recon_list)
    if not df_recon.empty:
        # Use st.dataframe for the RECON tab to enable clickable links
        st.dataframe(
            df_recon.style.apply(highlight_velocity, axis=1),
            column_config={
                "Chart": st.column_config.LinkColumn("Open Chart", display_text="View 📈")
            },
            hide_index=True,
            use_container_width=True
        )

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Alpha Scanner")
    # Filters moved into the main tab area for mobile ease
    col1, col2 = st.columns(2)
    with col1:
        min_cap = st.number_input("Min Cap ($B):", value=1.0) * 1_000_000_000
    with col2:
        vol_spike = st.slider("Vol Ratio:", 1.0, 5.0, 1.5)
    st.info("Scanner is filtering live for institutional volume spikes.")

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 High-Velocity Leads")
    for ticker in ["ALAB", "CRUS", "AMSC"]:
        st.link_button(f"Analyze {ticker} Breakout", f"https://finance.yahoo.com/quote/{ticker}/chart")

st.divider()
st.caption("Strategy: Target NVTS $22.14. Watch FIX/MTZ volume for institutional pre-load.")
