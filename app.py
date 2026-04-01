import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stAreaChart { height: 280px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 10px; }
    [data-testid="stMetricValue"] { font-size: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# Sector Config
watchlists = {
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"]
}
sector_etfs = {"Energy": "XLE", "Tech": "XLK", "Industrials": "XLI", "Materials": "XLB"}

# --- DATA ENGINE ---

@st.cache_data(ttl=300)
def get_snapshot(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    try:
        # Download 5d to ensure daily change calculation is possible
        data = yf.download(tickers + [etf], period="5d", progress=False)
        if data.empty: return pd.DataFrame(), 0.0
        
        close = data['Close']
        # Benchmark % Change
        bench_chg = ((close[etf].iloc[-1] - close[etf].iloc[-2]) / close[etf].iloc[-2]) * 100
        
        results = []
        for t in tickers:
            if t in close.columns:
                p_now, p_prev = close[t].iloc[-1], close[t].iloc[-2]
                if pd.isna(p_now): continue
                chg = ((p_now - p_prev) / p_prev) * 100
                results.append({"Ticker": t, "Price": p_now, "Chg": chg, "Alpha": chg - bench_chg})
        
        # Defensive check to prevent ValueError during sorting (cite: 1774998979672.jpeg)
        if not results: return pd.DataFrame(), 0.0
        return pd.DataFrame(results).sort_values("Alpha", ascending=False), bench_chg
    except Exception:
        return pd.DataFrame(), 0.0

@st.cache_data(ttl=600)
def get_chart(ticker):
    # Implementing a retry delay to handle JSONDecodeErrors (cite: image_7521d8.png)
    for attempt in range(3):
        try:
            # Using '6mo' as logs showed '6m' is an invalid parameter (cite: image_720628.png)
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty: return df['Close']
        except Exception:
            time.sleep(attempt + 1)
    return None

# --- UI MAIN ---
st.title("🛡️ Alpha Terminal")

col_a, col_b = st.columns([3, 1])
with col_a:
    sel_sector = st.selectbox("Market Sector:", list(watchlists.keys()))
with col_b:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

df_ranked, etf_val = get_snapshot(sel_sector)

if not df_ranked.empty:
    st.subheader(f"Momentum vs {sector_etfs[sel_sector]} ({etf_val:+.2f}%)")
    
    for _, row in df_ranked.iterrows():
        color = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # Automated lazy-loading to prevent connection timeouts (cite: image_71f9ed.png)
            chart_data = get_chart(row['Ticker'])
            if chart_data is not None:
                # Mountain chart style with shaded area (cite: image_751619.png)
                st.area_chart(chart_data)
            else:
                st.error("Yahoo link timed out. Tap 'Sync' and try again.")
else:
    st.info("🔄 Refreshing data feed...")
