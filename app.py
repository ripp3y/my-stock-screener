import streamlit as st
import yfinance as yf
import pandas as pd

# 1. VISUAL SETUP
st.set_page_config(page_title="Alpha Terminal", layout="centered")
st.markdown("""
    <style>
    .stAreaChart { height: 200px !important; }
    .stExpander { border: 1px solid #444 !important; border-radius: 8px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Define Sector Map (Note: PBR-A is more stable than PBR.A in 2026)
watchlists = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Energy": "XLE", "Materials": "XLB", "Tech": "XLK", "Industrials": "XLI"}

# 2. RUGGED DATA ENGINE (Handles Multi-Index & Rate Limits)
@st.cache_data(ttl=600)
def fetch_rugged_data(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    
    # Simple batch download without 'session' to avoid TypeError
    data = yf.download(tickers + [etf], period="5d", progress=False)
    
    if data.empty:
        return None, 0.0

    # Handling the 2026 Multi-Index structure
    # We flatten the columns to make math easier
    try:
        # Accessing only 'Close' prices
        close_prices = data['Close']
        etf_pc = ((close_prices[etf].iloc[-1] - close_prices[etf].iloc[-2]) / close_prices[etf].iloc[-2]) * 100
        
        results = []
        for t in tickers:
            if t in close_prices.columns:
                p_now = close_prices[t].iloc[-1]
                p_prev = close_prices[t].iloc[-2]
                change = ((p_now - p_prev) / p_prev) * 100
                results.append({
                    "Ticker": t, "Price": float(p_now), 
                    "Change": float(change), "Alpha": float(change - etf_pc)
                })
        return pd.DataFrame(results).sort_values(by="Alpha", ascending=False), etf_pc
    except Exception as e:
        st.error(f"Data Processing Error: {e}")
        return None, 0.0

# 3. INTERFACE
st.title("🛡️ Alpha Terminal")

# Manual reboot button for the cloud server
if st.button("🔄 Force App Reboot"):
    st.cache_data.clear()
    st.rerun()

sel_sector = st.selectbox("Market Sector:", list(watchlists.keys()))

with st.spinner("Connecting to Market..."):
    df, etf_val = fetch_rugged_data(sel_sector)

if df is not None:
    st.subheader(f"Ranked: {sel_sector} (Benchmark: {etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Change'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # LAZY LOAD: Fetch 6M data only when tapped
            if st.button(f"View {row['Ticker']} Trend", key=f"btn_{row['Ticker']}"):
                chart_raw = yf.download(row['Ticker'], period="6m", progress=False)
                if not chart_raw.empty:
                    # 'Mountain' style shaded chart
                    st.area_chart(chart_raw['Close'])
                else:
                    st.warning("Yahoo connection timeout. Please wait 10 seconds.")
else:
    st.info("Market data is temporarily unavailable. This often happens on shared cloud IPs. Tap 'Force App Reboot' above to try a new connection.")
