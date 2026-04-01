import streamlit as st
import yfinance as yf
import pandas as pd
import requests

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# 1. MOUNTAIN CHART CSS & UI
st.markdown("""
    <style>
    .stAreaChart { height: 220px !important; }
    .stExpander { border: 1px solid #444 !important; border-radius: 8px; margin-bottom: 6px; }
    div[data-testid="stExpander"] p { font-size: 0.95rem; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 2. BROWSER SIMULATION ENGINE
# This helps bypass the "Data temporarily unavailable" block
def get_stealth_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return session

watchlists = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Energy": "XLE", "Materials": "XLB", "Tech": "XLK", "Industrials": "XLI"}

@st.cache_data(ttl=600)
def fetch_market_state(sector_name):
    session = get_stealth_session()
    tickers = watchlists[sector_name]
    etf = sector_etfs[sector_name]
    
    # Fetch price data with session headers
    raw = yf.download(tickers + [etf], period="5d", session=session, progress=False, group_by='ticker')
    if raw.empty: return None, None
    
    etf_pc = ((raw[etf]['Close'].iloc[-1] - raw[etf]['Close'].iloc[-2]) / raw[etf]['Close'].iloc[-2]) * 100
    
    rows = []
    for t in tickers:
        try:
            t_data = raw[t]
            price = t_data['Close'].iloc[-1]
            change = ((t_data['Close'].iloc[-1] - t_data['Close'].iloc[-2]) / t_data['Close'].iloc[-2]) * 100
            rows.append({"Ticker": t, "Price": price, "Change": change, "Alpha": change - etf_pc})
        except: continue
    return pd.DataFrame(rows).sort_values(by="Alpha", ascending=False), etf_pc

# 3. APP INTERFACE
st.title("🛡️ Alpha Terminal")

sel_sector = st.selectbox("Market Strength:", list(watchlists.keys()))

df, etf_val = fetch_market_state(sel_sector)

if df is not None:
    st.subheader(f"Ranked: {sel_sector} (Benchmark: {etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Change'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # Unique key for every button to prevent state mix-ups
            if st.button(f"Generate Mountain Chart", key=f"btn_{row['Ticker']}"):
                with st.spinner("Decoding trend..."):
                    # Use the stealth session for the chart download too
                    sess = get_stealth_session()
                    chart_data = yf.download(row['Ticker'], period="6m", session=sess, progress=False)['Close']
                    
                    if not chart_data.empty:
                        # st.area_chart creates the shaded 'Mountain' effect
                        st.area_chart(chart_data)
                    else:
                        st.error("Yahoo connection reset. Tap again in 5 seconds.")
else:
    st.info("Terminal initializing... Please wait 10 seconds.")
