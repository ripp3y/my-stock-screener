import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Advanced Mobile Optimization
st.set_page_config(page_title="Alpha Screener", layout="centered")

# Custom CSS for that compact "Bloomberg" feel on your phone
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; }
    h1 { font-size: 1.4rem !important; margin-bottom: 0px !important; }
    h3 { font-size: 1.1rem !important; }
    .stButton>button { height: 2.2rem; font-size: 0.85rem; width: 100%; }
    hr { margin: 0.4rem 0px !important; }
    /* Compact charts */
    [data-testid="stLineChart"] { height: 200px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Market Sectors & Core Watchlist
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

# 3. Data Engine
@st.cache_data(ttl=300)
def get_alpha_data():
    s_perf_raw = []
    for name, tick in sectors.items():
        try:
            h = yf.Ticker(tick).history(period="2d")
            change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
            s_perf_raw.append({"Name": name, "PC": change})
        except: s_perf_raw.append({"Name": name, "PC": 0.0})
    s_df = pd.DataFrame(s_perf_raw).sort_values(by="PC", ascending=False)
    
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

# --- RENDER INTERFACE ---
df_all, df_s_perf = get_alpha_data()

st.title("🛡️ Alpha Terminal")

# Search Bar
search_q = st.text_input("🔍 Quick Search (e.g. CENX)", "").strip().upper()
if search_q:
    try:
        t_obj = yf.Ticker(search_q)
        t_hist = t_obj.history(period="6m")
        cur_price = t_hist['Close'].iloc[-1]
        st.write(f"**{search_q}** | Current: `${cur_price:.2f}`")
        st.line_chart(t_hist['Close'])
    except:
        st.error("Ticker not found.")

st.divider()

# Navigation Buttons
c1, c2 = st.columns(2)
with c1:
    btn_best = st.button("🏆 THE BEST")
with c2:
    btn_sectors = st.button("📁 SECTORS")

# Session State for View Persistence
if 'mode' not in st.session_state: st.session_state.mode = 'sectors'
if btn_best: st.session_state.mode = 'best'
if btn_sectors: st.session_state.mode = 'sectors'

if st.session_state.mode == 'best':
    st.subheader("🔥 Top 10 Global Leaders")
    top_10 = df_all.sort_values(by="Alpha", ascending=False).head(10)
    for _, r in top_10.iterrows():
        with st.expander(f"{r['Ticker']} | ${r['Price']:.2f} | +{r['Alpha']:.1f}% Alpha"):
            h = yf.Ticker(r['Ticker']).history(period="6m")
            st.line_chart(h['Close'])

else:
    s_options = [f"{r['Name']} ({r['PC']:+.2f}%)" for _, r in df_s_perf.iterrows()]
    sel_label = st.selectbox("Sort by Sector Strength:", s_options)
    sel_name = sel_label.split(" (")[0]
    
    st.subheader(f"Ranked: {sel_name}")
    df_v = df_all[df_all['Sector'] == sel_name].sort_values(by="Alpha", ascending=False)
    
    for _, row in df_v.iterrows():
        badge = "⭐" if row['Alpha'] > 0 else "◌"
        color = "green" if row['Change'] > 0 else "red"
        label = f"{badge} {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(label):
            st.write(f"6-Month Trend for {row['Ticker']}")
            h_data = yf.Ticker(row['Ticker']).history(period="6m")
            st.line_chart(h_data['Close'])
