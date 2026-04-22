# Force the sidebar to stay open on load
st.set_page_config(
    page_title="Radar v5.30", 
    layout="wide", 
    initial_sidebar_state="expanded"
)
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [SYSTEM CONFIG] ---
st.set_page_config(page_title="Radar v5.30", layout="wide")

# --- [ROBUST DATA LOADER] ---
@st.cache_data(ttl=86400)
def load_market_master():
    url = "https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/all.csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.lower().replace(" ", "") for c in df.columns]
        # FIX: Ensure required columns exist to prevent KeyErrors
        if 'sector' not in df.columns: df['sector'] = 'Unknown'
        if 'marketcap' not in df.columns: df['marketcap'] = 0
        return df
    except:
        return pd.DataFrame(columns=['symbol', 'name', 'sector', 'marketcap'])

def get_live_metrics(tickers):
    if not tickers: return None
    # Fetching 5 days to calculate Average Volume vs Current Volume
    data = yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)
    return data

# --- [INITIALIZATION] ---
master_df = load_market_master()

# --- [SIDEBAR FILTERS] ---
st.sidebar.header("🛡️ Institutional Filters")
min_cap = st.sidebar.slider("Min Market Cap ($B):", 0, 500, 1) * 1_000_000_000
vol_spike_threshold = st.sidebar.slider("Volume Spike Ratio (x):", 1.0, 5.0, 1.5)

# --- [TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

with tab_recon:
    portfolio = ["SNDK", "MRVL", "STX", "FIX", "NVTS", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    recon_list = []
    for t in portfolio:
        try:
            curr_price = data[t]['Close'].iloc[-1]
            recon_list.append({"Ticker": t, "Price": f"${curr_price:.2f}"})
        except: continue
    st.table(pd.DataFrame(recon_list))

with tab_alpha:
    st.subheader("🌪️ Volume Spike & Cap Search")
    
    # Filter by Cap
    filtered_df = master_df[master_df['marketcap'] >= min_cap]
    ticker_options = filtered_df['symbol'].tolist()
    
    picks = st.multiselect("Watchlist:", ticker_options, default=["NVTS", "FIX", "MTZ"])
    
    if picks:
        raw_data = get_live_metrics(picks)
        results = []
        for p in picks:
            try:
                # VOLUME SPIKE LOGIC
                recent_vol = raw_data[p]['Volume'].iloc[-1]
                avg_vol = raw_data[p]['Volume'].mean()
                vol_ratio = recent_vol / avg_vol
                
                price = raw_data[p]['Close'].iloc[-1]
                status = "🔥 SPIKING" if vol_ratio > vol_spike_threshold else "Steady"
                
                results.append({
                    "Ticker": p, 
                    "Price": f"${price:.2f}", 
                    "Vol Ratio": f"{vol_ratio:.2f}x",
                    "Status": status
                })
            except: continue
        st.dataframe(pd.DataFrame(results), use_container_width=True)

with tab_breakout:
    st.subheader("🚀 52-Week High Watch")
    gems = ["ALAB", "CRUS", "AMSC", "STX", "VRT"]
    g_data = get_live_metrics(gems)
    for g in gems:
        try:
            curr = g_data[g]['Close'].iloc[-1]
            high = g_data[g]['High'].max()
            dist = (1 - (curr / high)) * 100
            st.write(f"**{g}**: ${curr:.2f} ({dist:.2f}% from High)")
        except: continue

st.divider()
st.caption(f"Strategy: Exit NVTS (3-4 days). Watch for Volume Spikes > {vol_spike_threshold}x.")
