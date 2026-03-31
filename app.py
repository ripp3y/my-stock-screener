import streamlit as st
import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Mobile Setup
st.set_page_config(page_title="Alpha Terminal", layout="centered")

st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; }
    [data-testid="stLineChart"] { height: 200px !important; }
    div[data-testid="stExpander"] { border: 1px solid #333; margin-bottom: 4px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Watchlist & ETFs
watchlists = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}
benchmarks = {"Energy": "XLE", "Materials": "XLB", "Tech": "XLK", "Industrials": "XLI"}

# 3. Simple Data Fetcher
@st.cache_data(ttl=600)
def fetch_alpha_data():
    results = []
    sector_perf = {}
    
    for sector, etf in benchmarks.items():
        try:
            # Get 2-day history for change calculation
            s_data = yf.download(etf, period="2d", progress=False)['Close']
            if len(s_data) < 2: continue
            s_change = ((s_data.iloc[-1] - s_data.iloc[-2]) / s_data.iloc[-2]) * 100
            sector_perf[sector] = float(s_change)
            
            for ticker in watchlists[sector]:
                try:
                    t_data = yf.download(ticker, period="2d", progress=False)['Close']
                    if len(t_data) < 2: continue
                    t_price = float(t_data.iloc[-1])
                    t_change = ((t_data.iloc[-1] - t_data.iloc[-2]) / t_data.iloc[-2]) * 100
                    
                    results.append({
                        "Ticker": ticker, "Price": t_price, "Change": float(t_change),
                        "Sector": sector, "Alpha": float(t_change - s_change)
                    })
                except: continue
        except: continue
    
    # Create DF with hardcoded columns to prevent KeyError
    return pd.DataFrame(results, columns=["Ticker", "Price", "Change", "Sector", "Alpha"]), sector_perf

# Run Engine
df_all, sector_dict = fetch_alpha_data()

st.title("🛡️ Alpha Terminal")

# 4. Display Logic
if not sector_dict:
    st.warning("Syncing market data... please refresh in a moment.")
else:
    # Sort sectors by strength
    sorted_s = sorted(sector_dict.items(), key=lambda x: x[1], reverse=True)
    sel_label = st.selectbox("Market Strength:", [f"{s} ({p:+.2f}%)" for s, p in sorted_s])
    sel_name = sel_label.split(" (")[0]
    
    st.subheader(f"Ranked: {sel_name}")
    
    # Safely filter and sort
    df_v = df_all[df_all['Sector'] == sel_name].copy()
    if not df_v.empty:
        df_v = df_v.sort_values(by="Alpha", ascending=False)
        
        for _, row in df_v.iterrows():
            c = "green" if row['Change'] > 0 else "red"
            with st.expander(f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{c}[{row['Change']:+.2f}%]"):
                # Fetch chart only on click
                chart = yf.download(row['Ticker'], period="6m", progress=False)['Close']
                if not chart.empty:
                    st.line_chart(chart)
                else:
                    st.write("Chart data busy... try again.")
