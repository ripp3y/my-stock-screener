import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# CSS for a clean mobile look
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; }
    [data-testid="stLineChart"] { height: 180px !important; }
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

@st.cache_data(ttl=600)
def get_clean_data():
    all_stocks = []
    s_perf = []
    
    for s_name, s_ticker in sectors.items():
        try:
            s_obj = yf.Ticker(s_ticker)
            s_hist = s_obj.history(period="5d")
            if s_hist.empty: continue
            
            s_pc = ((s_hist['Close'].iloc[-1] - s_hist['Close'].iloc[-2]) / s_hist['Close'].iloc[-2]) * 100
            s_perf.append({"Name": s_name, "PC": s_pc})
            
            if s_name in sector_stocks:
                for t in sector_stocks[s_name]:
                    try:
                        t_obj = yf.Ticker(t)
                        t_hist = t_obj.history(period="5d")
                        if t_hist.empty: continue
                        
                        price = t_hist['Close'].iloc[-1]
                        change = ((t_hist['Close'].iloc[-1] - t_hist['Close'].iloc[-2]) / t_hist['Close'].iloc[-2]) * 100
                        
                        all_stocks.append({
                            "Ticker": t, "Price": price, "Change": change, 
                            "Sector": s_name, "Alpha": change - s_pc
                        })
                    except: continue
        except: continue
        
    # Ensure the DataFrame is created with the correct columns even if empty
    df = pd.DataFrame(all_stocks, columns=['Ticker', 'Price', 'Change', 'Sector', 'Alpha'])
    sdf = pd.DataFrame(s_perf, columns=['Name', 'PC']).sort_values(by="PC", ascending=False)
    return df, sdf

df_all, df_s_perf = get_clean_data()

st.title("🛡️ Alpha Terminal")

# Search Bar (Top Priority)
search_q = st.text_input("🔍 Quick Ticker Search", "").strip().upper()
if search_q:
    try:
        data = yf.download(search_q, period="6m", progress=False)
        if not data.empty:
            st.write(f"### {search_q}: ${data['Close'].iloc[-1]:.2f}")
            st.line_chart(data['Close'])
    except: st.error("Ticker not found.")

st.divider()

# Sector Drill-Down
if not df_s_perf.empty:
    s_labels = [f"{r['Name']} ({r['PC']:+.2f}%)" for _, r in df_s_perf.iterrows()]
    sel_label = st.selectbox("Sort by Sector Strength:", s_labels)
    sel_name = sel_label.split(" (")[0]
    
    # Securely filter the data
    df_v = df_all[df_all['Sector'] == sel_name].sort_values(by="Alpha", ascending=False)
    
    for _, row in df_v.iterrows():
        c = "green" if row['Change'] > 0 else "red"
        with st.expander(f"⭐ {row['Ticker']} | ${row['Price']:.2f} | :{c}[{row['Change']:+.2f}%]"):
            # Fetch chart ONLY when the user expands the section to save bandwidth/API limits
            chart_data = yf.download(row['Ticker'], period="6m", progress=False)
            if not chart_data.empty:
                st.line_chart(chart_data['Close'])
            else:
                st.write("Chart data loading...")
