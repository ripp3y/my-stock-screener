import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# CSS to optimize the 'Mountain' chart for mobile
st.markdown("""
    <style>
    .stAreaChart { height: 250px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Sector & Ticker configuration
watchlists = {
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

# FIX: Removed 'session' to stop the TypeError in your logs
@st.cache_data(ttl=300)
def get_snapshot(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    data = yf.download(tickers + [etf], period="5d", progress=False)
    if data.empty: return None, 0.0
    close = data['Close']
    etf_pc = ((close[etf].iloc[-1] - close[etf].iloc[-2]) / close[etf].iloc[-2]) * 100
    ranks = []
    for t in tickers:
        try:
            p_now, p_prev = close[t].iloc[-1], close[t].iloc[-2]
            if pd.isna(p_now): continue
            chg = ((p_now - p_prev) / p_prev) * 100
            ranks.append({"Ticker": t, "Price": p_now, "Chg": chg, "Alpha": chg - etf_pc})
        except: continue
    return pd.DataFrame(ranks).sort_values(by="Alpha", ascending=False), etf_pc

# NEW: Cached function for the 6-Month Mountain Chart
# FIX: Using '6mo' (correct) instead of '6m' (invalid)
@st.cache_data(ttl=600)
def fetch_mountain_data(ticker):
    return yf.download(ticker, period="6mo", progress=False)

# --- UI RENDER ---
st.title("🛡️ Alpha Terminal")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

sel_sector = st.selectbox("Market Focus:", list(watchlists.keys()))
df, etf_val = get_snapshot(sel_sector)

if df is not None:
    st.subheader(f"Ranked vs {sector_etfs[sel_sector]} ({etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        # 'Load as we click' - Code inside runs when expander is toggled
        with st.expander(label):
            with st.spinner(f"Drawing {row['Ticker']}..."):
                hist = fetch_mountain_data(row['Ticker'])
                if not hist.empty:
                    # st.area_chart creates the shaded 'Mountain' look
                    st.area_chart(hist['Close'])
                else:
                    st.error("Yahoo sync failed. Try refreshing the terminal.")
else:
    st.info("Syncing market feed... Tap Refresh if data doesn't appear.")
