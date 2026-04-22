import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [SYSTEM CONFIG] ---
st.set_page_config(page_title="Radar v5.20", layout="wide")

# --- [INSTITUTIONAL DATA LOADER] ---
@st.cache_data(ttl=86400)
def load_market_master():
    # Fetching a master list that includes Ticker, Name, Sector, and Market Cap
    url = "https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/all.csv"
    try:
        df = pd.read_csv(url)
        # Standardizing column names for the filter logic
        df.columns = [c.lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['symbol', 'name', 'sector', 'marketcap'])

def get_live_data(tickers):
    if not tickers: return None
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [INITIALIZATION] ---
master_df = load_market_master()

# --- [UI HEADER] ---
st.title("📡 Radar v5.20")
st.sidebar.header("🛡️ Institutional Filters")

# 1. Market Cap Filter (e.g., Only Mid/Large Cap)
min_cap = st.sidebar.number_input("Min Market Cap ($ Billions):", value=1.0, step=0.5) * 1_000_000_000

# 2. Sector Filter
all_sectors = ["All"] + sorted([str(s) for s in master_df['sector'].unique() if str(s) != 'nan'])
selected_sector = st.sidebar.selectbox("Filter by Sector:", all_sectors)

# --- [TABBED INTERFACE] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["SNDK", "MRVL", "STX", "FIX", "NVTS", "MTZ", "CIEN"]
    data = get_live_data(portfolio)
    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            recon_list.append({"Ticker": t, "Price": f"${curr:.2f}"})
        except: continue
    st.table(pd.DataFrame(recon_list))

# --- [TAB 2: ALPHA (FILTERED SEARCH)] ---
with tab_alpha:
    st.subheader("Filtered Alpha Scan")
    
    # Applying the Filters
    filtered_df = master_df[master_df['marketcap'] >= min_cap]
    if selected_sector != "All":
        filtered_df = filtered_df[filtered_df['sector'] == selected_sector]
    
    ticker_options = filtered_df['symbol'].tolist()
    st.write(f"Showing {len(ticker_options)} stocks matching your criteria.")
    
    picks = st.multiselect("Active Watchlist:", ticker_options, default=ticker_options[:5])
    
    if picks:
        s_data = get_live_data(picks)
        results = []
        for p in picks:
            try:
                price = s_data[p]['Close'].iloc[-1]
                results.append({"Ticker": p, "Price": f"${price:.2f}", "Status": "🔥 SCANNING"})
            except: continue
        st.dataframe(pd.DataFrame(results), use_container_width=True)

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("Blue Sky Leads")
    # Using FIX, MTZ, and ALAB as the benchmark breakout leads
    gems = ["FIX", "MTZ", "ALAB", "CRUS", "VRT"]
    gem_data = get_live_data(gems)
    for g in gems:
        try:
            st.write(f"**{g}** | Current: ${gem_data[g]['Close'].iloc[-1]:.2f}")
        except: continue

st.divider()
st.caption(f"Filters Active: Min ${min_cap/1e9}B Cap | Sector: {selected_sector}")
