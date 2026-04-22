import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [SYSTEM CONFIG] ---
st.set_page_config(page_title="Radar v5.10", layout="wide")

# --- [MASTER LIST LOADER] ---
@st.cache_data(ttl=86400)
def load_global_tickers():
    # Using a reliable community-maintained CSV for all US tickers
    url = "https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/all.csv"
    try:
        df = pd.read_csv(url)
        return df['symbol'].tolist()
    except:
        # Emergency backup if GitHub is down
        return ["SNDK", "MRVL", "STX", "FIX", "NVTS", "MTZ", "CIEN", "CRUS", "ALAB", "FLR"]

def get_market_data(tickers):
    if not tickers: return None
    data = yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)
    return data

# --- [INITIALIZATION] ---
all_tickers = load_global_tickers()

# --- [UI HEADER] ---
st.title("📡 Radar v5.10")
st.caption(f"Connected to {len(all_tickers)} US Tickers | 100% YoY Mode Active")

# --- [TABBED INTERFACE] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["SNDK", "MRVL", "STX", "FIX", "NVTS", "MTZ", "CIEN"]
    data = get_market_data(portfolio)
    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[0]
            change = ((curr - prev) / prev) * 100
            recon_list.append({"Ticker": t, "Price": f"${curr:.2f}", "Move": f"{change:+.2f}%"})
        except: continue
    st.table(pd.DataFrame(recon_list))

# --- [TAB 2: ALPHA (GLOBAL SEARCH)] ---
with tab_alpha:
    st.subheader("Global Sector Search")
    user_search = st.multiselect("Search & Add Tickers to Watchlist:", all_tickers, default=["CRUS", "ALAB"])
    
    if user_search:
        search_data = get_market_data(user_search)
        alpha_list = []
        for t in user_search:
            try:
                curr = search_data[t]['Close'].iloc[-1]
                alpha_list.append({"Ticker": t, "Price": f"${curr:.2f}", "Status": "🔥 WATCHING"})
            except: continue
        st.dataframe(pd.DataFrame(alpha_list), use_container_width=True)

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("High-Velocity Scan")
    # Pre-defined high-potential gems for instant viewing
    gems = ["CRUS", "AMSC", "ALAB", "FLR", "VRT"]
    gem_data = get_market_data(gems)
    
    breakout_list = []
    for t in gems:
        try:
            high = gem_data[t]['High'].max()
            curr = gem_data[t]['Close'].iloc[-1]
            if curr >= (high * 0.97): # Within 3% of 5-day high
                breakout_list.append({"Ticker": t, "Price": f"${curr:.2f}", "Status": "🚀 BREAKING OUT"})
        except: continue
    st.table(pd.DataFrame(breakout_list))

st.divider()
st.caption("Strategy: Exit NVTS by Monday. Rotate into FIX/MTZ.")
