import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Fixes the chart height for mobile viewing
st.markdown("""
    <style>
    .stAreaChart { height: 250px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Your target sectors and tickers
watchlists = {
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

@st.cache_data(ttl=300)
def get_market_snapshot(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    
    # Batch download only 5 days of data for the ranking list
    # Removed 'session' to fix the TypeError in your logs
    data = yf.download(tickers + [etf], period="5d", progress=False)
    
    if data.empty: return None, 0.0

    close = data['Close']
    etf_pc = ((close[etf].iloc[-1] - close[etf].iloc[-2]) / close[etf].iloc[-2]) * 100
    
    ranks = []
    for t in tickers:
        try:
            p_now = close[t].iloc[-1]
            p_prev = close[t].iloc[-2]
            if pd.isna(p_now): continue
            
            chg = ((p_now - p_prev) / p_prev) * 100
            ranks.append({"Ticker": t, "Price": p_now, "Chg": chg, "Alpha": chg - etf_pc})
        except: continue
    
    return pd.DataFrame(ranks).sort_values(by="Alpha", ascending=False), etf_pc

# --- UI START ---
st.title("🛡️ Alpha Terminal")

# Clears the 'Pending' loops if the app gets stuck
if st.button("🔄 Hard Reset Connection"):
    st.cache_data.clear()
    st.rerun()

sel_sector = st.selectbox("Focus Sector:", list(watchlists.keys()))

with st.spinner("Ranking Momentum..."):
    df, etf_val = get_market_snapshot(sel_sector)

if df is not None:
    st.subheader(f"Ranked vs {sector_etfs[sel_sector]} ({etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # This is the "Load as we click" trigger
            if st.button(f"Load 6M Mountain Chart ({row['Ticker']})"):
                with st.spinner("Syncing with Yahoo..."):
                    # FIX: Changed '6m' to '6mo' to resolve your invalid period error
                    hist = yf.download(row['Ticker'], period="6mo", progress=False)
                    
                    if not hist.empty:
                        # st.area_chart creates the shaded 'Mountain' look you wanted
                        st.area_chart(hist['Close'])
                    else:
                        st.error("Connection lost. Tap again in 5s.")
else:
    st.warning("Data sync pending. Try the 'Hard Reset' button above.")
