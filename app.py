import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# CSS to make the app feel like a native mobile tool
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; }
    .stButton>button { height: 2.2rem; font-size: 0.85rem; width: 100%; }
    [data-testid="stLineChart"] { height: 180px !important; }
    div[data-testid="stExpander"] { border: 1px solid #333; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

sectors = {
    "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI", "Tech": "XLK",
    "Financials": "XLF", "Health Care": "XLV", "Cons. Discretionary": "XLY",
    "Cons. Staples": "XLP", "Utilities": "XLU", "Real Estate": "XLRE", "Communication": "XLC"
}

sector_stocks = {
    "Energy": ["PBR-A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}

# 1. Faster Data Engine
@st.cache_data(ttl=600)
def get_market_snapshot():
    all_stocks = []
    s_perf = []
    
    for s_name, s_ticker in sectors.items():
        try:
            s_data = yf.download(s_ticker, period="5d", progress=False)
            if s_data.empty: continue
            
            s_pc = ((s_data['Close'].iloc[-1] - s_data['Close'].iloc[-2]) / s_data['Close'].iloc[-2]) * 100
            s_perf.append({"Name": s_name, "PC": float(s_pc)})
            
            if s_name in sector_stocks:
                for t in sector_stocks[s_name]:
                    try:
                        t_data = yf.download(t, period="5d", progress=False)
                        if t_data.empty: continue
                        price = float(t_data['Close'].iloc[-1])
                        change = float(((t_data['Close'].iloc[-1] - t_data['Close'].iloc[-2]) / t_data['Close'].iloc[-2]) * 100)
                        all_stocks.append({
                            "Ticker": t, "Price": price, "Change": change, 
                            "Sector": s_name, "Alpha": change - s_pc
                        })
                    except: continue
        except: continue
        
    return pd.DataFrame(all_stocks), pd.DataFrame(s_perf).sort_values(by="PC", ascending=False)

df_all, df_s_perf = get_market_snapshot()

st.title("🛡️ Alpha Terminal")

# 2. SECTOR VIEW
if not df_s_perf.empty:
    s_labels = [f"{r['Name']} ({r['PC']:+.2f}%)" for _, r in df_s_perf.iterrows()]
    sel_label = st.selectbox("Market Strength:", s_labels)
    sel_name = sel_label.split(" (")[0]
    
    df_v = df_all[df_all['Sector'] == sel_name].sort_values(by="Alpha", ascending=False)
    
    for _, row in df_v.iterrows():
        c = "green" if row['Change'] > 0 else "red"
        # The key fix: Fetching data inside the expander only when needed
        with st.expander(f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{c}[{row['Change']:+.2f}%]"):
            with st.spinner('Loading Chart...'):
                # We pull 6 months, but keep the request 'Close' only to stay light
                chart_data = yf.download(row['Ticker'], period="6m", progress=False)['Close']
                if not chart_data.empty:
                    st.line_chart(chart_data)
                else:
                    st.write("Data sync failed. Try again.")
