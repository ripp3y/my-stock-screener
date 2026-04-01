import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Custom CSS for the 'Mountain' chart height and expander styling
st.markdown("""
    <style>
    .stAreaChart { height: 220px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Define your target watchlists
watchlists = {
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

# CLEAN DATA ENGINE: No 'session' parameter to avoid the TypeError in your logs
@st.cache_data(ttl=600)
def get_alpha_snapshot(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    
    # Batch download 5 days for daily change calculation
    data = yf.download(tickers + [etf], period="5d", progress=False)
    
    if data.empty or 'Close' not in data:
        return None, 0.0

    close_data = data['Close']
    etf_pc = ((close_data[etf].iloc[-1] - close_data[etf].iloc[-2]) / close_data[etf].iloc[-2]) * 100
    
    results = []
    for t in tickers:
        try:
            p_now = close_data[t].iloc[-1]
            p_prev = close_data[t].iloc[-2]
            if pd.isna(p_now): continue
            
            change = ((p_now - p_prev) / p_prev) * 100
            results.append({
                "Ticker": t, "Price": float(p_now), 
                "Change": float(change), "Alpha": float(change - etf_pc)
            })
        except: continue
    
    return pd.DataFrame(results).sort_values(by="Alpha", ascending=False), etf_pc

# UI RENDER
st.title("🛡️ Alpha Terminal")

if st.button("🔄 Refresh Market Data"):
    st.cache_data.clear()
    st.rerun()

sel_sector = st.selectbox("Sector Focus:", list(watchlists.keys()))

with st.spinner(f"Ranking {sel_sector}..."):
    df, etf_val = get_alpha_snapshot(sel_sector)

if df is not None and not df.empty:
    st.subheader(f"Ranked vs {sector_etfs[sel_sector]} ({etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Change'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        # When you click this expander, the code inside runs immediately
        with st.expander(label):
            # The 'Load on Click' logic lives here
            with st.spinner(f"Fetching {row['Ticker']} History..."):
                try:
                    # Fetching 6M data for the 'Mountain' chart
                    # Using a clean download call to avoid the 'YfData' TypeError
                    hist = yf.download(row['Ticker'], period="6m", progress=False)
                    
                    if not hist.empty:
                        # st.area_chart creates the shaded 'Mountain' visual
                        st.area_chart(hist['Close'])
                    else:
                        st.error("Data temporarily unavailable from Yahoo.")
                except Exception as e:
                    st.error(f"Sync error: {e}")
else:
    st.info("Connection pending. Tap Refresh if data doesn't load in 5 seconds.")
