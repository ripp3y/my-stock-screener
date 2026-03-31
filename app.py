import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Advanced Mobile Optimization
st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Custom CSS for dense mobile viewing
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; line-height: 1.1 !important; }
    h1 { font-size: 1.4rem !important; margin-bottom: 0px !important; }
    .stButton>button { height: 2.2rem; font-size: 0.85rem; width: 100%; }
    hr { margin: 0.4rem 0px !important; }
    [data-testid="stLineChart"] { height: 220px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Market Structure
sectors = {
    "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI", "Tech": "XLK",
    "Financials": "XLF", "Health Care": "XLV", "Cons. Discretionary": "XLY",
    "Cons. Staples": "XLP", "Utilities": "XLU", "Real Estate": "XLRE", "Communication": "XLC"
}

sector_stocks = {
    "Energy": ["PBR.A", "EQNR", "OVV", "PTEN", "CVX", "XOM", "SLB", "COP"],
    "Materials": ["CENX", "AA", "FCX", "NEM", "BHP", "RIO", "LIN", "SHW"],
    "Tech": ["MU", "LRCX", "ASX", "NVDA", "AAPL", "MSFT", "AMD", "AVGO"],
    "Industrials": ["CAT", "DE", "GE", "UNP", "HON", "RTX", "LMT", "UPS"]
}

# 3. Data Engine
@st.cache_data(ttl=300)
def get_market_data():
    s_perf = []
    for name, tick in sectors.items():
        try:
            h = yf.Ticker(tick).history(period="2d")
            pc = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
            s_perf.append({"Name": name, "PC": pc})
        except: s_perf.append({"Name": name, "PC": 0.0})
    s_df = pd.DataFrame(s_perf).sort_values(by="PC", ascending=False)
    
    all_stocks = []
    for _, s_row in s_df.iterrows():
        s_name = s_row['Name']
        if s_name in sector_stocks:
            for t in sector_stocks[s_name]:
                try:
                    obj = yf.Ticker(t)
                    h = obj.history(period="2d")
                    price = h['Close'].iloc[-1]
                    change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                    all_stocks.append({
                        "Ticker": t, "Price": price, "Change": change, 
                        "Sector": s_name, "Alpha": change - s_row['PC']
                    })
                except: continue
    return pd.DataFrame(all_stocks), s_df

df_all, df_s_perf = get_market_data()

# 4. Interface
st.title("🛡️ Alpha Terminal")

# SEARCH BAR LOGIC
search_q = st.text_input("🔍 Quick Ticker Search", "").strip().upper()
if search_q:
    try:
        t_obj = yf.Ticker(search_q)
        t_hist = t_obj.history(period="6m")
        if not t_hist.empty:
            cur_p = t_hist['Close'].iloc[-1]
            st.write(f"### {search_q}: ${cur_p:.2f}")
            st.line_chart(t_hist['Close']) # Shows the Mountain Chart
        else: st.error("No data found for this ticker.")
    except: st.error("Ticker not found.")

st.divider()

# SECTOR DRILL DOWN
s_options = [f"{r['Name']} ({r['PC']:+.2f}%)" for _, r in df_s_perf.iterrows()]
sel_label = st.selectbox("Sort by Sector Strength:", s_options)
sel_name = sel_label.split(" (")[0]

df_v = df_all[df_all['Sector'] == sel_name].sort_values(by="Alpha", ascending=False)

for _, row in df_v.iterrows():
    badge = "⭐" if row['Alpha'] > 0 else "◌"
    color = "green" if row['Change'] > 0 else "red"
    # This Expander is what shows the chart when clicked
    with st.expander(f"{badge} {row['Ticker']} | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%]"):
        st.write(f"**6-Month Trend for {row['Ticker']}**")
        h_data = yf.Ticker(row['Ticker']).history(period="6m")
        st.line_chart(h_data['Close']) # This generates the visual info you wanted
