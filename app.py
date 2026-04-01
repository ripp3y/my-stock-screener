import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# CSS to make the 'Mountain' charts look professional on mobile
st.markdown("""
    <style>
    .stAreaChart { height: 250px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Sector & Ticker Definitions
watchlists = {
    "Energy": ["SLB", "EQNR", "COP", "PBR-A", "XOM", "CVX", "PTEN", "OVV"],
    "Tech": ["LRCX", "NVDA", "AVGO", "MU", "ASX", "AMD", "MSFT", "AAPL"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Energy": "XLE", "Tech": "XLK", "Industrials": "XLI"}

# --- CACHED DATA ENGINE ---

@st.cache_data(ttl=300)
def get_snapshot(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    # Batch download 5 days for daily change calculation
    data = yf.download(tickers + [etf], period="5d", progress=False)
    if data.empty: return pd.DataFrame(), 0.0
    
    close = data['Close']
    etf_pc = ((close[etf].iloc[-1] - close[etf].iloc[-2]) / close[etf].iloc[-2]) * 100
    
    results = []
    for t in tickers:
        if t in close.columns:
            p_now, p_prev = close[t].iloc[-1], close[t].iloc[-2]
            if pd.isna(p_now): continue
            chg = ((p_now - p_prev) / p_prev) * 100
            results.append({"Ticker": t, "Price": p_now, "Chg": chg, "Alpha": chg - etf_pc})
    
    if not results: return pd.DataFrame(), 0.0
    return pd.DataFrame(results).sort_values("Alpha", ascending=False), etf_pc

@st.cache_data(ttl=600)
def get_mountain_chart(ticker):
    # Retry loop to handle the JSONDecodeError seen in your logs
    for attempt in range(3):
        try:
            # FIX: Using '6mo' instead of '6m' to avoid invalid parameter errors
            df = yf.download(ticker, period="6mo", progress=False)
            if not df.empty: return df['Close']
        except:
            time.sleep(1)
    return None

# --- UI RENDER ---
st.title("🛡️ Alpha Terminal")

col_left, col_right = st.columns([3, 1])
with col_left:
    sel_sector = st.selectbox("Focus:", list(watchlists.keys()))
with col_right:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

df, bench_val = get_snapshot(sel_sector)

if not df.empty:
    st.subheader(f"Ranked vs {sector_etfs[sel_sector]} ({bench_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Chg'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Chg']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        # CHARTS LOAD HERE: Only when the user clicks the ticker
        with st.expander(label):
            with st.spinner(f"Pulling {row['Ticker']}..."):
                chart_data = get_mountain_chart(row['Ticker'])
                if chart_data is not None:
                    # Renders the shaded 'Mountain' visual
                    st.area_chart(chart_data)
                else:
                    st.error("Yahoo sync pending. Try again in a moment.")
else:
    st.info("🔄 Refreshing data link...")
