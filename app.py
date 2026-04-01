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
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Tech": "XLK", "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI"}

# --- ROBUST DATA ENGINE ---

@st.cache_data(ttl=300)
def fetch_sector_snapshot(sector_name):
    tickers = watchlists[sector_name]
    etf = sector_etfs[sector_name]
    
    # Standard batch download (5d to get yesterday's close)
    data = yf.download(tickers + [etf], period="5d", progress=False)
    
    if data.empty or 'Close' not in data:
        return pd.DataFrame(), 0.0
        
    close = data['Close']
    try:
        etf_pc = ((close[etf].iloc[-1] - close[etf].iloc[-2]) / close[etf].iloc[-2]) * 100
        
        results = []
        for t in tickers:
            if t in close.columns:
                p_now, p_prev = close[t].iloc[-1], close[t].iloc[-2]
                if pd.isna(p_now): continue
                chg = ((p_now - p_prev) / p_prev) * 100
                results.append({"Ticker": t, "Price": p_now, "Chg": chg, "Alpha": chg - etf_pc})
        
        return pd.DataFrame(results).sort_values(by="Alpha", ascending=False), etf_pc
    except:
        return pd.DataFrame(), 0.0

# NEW: Retry logic to beat the JSONDecodeError/Throttling
@st.cache_data(ttl=600)
def get_chart_with_retry(ticker, retries=3):
    for i in range(retries):
        try:
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty and 'Close' in df:
                return df['Close']
        except Exception:
            time.sleep(1) # Pause before retry
            continue
    return None

# --- UI ---
st.title("🛡️ Alpha Terminal")

if st.button("🔄 Clear Cache & Sync"):
    st.cache_data.clear()
    st.rerun()

sel_sector = st.selectbox("Market Sector:", list(watchlists.keys()))
df_ranked, benchmark = fetch_sector_snapshot(sel_sector)

if not df_ranked.empty:
    st.subheader(f"Momentum vs {sector_etfs[sel_sector]} ({benchmark:+.2f}%)")
    
    for _, row in df_ranked.iterrows():
        status = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{status}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # CHARTS LOAD AUTOMATICALLY ON CLICK HERE
            with st.spinner(f"Requesting {row['Ticker']}..."):
                chart_data = get_chart_with_retry(row['Ticker'])
                
                if chart_data is not None:
                    # Renders the shaded 'Mountain' chart
                    st.area_chart(chart_data)
                else:
                    st.error("Yahoo Finance blocked the request. Try again in a minute.")
else:
    st.info("Syncing... If it takes more than 10s, Yahoo may be throttling the server.")
