import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Mobile Optimization
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; }
    [data-testid="stLineChart"] { height: 180px !important; }
    div[data-testid="stExpander"] { border: 1px solid #333; margin-bottom: 4px; }
    </style>
    """, unsafe_allow_html=True)

# Define Watchlist
sector_map = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
etfs = {"Energy": "XLE", "Materials": "XLB", "Tech": "XLK", "Industrials": "XLI"}

# 1. THE DATA ENGINE (With NaN Protection)
@st.cache_data(ttl=600)
def get_market_data():
    all_data = []
    s_perf = {}
    
    for s_name, etf_tick in etfs.items():
        try:
            # Get Sector Baseline
            e_h = yf.download(etf_tick, period="5d", progress=False)
            if e_h.empty: continue
            s_ch = ((e_h['Close'].iloc[-1] - e_h['Close'].iloc[-2]) / e_h['Close'].iloc[-2]) * 100
            s_perf[s_name] = float(s_ch)
            
            # Get Individual Stocks
            for t in sector_map[s_name]:
                try:
                    t_h = yf.download(t, period="5d", progress=False)
                    if t_h.empty: continue
                    price = float(t_h['Close'].iloc[-1])
                    ch = ((t_h['Close'].iloc[-1] - t_h['Close'].iloc[-2]) / t_h['Close'].iloc[-2]) * 100
                    
                    all_data.append({
                        "Ticker": t, "Price": price, "Change": float(ch), 
                        "Sector": s_name, "Alpha": float(ch - s_ch)
                    })
                except: continue
        except: continue
    
    df = pd.DataFrame(all_data)
    # Protection against the ValueError: Drop any row with missing math
    if not df.empty:
        df = df.dropna(subset=['Alpha'])
        
    return df, s_perf

df_all, s_perf_dict = get_market_data()

st.title("🛡️ Alpha Terminal")

# 2. SECTOR SELECTION
if s_perf_dict:
    # Sort sectors by performance
    sorted_sectors = sorted(s_perf_dict.items(), key=lambda x: x[1], reverse=True)
    options = [f"{s} ({p:+.2f}%)" for s, p in sorted_sectors]
    sel_label = st.selectbox("Select Sector:", options)
    sel_name = sel_label.split(" (")[0]
    
    # 3. STOCK LISTING
    st.subheader(f"Ranked: {sel_name}")
    df_v = df_all[df_all['Sector'] == sel_name].sort_values(by="Alpha", ascending=False)
    
    for _, row in df_v.iterrows():
        color = "green" if row['Change'] > 0 else "red"
        label = f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%]"
        
        with st.expander(label):
            # Only download chart when tapped
            with st.spinner("Fetching Chart..."):
                c_data = yf.download(row['Ticker'], period="6m", progress=False)['Close']
                if not c_data.empty:
                    st.line_chart(c_data)
                else:
                    st.write("Chart data unavailable.")
