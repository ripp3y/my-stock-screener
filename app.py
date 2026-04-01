import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# CSS to fix the mobile 'Black Box' chart issue
st.markdown("""
    <style>
    .stAreaChart { height: 220px !important; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px; margin-bottom: 5px; }
    div[data-testid="stExpander"] p { font-size: 0.9rem; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

watchlists = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
sector_etfs = {"Energy": "XLE", "Materials": "XLB", "Tech": "XLK", "Industrials": "XLI"}

# 1. CLEAN DATA ENGINE (Bypasses the 'session' TypeError)
@st.cache_data(ttl=600)
def get_clean_alpha_data(sector):
    tickers = watchlists[sector]
    etf = sector_etfs[sector]
    
    # We download 5 days to ensure the % change calculation has a baseline
    # Removing 'session' parameter to fix the YfData __init__ TypeError
    data = yf.download(tickers + [etf], period="5d", progress=False)
    
    if data.empty or 'Close' not in data:
        return None, 0.0

    close_data = data['Close']
    etf_pc = ((close_data[etf].iloc[-1] - close_data[etf].iloc[-2]) / close_data[etf].iloc[-2]) * 100
    
    results = []
    for t in tickers:
        try:
            # Multi-index safe retrieval
            p_now = close_data[t].iloc[-1]
            p_prev = close_data[t].iloc[-2]
            if pd.isna(p_now) or pd.isna(p_prev): continue
            
            change = ((p_now - p_prev) / p_prev) * 100
            results.append({
                "Ticker": t, "Price": float(p_now), 
                "Change": float(change), "Alpha": float(change - etf_pc)
            })
        except: continue
    
    return pd.DataFrame(results).sort_values(by="Alpha", ascending=False), etf_pc

# 2. UI RENDER
st.title("🛡️ Alpha Terminal")

# Critical for clearing the 'Pending' loops
if st.button("🔄 Sync Connection"):
    st.cache_data.clear()
    st.rerun()

sel_name = st.selectbox("Market Focus:", list(watchlists.keys()))

with st.spinner(f"Decoding {sel_name} Sector..."):
    df, etf_val = get_clean_alpha_data(sel_name)

if df is not None and not df.empty:
    st.subheader(f"Ranked vs {sector_etfs[sel_name]} ({etf_val:+.2f}%)")
    
    for _, row in df.iterrows():
        color = "green" if row['Change'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            # Click-to-load prevents the 'Too Many Requests' block from Yahoo
            if st.button(f"Load Mountain Chart ({row['Ticker']})", key=f"btn_{row['Ticker']}"):
                with st.spinner("Drawing Trend..."):
                    chart_raw = yf.download(row['Ticker'], period="6m", progress=False)
                    if not chart_raw.empty:
                        # st.area_chart provides the Yahoo-style shaded 'Mountain' look
                        st.area_chart(chart_raw['Close'])
                    else:
                        st.warning("Yahoo connection timed out. Wait 10s and tap again.")
else:
    st.error("Terminal offline. Tap 'Sync Connection' above to retry.")
