import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG MUST BE FIRST] ---
st.set_page_config(page_title="Radar v5.70", layout="wide")

# --- [2. DATA LOADERS] ---
@st.cache_data(ttl=86400)
def load_market_master():
    url = "https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/all.csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.lower().replace(" ", "") for c in df.columns]
        if 'marketcap' not in df.columns: df['marketcap'] = 0
        return df
    except:
        return pd.DataFrame(columns=['symbol', 'name', 'marketcap'])

def get_live_metrics(tickers):
    if not tickers: return None
    # Fetching 5 days of data for volume averaging and price moves
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. STYLING LOGIC] ---
def highlight_spikes(row):
    # Bright Green for Spikes, Red for Consolidation
    if "⚡" in str(row['Mission Status']) or "🔥" in str(row['Mission Status']):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. INITIALIZATION] ---
master_df = load_market_master()

# --- [5. UI HEADER] ---
st.title("📡 Radar v5.70: Portfolio Recon")

# --- [6. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

with tab_recon:
    st.subheader("Tactical Portfolio Overview")
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    
    recon_list = []
    # Status mapping based on current market behavior
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
            prev_close = data[t]['Close'].iloc[-8] # Approx 24h ago in 1h intervals
            move = ((curr - prev_close) / prev_close) * 100
            target = curr * 1.20
            
            recon_list.append({
                "Ticker": t,
                "Current Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Upside Target": f"${target:.2f}",
                "Mission Status": status_map.get(t, "Scanning")
            })
        except: continue
    
    # Display styled table
    df_recon = pd.DataFrame(recon_list)
    if not df_recon.empty:
        st.table(df_recon.style.apply(highlight_spikes, axis=1))

with tab_alpha:
    st.subheader("🌪️ Volume Spike & Institutional Filter")
    col1, col2 = st.columns(2)
    with col1:
        min_cap = st.number_input("Min Market Cap ($B):", value=1.0, step=0.5) * 1_000_000_000
    with col2:
        vol_threshold = st.slider("Vol Spike Threshold:", 1.0, 5.0, 1.5)

    filtered_options = master_df[master_df['marketcap'] >= min_cap]['symbol'].tolist()
    picks = st.multiselect("Active Watchlist:", filtered_options, default=["NVTS", "FIX", "MTZ"])
    
    if picks:
        raw_data = get_live_metrics(picks)
        alpha_results = []
        for p in picks:
            try:
                recent_vol = raw_data[p]['Volume'].iloc[-1]
                avg_vol = raw_data[p]['Volume'].mean()
                ratio = recent_vol / avg_vol
                price = raw_data[p]['Close'].iloc[-1]
                
                alpha_results.append({
                    "Ticker": p, 
                    "Price": f"${price:.2f}", 
                    "Vol Ratio": f"{ratio:.2f}x",
                    "Status": "🔥 SPIKING" if ratio > vol_threshold else "Steady"
                })
            except: continue
        st.dataframe(pd.DataFrame(alpha_results), use_container_width=True)

with tab_breakout:
    st.subheader("🚀 High-Velocity Leads")
    # Monitoring your key runners
    leads = ["ALAB", "CRUS", "AMSC", "VRT"]
    l_data = get_live_metrics(leads)
    for l in leads:
        try:
            curr = l_data[l]['Close'].iloc[-1]
            st.write(f"**{l}**: ${curr:.2f} | Strength: Strong")
        except: continue

st.divider()
st.caption("Strategy: Monitor NVTS for $19.50 exit. Prepare FIX/MTZ rotation for April 28.")
