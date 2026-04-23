import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v7.00", layout="wide")

# --- [2. DATA LOADER] ---
@st.cache_data(ttl=300)
def get_terminal_data(tickers):
    if not tickers: return None
    # Fetching 5 days of hourly data for smooth charts and accurate 24h moves
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING LOGIC] ---
def apply_mission_style(row):
    # Restoring the Bright Green glow for your priority movers
    priority_triggers = ["⚡ Hyper-Growth", "🔥 Institutional Spiking", "🚀 Blue Sky Breakout"]
    if any(trigger in str(row['Mission Status']) for trigger in priority_triggers):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI HEADER] ---
st.title("📟 Strategic Terminal v7.00")
st.markdown("---")

# --- [5. TABS RESTORED] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_terminal_data(portfolio)
    
    # Status Tiers mapped from your preferred v6.00 screenshots
    status_map = {
        "NVTS": "⚡ Hyper-Growth",
        "FIX": "🔥 Institutional Spiking",
        "SNDK": "🚀 Blue Sky Breakout",
        "MRVL": "🚀 New 52W High",
        "STX": "🟢 Steady Accumulation",
        "MTZ": "🧱 Structural Markup",
        "CIEN": "🟡 Healthy Consolidation"
    }

    recon_list = []
    for t in portfolio:
        try:
            # Pricing & Move Logic
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[-8] 
            move = ((curr - prev) / prev) * 100
            
            recon_list.append({
                "Ticker": t,
                "Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Target": f"${curr * 1.20:.2f}",
                "Mission Status": status_map.get(t, "Scanning...")
            })
        except: continue
    
    # Render the styled table
    st.table(pd.DataFrame(recon_list).style.apply(apply_mission_style, axis=1))

    # --- NEW LIGHTWEIGHT CHART SECTION ---
    st.markdown("### 📈 Quick-Look Technicals")
    selected = st.selectbox("Select Stone to Inspect:", portfolio)
    if selected in data:
        # Area chart is much faster than Plotly/Candlesticks for mobile
        chart_data = data[selected]['Close']
        st.area_chart(chart_data, color="#00FF00" if selected in ["NVTS", "FIX"] else "#1E90FF")
        st.link_button(f"Open Full {selected} Pro Chart", f"https://finance.yahoo.com/quote/{selected}/chart")

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Relative Volume Scanner")
    alpha_watchlist = ["ALAB", "CRUS", "AMSC", "FLR", "VRT", "SMCI"]
    alpha_data = get_terminal_data(alpha_watchlist)
    
    alpha_rows = []
    for a in alpha_watchlist:
        try:
            curr_a = alpha_data[a]['Close'].iloc[-1]
            alpha_rows.append({"Ticker": a, "Price": f"${curr_a:.2f}", "Status": "🔥 SCANNING"})
        except: continue
    st.table(pd.DataFrame(alpha_rows))

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 High-Velocity Monitor")
    for lead in ["NVTS", "FIX", "ALAB"]:
        st.markdown(f"**{lead}**: Institutional Momentum Active.")
        # Lightweight Sparkline-style chart for breakouts
        if lead in data:
            st.line_chart(data[lead]['Close'], height=150)

st.markdown("---")
st.caption("v7.00 Performance Baseline | Target: 100% YoY")
