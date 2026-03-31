import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Alpha Terminal", layout="centered")

# Final CSS for mobile performance
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.85rem !important; }
    .stButton>button { height: 2.2rem; font-size: 0.85rem; width: 100%; }
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

# 1. BATCH DATA ENGINE (Fixes the "Unavailable" Error)
@st.cache_data(ttl=600) # Increased cache to 10 minutes to reduce API stress
def get_alpha_terminal_data():
    all_stocks = []
    s_perf = []
    charts = {}
    
    for s_name, s_ticker in sectors.items():
        try:
            s_obj = yf.Ticker(s_ticker)
            s_hist = s_obj.history(period="1mo")
            if len(s_hist) < 2: continue
            
            s_change = ((s_hist['Close'].iloc[-1] - s_hist['Close'].iloc[-2]) / s_hist['Close'].iloc[-2]) * 100
            s_perf.append({"Name": s_name, "PC": s_change})
            
            if s_name in sector_stocks:
                # BATCH DOWNLOAD for the entire sector at once
                sector_tickers = sector_stocks[s_name]
                data = yf.download(sector_tickers, period="6m", interval="1d", group_by='ticker', progress=False)
                
                for t in sector_tickers:
                    try:
                        # Extract price and change
                        t_data = data[t] if len(sector_tickers) > 1 else data
                        if t_data.empty: continue
                        
                        price = t_data['Close'].iloc[-1]
                        # Calc 1-day change from the 6m history
                        change = ((t_data['Close'].iloc[-1] - t_data['Close'].iloc[-2]) / t_data['Close'].iloc[-2]) * 100
                        
                        all_stocks.append({
                            "Ticker": t, "Price": price, "Change": change, 
                            "Sector": s_name, "Alpha": change - s_change
                        })
                        # Pre-store the chart data
                        charts[t] = t_data['Close']
                    except: continue
        except: continue
    return pd.DataFrame(all_stocks), pd.DataFrame(s_perf).sort_values(by="PC", ascending=False), charts

# 2. RUN APP
df_all, df_s_perf, all_charts = get_alpha_terminal_data()

st.title("🛡️ Alpha Terminal")

# Search Bar
search_q = st.text_input("🔍 Quick Ticker Search", "").strip().upper()
if search_q:
    s_data = yf.download(search_q, period="6m", progress=False)
    if not s_data.empty:
        st.write(f"### {search_q}: ${s_data['Close'].iloc[-1]:.2f}")
        st.line_chart(s_data['Close'])

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
            # Instant chart display from pre-loaded data
            if row['Ticker'] in all_charts:
                st.line_chart(all_charts[row['Ticker']])
            else:
                st.write("Fetching latest chart...")
