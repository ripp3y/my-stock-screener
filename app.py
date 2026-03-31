import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Compact CSS for mobile
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; }
    .stButton>button { height: 2.2rem; font-size: 0.85rem; width: 100%; }
    [data-testid="stLineChart"] { height: 220px !important; }
    </style>
    """, unsafe_allow_html=True)

# Define Sectors and Tickers
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

# 1. THE BULLETPROOF DATA ENGINE
@st.cache_data(ttl=300)
def get_safe_data():
    all_results = []
    s_perf = []
    
    for s_name, s_ticker in sectors.items():
        try:
            # Use '1mo' instead of '2d' to ensure we always have enough data points for a chart
            s_obj = yf.Ticker(s_ticker)
            s_hist = s_obj.history(period="1mo")
            if len(s_hist) < 2: continue
            
            s_change = ((s_hist['Close'].iloc[-1] - s_hist['Close'].iloc[-2]) / s_hist['Close'].iloc[-2]) * 100
            s_perf.append({"Name": s_name, "PC": s_change})
            
            if s_name in sector_stocks:
                for t in sector_stocks[s_name]:
                    try:
                        t_obj = yf.Ticker(t)
                        t_hist = t_obj.history(period="1mo")
                        if t_hist.empty: continue
                        
                        price = t_hist['Close'].iloc[-1]
                        change = ((t_hist['Close'].iloc[-1] - t_hist['Close'].iloc[-2]) / t_hist['Close'].iloc[-2]) * 100
                        all_results.append({
                            "Ticker": t, "Price": price, "Change": change, 
                            "Sector": s_name, "Alpha": change - s_change
                        })
                    except: continue
        except: continue
    
    return pd.DataFrame(all_results), pd.DataFrame(s_perf).sort_values(by="PC", ascending=False)

# 2. RUN APP
df_all, df_s_perf = get_safe_data()

st.title("🛡️ Alpha Terminal")

# Emergency Clear Cache Button
if st.button("🔄 Clear App Cache / Force Refresh"):
    st.cache_data.clear()
    st.rerun()

search_q = st.text_input("🔍 Quick Ticker Search", "").strip().upper()
if search_q:
    t_obj = yf.Ticker(search_q)
    t_h = t_obj.history(period="6m")
    if not t_h.empty:
        st.write(f"### {search_q}: ${t_h['Close'].iloc[-1]:.2f}")
        st.line_chart(t_h['Close'])
    else: st.error("No data found. Try a different ticker.")

st.divider()

# 3. SECTOR DISPLAY
if not df_s_perf.empty:
    s_labels = [f"{r['Name']} ({r['PC']:+.2f}%)" for _, r in df_s_perf.iterrows()]
    sel_label = st.selectbox("Sort by Sector Strength:", s_labels)
    sel_name = sel_label.split(" (")[0]
    
    st.subheader(f"Ranked: {sel_name}")
    df_v = df_all[df_all['Sector'] == sel_name].sort_values(by="Alpha", ascending=False)
    
    for _, row in df_v.iterrows():
        is_lead = row['Alpha'] > 0
        badge = "⭐" if is_lead else "◌"
        c = "green" if row['Change'] > 0 else "red"
        
        with st.expander(f"{badge} {row['Ticker']} | ${row['Price']:.2f} | :{c}[{row['Change']:+.2f}%]"):
            # Pull fresh 6-month history for the chart
            h_chart = yf.Ticker(row['Ticker']).history(period="6m")
            if not h_chart.empty:
                st.line_chart(h_chart['Close'])
            else:
                st.write("Chart data temporarily unavailable.")
