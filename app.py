import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# --- MOBILE OPTIMIZATION ---
st.markdown("""
    <style>
    .stAreaChart { height: 280px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 8px; }
    [data-testid="stMetricValue"] { font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# Sector definitions
watchlists = {
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

# --- DATA ENGINE ---

@st.cache_data(ttl=300)
def get_market_state(sector_name):
    tickers = watchlists[sector_name]
    etf = sector_etfs[sector_name]
    
    try:
        # Standardize period to '5d' for daily change calculations
        data = yf.download(tickers + [etf], period="5d", progress=False)
        
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
        
        # FIX: Added empty check to prevent ValueError (cite: 1774998979672.jpeg)
        if not ranks:
            return pd.DataFrame(), 0.0
            
        return pd.DataFrame(ranks).sort_values(by="Alpha", ascending=False), etf_pc
    except Exception:
        return pd.DataFrame(), 0.0

@st.cache_data(ttl=600)
def fetch_chart_data(ticker):
    # Retry loop to handle Yahoo Finance JSONDecodeErrors (cite: image_7521d8.png)
    for _ in range(3):
        try:
            # FIX: Use '6mo' (valid) instead of '6m' (invalid) (cite: image_720628.png)
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty: return df['Close']
        except:
            time.sleep(1)
    return None

# --- UI RENDER ---
st.title("🛡️ Alpha Terminal")

# Navigation
col1, col2 = st.columns([3, 1])
with col1:
    sel_sector = st.selectbox("Sector:", list(watchlists.keys()))
with col2:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

df, bench_pc = get_market_state(sel_sector)

if not df.empty:
    st.subheader(f"Ranked vs {sector_etfs[sel_sector]} ({bench_pc:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # Load on expand prevents mass-request throttling (cite: image_71f9ed.png)
            chart = fetch_chart_data(row['Ticker'])
            if chart is not None:
                st.area_chart(chart)
            else:
                st.warning("Data link temporary unavailable. Try again in a moment.")
else:
    st.info("🔄 Syncing market data... If results don't appear, tap 'Sync' above.")
