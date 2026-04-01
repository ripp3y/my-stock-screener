import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# CSS to fix chart height for mobile and style expanders
st.markdown("""
    <style>
    .stAreaChart { height: 250px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Configuration for watchlists and benchmarks
watchlists = {
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

# --- DATA ENGINES ---

# FIX: Removed 'session' to stop the TypeError seen in image_71f2cb.png
@st.cache_data(ttl=300)
def get_market_state(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    
    try:
        data = yf.download(tickers + [etf], period="5d", progress=False)
        if data.empty or 'Close' not in data:
            return None, 0.0
            
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
    except Exception as e:
        st.error(f"Snapshot Error: {e}")
        return None, 0.0

# FIX: Period changed from '6m' (invalid) to '6mo' (valid) per image_720628.png
@st.cache_data(ttl=600)
def fetch_mountain_data(ticker):
    try:
        return yf.download(ticker, period="6mo", progress=False)
    except:
        return pd.DataFrame()

# --- UI START ---
st.title("🛡️ Alpha Terminal")

# Main action row
col1, col2 = st.columns([3, 1])
with col1:
    sel_sector = st.selectbox("Sector Focus:", list(watchlists.keys()))
with col2:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

df, etf_val = get_market_state(sel_sector)

if df is not None and not df.empty:
    st.subheader(f"Momentum vs {sector_etfs[sel_sector]} ({etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        # Everything inside this with block loads only when the expander is opened
        with st.expander(label):
            with st.spinner(f"Pulling {row['Ticker']} data..."):
                hist = fetch_mountain_data(row['Ticker'])
                
                # Check if data exists before plotting to avoid the empty chart in image 1000029618.jpg
                if not hist.empty and 'Close' in hist:
                    st.area_chart(hist['Close'])
                else:
                    st.error("Market data sync failed. Check your connection.")
else:
    st.warning("Establishing data link... Tap 'Sync' if data is missing.")
