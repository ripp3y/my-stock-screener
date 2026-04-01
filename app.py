import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# --- MOBILE UI OPTIMIZATION ---
st.markdown("""
    <style>
    /* Force charts to a readable mobile height */
    .stAreaChart { height: 280px !important; }
    /* Style expanders for easier thumb-tapping */
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 10px; }
    [data-testid="stMetricValue"] { font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# Define sector groupings directly to avoid filtering KeyErrors
watchlists = {
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

# --- DEFENSIVE DATA ENGINE ---

@st.cache_data(ttl=300)
def get_market_state(sector_name):
    tickers = watchlists[sector_name]
    etf = sector_etfs[sector_name]
    
    try:
        # Fetch 5 days to ensure we have a 'previous' close for change calculation
        data = yf.download(tickers + [etf], period="5d", progress=False)
        
        if data.empty or 'Close' not in data:
            return pd.DataFrame(), 0.0
            
        close_prices = data['Close']
        
        # Calculate ETF benchmark performance
        etf_pc = ((close_prices[etf].iloc[-1] - close_prices[etf].iloc[-2]) / close_prices[etf].iloc[-2]) * 100
        
        performance_list = []
        for t in tickers:
            try:
                # Use .iloc[-1] and -2 to ensure we have valid price points
                p_now = close_prices[t].iloc[-1]
                p_prev = close_prices[t].iloc[-2]
                
                if pd.isna(p_now) or pd.isna(p_prev):
                    continue
                    
                chg = ((p_now - p_prev) / p_prev) * 100
                performance_list.append({
                    "Ticker": t, 
                    "Price": p_now, 
                    "Chg": chg, 
                    "Alpha": chg - etf_pc
                })
            except:
                continue
        
        # Guard against ValueError during sorting (image_1774998979672.jpeg)
        if not performance_list:
            return pd.DataFrame(), 0.0
            
        return pd.DataFrame(performance_list).sort_values(by="Alpha", ascending=False), etf_pc
    except Exception:
        return pd.DataFrame(), 0.0

@st.cache_data(ttl=600)
def get_historical_chart(ticker):
    try:
        # Period '6mo' is the correct API format (image_720628.png)
        df = yf.download(ticker, period="6mo", progress=False)
        return df['Close'] if not df.empty else None
    except:
        return None

# --- UI LAYOUT ---
st.title("🛡️ Alpha Terminal")

# Navigation and Sync
col1, col2 = st.columns([3, 1])
with col1:
    selected_sector = st.selectbox("Market Sector:", list(watchlists.keys()))
with col2:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

# Processing
df_ranked, bench_val = get_market_state(selected_sector)

if not df_ranked.empty:
    st.subheader(f"Ranked: {selected_sector} (vs {sector_etfs[selected_sector]} {bench_val:+.2f}%)")
    
    for _, row in df_ranked.iterrows():
        # Dynamic coloring for mobile readability
        status_color = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{status_color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # Fetch chart ONLY when expanded to save mobile bandwidth
            chart_data = get_historical_chart(row['Ticker'])
            if chart_data is not None:
                st.area_chart(chart_data)
            else:
                st.warning("Chart data sync pending... try refreshing.")
else:
    st.info("🔄 Connecting to market data... Tap 'Sync' if results don't load.")
