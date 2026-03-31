import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Config for tight mobile layout
st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Custom CSS to shrink fonts and margins for "At-A-Glance" viewing
st.markdown("""
    <style>
    .stMarkdown { font-size: 0.85rem !important; line-height: 1.2 !important; }
    h3 { font-size: 1.1rem !important; margin-bottom: 0px !important; }
    .stButton>button { height: 2.5rem; font-size: 0.9rem; }
    div[data-testid="stMetric"] { padding: 0px; }
    hr { margin: 0.5rem 0px !important; }
    </style>
    """, unsafe_allow_html=True)

sectors = {
    "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI", "Tech": "XLK",
    "Financials": "XLF", "Health Care": "XLV", "Cons. Discretionary": "XLY",
    "Cons. Staples": "XLP", "Utilities": "XLU", "Real Estate": "XLRE", "Communication": "XLC"
}

sector_stocks = {
    "Energy": ["PBR.A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Financials": ["JPM", "BAC", "MS", "GS", "WFC", "V", "MA", "AXP"],
    "Health Care": ["LLY", "UNH", "JNJ", "ABBV", "MRK", "TMO", "PFE", "AMGN"],
    "Cons. Discretionary": ["AMZN", "TSLA", "HD", "NKE", "MCD", "SBUX", "BKNG", "TJX"],
    "Cons. Staples": ["PG", "KO", "PEP", "COST", "WMT", "PM", "EL", "MO"],
    "Utilities": ["NEE", "SO", "DUK", "CEG", "SRE", "AEP", "D", "FE"],
    "Real Estate": ["PLD", "AMT", "EQIX", "CCI", "WY", "PSA", "DLR", "VICI"],
    "Communication": ["META", "GOOGL", "NFLX", "DIS", "TMUS", "VZ", "T", "CHTR"]
}

@st.cache_data(ttl=300)
def get_market_data():
    s_perf = []
    for name, tick in sectors.items():
        try:
            h = yf.Ticker(tick).history(period="2d")
            pc = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
            s_perf.append({"Name": name, "PC": pc})
        except: s_perf.append({"Name": name, "PC": 0.0})
    
    # Sort sectors by performance
    s_df = pd.DataFrame(s_perf).sort_values(by="PC", ascending=False)
    
    all_stocks = []
    for _, s_row in s_df.iterrows():
        s_name = s_row['Name']
        s_base = s_row['PC']
        for t in sector_stocks[s_name]:
            try:
                obj = yf.Ticker(t)
                h = obj.history(period="2d")
                price = h['Close'].iloc[-1]
                change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                all_stocks.append({
                    "Ticker": t, "Price": price, "Change": change, 
                    "Sector": s_name, "Alpha": change - s_base
                })
            except: continue
    return pd.DataFrame(all_stocks), s_df

df_all, df_s_perf = get_market_data()

# 4. Interface
st.title("🏆 The Best")
if st.button("SHOW TOP 10 GLOBAL LEADERS"):
    top_10 = df_all.sort_values(by="Alpha", ascending=False).head(10)
    for _, r in top_10.iterrows():
        st.write(f"**{r['Ticker']}** | {r['Sector']} | **+{r['Alpha']:.1f}% Alpha** | ${r['Price']:.2f}")
    st.divider()

# Sorted Dropdown with % included in label
sector_options = [f"{r['Name']} ({r['PC']:+.2f}%)" for _, r in df_s_perf.iterrows()]
selected_label = st.selectbox("Select Sector (Sorted by Strength):", sector_options)
selected_sector = selected_label.split(" (")[0]

st.subheader(f"Ranked {selected_sector}")

# Filter and Sort Sector View
df_view = df_all[df_all['Sector'] == selected_sector].sort_values(by="Alpha", ascending=False)

for _, row in df_view.iterrows():
    is_lead = row['Alpha'] > 0
    badge = "⭐" if is_lead else "◌"
    color = "green" if is_lead else "gray"
    
    # Compact row format
    st.markdown(f"**{badge} {row['Ticker']}** | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%")
