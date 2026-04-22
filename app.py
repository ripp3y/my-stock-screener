import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG MUST BE FIRST] ---
st.set_page_config(page_title="Radar v5.50", layout="wide")

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
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. COLOR LOGIC] ---
def highlight_spikes(row):
    # If Status contains "SPIKING", turn the row Bright Green
    if "SPIKING" in str(row.Status):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. INITIALIZATION] ---
master_df = load_market_master()

# --- [5. UI HEADER] ---
st.title("📡 Radar v5.50")

# --- [6. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

with tab_recon:
    portfolio = ["SNDK", "MRVL", "STX", "FIX", "NVTS", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            recon_list.append({"Ticker": t, "Price": f"${curr:.2f}"})
        except: continue
    st.table(pd.DataFrame(recon_list))

with tab_alpha:
    st.subheader("🌪️ Volume Spike & Institutional Filter")
    
    col1, col2 = st.columns(2)
    with col1:
        min_cap = st.number_input("Min Market Cap ($B):", value=1.0, step=0.5) * 1_000_000_000
    with col2:
        vol_spike = st.slider("Vol Spike Threshold:", 1.0, 5.0, 1.5)

    filtered_options = master_df[master_df['marketcap'] >= min_cap]['symbol'].tolist()
    picks = st.multiselect("Watchlist:", filtered_options, default=["NVTS", "FIX", "MTZ"])
    
    if picks:
        raw_data = get_live_metrics(picks)
        results = []
        for p in picks:
            try:
                recent_vol = raw_data[p]['Volume'].iloc[-1]
                avg_vol = raw_data[p]['Volume'].mean()
                ratio = recent_vol / avg_vol
                price = raw_data[p]['Close'].iloc[-1]
                
                results.append({
                    "Ticker": p, 
                    "Price": f"${price:.2f}", 
                    "Vol Ratio": f"{ratio:.2f}x",
                    "Status": "🔥 SPIKING" if ratio > vol_spike else "Steady"
                })
            except: continue
        
        # APPLYING THE BRIGHT GREEN STYLE
        df_results = pd.DataFrame(results)
        if not df_results.empty:
            styled_df = df_results.style.apply(highlight_spikes, axis=1)
            st.dataframe(styled_df, use_container_width=True)

with tab_breakout:
    st.subheader("🚀 52-Week High Watch")
    gems = ["ALAB", "CRUS", "AMSC", "STX", "VRT"]
    g_data = get_live_metrics(gems)
    for g in gems:
        try:
            curr = g_data[g]['Close'].iloc[-1]
            high = g_data[g]['High'].max()
            st.write(f"**{g}**: ${curr:.2f} (Targeting ${high:.2f})")
        except: continue

st.caption(f"Status: Active | Highlighting Spikes over {vol_spike}x")
