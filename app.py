import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Advanced Mobile Optimization
st.set_page_config(page_title="Alpha Screener", layout="centered", initial_sidebar_state="collapsed")

# Inject Custom CSS for dense mobile viewing and chart layout
st.markdown("""
    <style>
    /* Compact Text and Lists */
    .stMarkdown, div[data-testid="stExpander"] label { font-size: 0.8rem !important; line-height: 1.1 !important; }
    h1, h2, h3 { line-height: 1.2 !important; margin-bottom: 0px !important; }
    h1 { font-size: 1.3rem !important; }
    h3 { font-size: 1.0rem !important; }
    
    /* Shrink charts for mobile screens */
    .stPlotlyChart { height: 250px !important; margin-top: -10px !important; }
    
    /* Tighten buttons and headers */
    .stButton>button { height: 2rem; font-size: 0.8rem; margin-top: -5px !important; }
    div[data-testid="stSidebarHeader"] { display: none !important; }
    div.st-emotion-cache-1kyxreq { padding: 0.5rem 1rem !important; }
    div[data-testid="stHeader"] { height: 0px !important; display:none !important; }
    hr { margin: 0.3rem 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Complete Market Infrastructure (Unchanged)
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

# 3. Enhanced Data Engine
@st.cache_data(ttl=300)
def get_alpha_data():
    all_stocks = []
    
    # 3a. Get Sector baselines and sort them
    s_perf_raw = []
    for name, tick in sectors.items():
        try:
            h = yf.Ticker(tick).history(period="2d")
            change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
            s_perf_raw.append({"Name": name, "PC": change})
        except: s_perf_raw.append({"Name": name, "PC": 0.0})
    s_df = pd.DataFrame(s_perf_raw).sort_values(by="PC", ascending=False)
    
    # 3b. Caluclate Alpha for all 88 stocks
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

# Charting function (mimicking the "Mountain" style)
def display_stock_mountain_chart(ticker_symbol):
    try:
        t_stock = yf.Ticker(ticker_symbol)
        h_6m = t_stock.history(period="6m")
        st.area_chart(h_6m['Close'], color="#4285F4") # Clean mobile mountain chart
    except: st.error(f"Could not load chart for {ticker_symbol}")

# --- MAIN INTERFACE START ---
df_all, df_s_perf = get_alpha_data()

st.title("🛡️ Alpha Momentum Terminal")

# NEW FEATURE: Global Search Bar (Fixed at Top)
search_ticker = st.text_input("🔍 Quick Ticker Search", placeholder="Example: CENX, PBR.A, MU...")
st.write("---")

if search_ticker:
    search_ticker = search_ticker.strip().upper()
    try:
        # 1. Fetch search data
        s_obj = yf.Ticker(search_ticker)
        s_h2d = s_obj.history(period="2d")
        
        # 2. Display Price & Change
        s_price = s_h2d['Close'].iloc[-1]
        s_change = ((s_h2d['Close'].iloc[-1] - s_h2d['Close'].iloc[-2]) / s_h2d['Close'].iloc[-2]) * 100
        color = "green" if s_change >= 0 else "red"
        
        st.markdown(f"**### 🔍 Search: {search_ticker}** | `${s_price:.2f}` (:{color}[{s_change:+.2f}%])")
        
        # 3. New Chart Drill-Down (Mountain View)
        display_stock_mountain_chart(search_ticker)
        
    except Exception as e:
        st.warning(f"Ticker '{search_ticker}' not found. Verify the symbol on Yahoo Finance.")
    st.divider()

# NEW FEATURE: Chart Drill-Down Button
with st.sidebar:
    st.markdown("### Chart Settings")
    show_charts = st.checkbox("🔄 Show Ticker Chart on Drill-Down", value=True)

# 4. Global Top 10 (Restructured)
cols = st.columns([0.2, 0.8])
with cols[0]:
    if st.button("🏆 TOP 10"): st.session_state['view_mode'] = 'best'
with cols[1]:
    if st.button("📁 SECTORS"): st.session_state['view_mode'] = 'sectors'
    
st.write("---")

# Navigation logic (using session state so chart drill-downs work)
if 'view_mode' not in st.session_state: st.session_state['view_mode'] = 'sectors'

if st.session_state['view_mode'] == 'best':
    st.subheader("🔥 Top 10 Global Leaders")
    top_10 = df_all.sort_values(by="Alpha", ascending=False).head(10)
    for i, r in top_10.iterrows():
        expander_label = f"{r['Ticker']} | ${r['Price']:.2f} | **+{r['Alpha']:.1f}% Alpha**"
        with st.expander(expander_label):
            # Display chart if user clicked the expander and charts are on
            if show_charts: display_stock_mountain_chart(r['Ticker'])

elif st.session_state['view_mode'] == 'sectors':
    # 5. Sorted Dropdown (Same as before)
    sector_options = [f"{r['Name']} ({r['PC']:+.2f}%)" for _, r in df_s_perf.iterrows()]
    selected_label = st.selectbox("Select Sector (Sorted by Strength):", sector_options)
    selected_sector = selected_label.split(" (")[0]
    s_perf = float(selected_label.split("(")[1].split("%")[0])

    st.subheader(f"Results: {selected_sector} (Sector: {s_perf:+.2f}%)")
    st.write("---")

    # Filter, Sort, and Display Sector View
    df_view = df_all[df_all['Sector'] == selected_sector].sort_values(by="Alpha", ascending=False)

    for _, row in df_view.iterrows():
        is_lead = row['Alpha'] > 0
        badge = "⭐" if is_lead else "◌"
        color = "green" if is_lead else "gray"
        
        # Compact row format with Expandable Chart
        expander_label = f"**{badge} {row['Ticker']}** | ${row['Price']:.2f} | :{color}[{row['Change']:+.2f}%] | Alpha: {row['Alpha']:+.1f}%"
        
        with st.expander(expander_label):
            # NEW: The Yahoo-Style Mountain Chart (6M View)
            # This triggers when you tap the row on your phone
            if show_charts:
                st.write(f"### 📈 {row['Ticker']} - 6 Month Trend")
                display_stock_mountain_chart(row['Ticker'])
