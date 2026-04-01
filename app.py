import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Mobile CSS: Forces charts to a readable height and styles expanders
st.markdown("""
    <style>
    .stAreaChart { height: 250px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 8px; }
    [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# User-defined sectors
watchlists = {
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

# --- DATA ENGINES ---

@st.cache_data(ttl=300)
def get_market_state(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    
    try:
        # FIX: Removed 'session' to stop TypeError from image_71f2cb.png
        data = yf.download(tickers + [etf], period="5d", progress=False)
        
        # Defensive check for empty data (prevents ValueError in image_1774998979672.jpeg)
        if data.empty or 'Close' not in data:
            return pd.DataFrame(), 0.0
            
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
        
        # Final safety check before sorting
        if not ranks: return pd.DataFrame(), 0.0
        return pd.DataFrame(ranks).sort_values(by="Alpha", ascending=False), etf_pc
    except Exception as e:
        return pd.DataFrame(), 0.0

@st.cache_data(ttl=600)
def fetch_mountain_data(ticker):
    try:
        # FIX: Using '6mo' (valid) instead of '6m' (invalid) per image_720628.png
        df = yf.download(ticker, period="6mo", progress=False)
        return df['Close'] if not df.empty else None
    except:
        return None

# --- UI RENDER ---
st.title("🛡️ Alpha Terminal")

# Sync Button & Selector
col1, col2 = st.columns([3, 1])
with col1:
    sel_sector = st.selectbox("View Sector:", list(watchlists.keys()))
with col2:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

df, etf_val = get_market_state(sel_sector)

if not df.empty:
    st.subheader(f"Momentum vs {sector_etfs[sel_sector]} ({etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Chg'] > 0 else "red"
        # Star icon added to simulate your "Global Leaders" layout
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        # Load on click logic
        with st.expander(label):
            with st.spinner("Syncing chart..."):
                hist = fetch_mountain_data(row['Ticker'])
                
                # Check for None prevents the flat-line charts seen in your screenshots
                if hist is not None:
                    st.area_chart(hist)
                else:
                    st.error("Yahoo sync failed. Tap 'Sync' at the top to try again.")
else:
    st.info("Establishing data link... Tap 'Sync' if data doesn't appear shortly.")
