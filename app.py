import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# --- MOBILE STYLING ---
st.markdown("""
    <style>
    .stAreaChart { height: 280px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

watchlists = {
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Energy": "XLE", "Tech": "XLK", "Industrials": "XLI"}

# --- HARDENED DATA ENGINE ---

@st.cache_data(ttl=300)
def get_market_snapshot(sector_name):
    tickers = watchlists[sector_name]
    etf = sector_etfs[sector_name]
    
    try:
        # Standardize download to '5d' to ensure enough data for change calculation
        data = yf.download(tickers + [etf], period="5d", progress=False)
        
        if data.empty or 'Close' not in data:
            return pd.DataFrame(), 0.0
            
        close = data['Close']
        # Benchmark % Change calculation
        etf_pc = ((close[etf].iloc[-1] - close[etf].iloc[-2]) / close[etf].iloc[-2]) * 100
        
        ranks = []
        for t in tickers:
            if t in close.columns:
                p_now, p_prev = close[t].iloc[-1], close[t].iloc[-2]
                if pd.isna(p_now): continue
                chg = ((p_now - p_prev) / p_prev) * 100
                ranks.append({"Ticker": t, "Price": p_now, "Chg": chg, "Alpha": chg - etf_pc})
        
        # FIX: Check for empty results to prevent ValueError sorting crash (cite: 1774998979672.jpeg)
        if not ranks:
            return pd.DataFrame(), 0.0
            
        return pd.DataFrame(ranks).sort_values(by="Alpha", ascending=False), etf_pc
    except Exception:
        return pd.DataFrame(), 0.0

@st.cache_data(ttl=600)
def fetch_mountain_chart(ticker):
    # Retry mechanism to bypass temporary API throttling (cite: image_7521d8.png)
    for attempt in range(3):
        try:
            # FIX: Change '6m' (invalid) to '6mo' (valid) (cite: image_720628.png)
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty and 'Close' in df:
                return df['Close']
        except Exception:
            time.sleep(attempt + 1) # Exponential backoff
    return None

# --- TERMINAL UI ---
st.title("🛡️ Alpha Terminal")

if st.button("🔄 Sync Feed"):
    st.cache_data.clear()
    st.rerun()

sel_sector = st.selectbox("Select Sector:", list(watchlists.keys()))
df_ranked, bench_pc = get_market_snapshot(sel_sector)

if not df_ranked.empty:
    st.subheader(f"Momentum vs {sector_etfs[sel_sector]} ({bench_pc:+.2f}%)")
    
    for _, row in df_ranked.iterrows():
        status_color = "green" if row['Chg'] > 0 else "red"
        header = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{status_color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(header):
            # Automated lazy-loading prevents mass-request timeouts (cite: image_71f9ed.png)
            with st.spinner(f"Fetching {row['Ticker']}..."):
                chart_data = fetch_mountain_chart(row['Ticker'])
                if chart_data is not None:
                    # Renders the shaded Mountain Chart seen in stable views (cite: image_753403.png)
                    st.area_chart(chart_data)
                else:
                    st.warning("Yahoo connection timed out. Please try again later.")
else:
    st.info("🔄 Connecting to data source... If this persists, tap 'Sync Feed'.")
