import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Advanced Mobile Optimization
st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Mobile UI fixes for dense viewing
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; line-height: 1.1 !important; }
    h1 { font-size: 1.4rem !important; margin-bottom: 0px !important; }
    .stButton>button { height: 2.2rem; font-size: 0.85rem; width: 100%; }
    hr { margin: 0.4rem 0px !important; }
    [data-testid="stLineChart"] { height: 220px !important; }
    div[data-testid="stExpander"] { border: 1px solid #444 !important; margin-bottom: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# Define Sector Map
watchlists = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Energy": "XLE", "Materials": "XLB", "Tech": "XLK", "Industrials": "XLI"}

@st.cache_data(ttl=300)
def fetch_sector_batch(sector_name):
    tickers = watchlists[sector_name]
    etf = sector_etfs[sector_name]
    
    # BATCH DOWNLOAD (The Fix)
    all_to_load = tickers + [etf]
    # We pull 5 days to ensure we have yesterday's close for % calculations
    raw = yf.download(all_to_load, period="5d", interval="1d", group_by='ticker', progress=False)
    
    if raw.empty:
        return None, None
    
    # Calculate ETF Baseline
    etf_data = raw[etf]
    etf_pc = ((etf_data['Close'].iloc[-1] - etf_data['Close'].iloc[-2]) / etf_data['Close'].iloc[-2]) * 100
    
    # Build Stock List
    results = []
    for t in tickers:
        try:
            t_data = raw[t]
            price = float(t_data['Close'].iloc[-1])
            change = ((t_data['Close'].iloc[-1] - t_data['Close'].iloc[-2]) / t_data['Close'].iloc[-2]) * 100
            results.append({
                "Ticker": t, "Price": price, "Change": float(change), 
                "Alpha": float(change - etf_pc)
            })
        except: continue
        
    return pd.DataFrame(results).sort_values(by="Alpha", ascending=False), etf_pc

st.title("🛡️ Alpha Terminal")

# Emergency Cache Clear
if st.button("🔄 Force Data Refresh"):
    st.cache_data.clear()
    st.rerun()

# 1. Sector Selection
sel_name = st.selectbox("Market Strength:", list(watchlists.keys()))

# 2. Load & Display
with st.spinner(f"Syncing {sel_name} Data..."):
    df, etf_val = fetch_sector_batch(sel_name)

if df is not None and not df.empty:
    st.subheader(f"Ranked: {sel_name} (Benchmark: {etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        c = "green" if row['Change'] > 0 else "red"
        # The Expander label now matches your "Alpha" goal
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{c}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # Fetch 6-month chart only when expanded to keep app fast
            with st.spinner("Fetching Chart..."):
                chart = yf.download(row['Ticker'], period="6m", progress=False)['Close']
                if not chart.empty:
                    st.line_chart(chart)
                else:
                    st.write("Chart sync pending... (Try refreshing)")
else:
    st.error("Connection Timeout or No Data. Please check your internet or tap Refresh.")
