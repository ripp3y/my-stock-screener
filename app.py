import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Mobile UI Tuning
st.markdown("""
    <style>
    .stExpander { border: 1px solid #444 !important; margin-bottom: 5px !important; }
    .stMarkdown { font-size: 0.9rem !important; }
    [data-testid="stLineChart"] { height: 200px !important; }
    </style>
    """, unsafe_allow_html=True)

watchlists = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Energy": "XLE", "Materials": "XLB", "Tech": "XLK", "Industrials": "XLI"}

# 1. Fetch only the core price/change data
@st.cache_data(ttl=300)
def get_sector_prices(sector_name):
    tickers = watchlists[sector_name]
    etf = sector_etfs[sector_name]
    all_ticks = tickers + [etf]
    
    # Download only the last 2 days for speed
    raw = yf.download(all_ticks, period="2d", group_by='ticker', progress=False)
    if raw.empty: return None, None
    
    etf_pc = ((raw[etf]['Close'].iloc[-1] - raw[etf]['Close'].iloc[-2]) / raw[etf]['Close'].iloc[-2]) * 100
    
    results = []
    for t in tickers:
        try:
            t_data = raw[t]
            price = t_data['Close'].iloc[-1]
            change = ((t_data['Close'].iloc[-1] - t_data['Close'].iloc[-2]) / t_data['Close'].iloc[-2]) * 100
            results.append({"Ticker": t, "Price": price, "Change": change, "Alpha": change - etf_pc})
        except: continue
    return pd.DataFrame(results).sort_values(by="Alpha", ascending=False), etf_pc

st.title("🛡️ Alpha Terminal")

sel_name = st.selectbox("Select Sector:", list(watchlists.keys()))

df, etf_val = get_sector_prices(sel_name)

if df is not None:
    st.subheader(f"Ranked: {sel_name} (Benchmark: {etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        c = "green" if row['Change'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{c}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        # KEY FIX: The expander now contains the logic to fetch the chart ONLY when opened
        with st.expander(label):
            if st.button(f"Load 6M Chart for {row['Ticker']}", key=row['Ticker']):
                with st.spinner("Fetching data..."):
                    # Specific download for the chosen stock only
                    chart_raw = yf.download(row['Ticker'], period="6m", progress=False)
                    if not chart_raw.empty:
                        st.line_chart(chart_raw['Close'])
                    else:
                        st.error("Data temporarily unavailable. Try again in a moment.")
else:
    st.warning("Data sync in progress... please refresh in a few seconds.")
