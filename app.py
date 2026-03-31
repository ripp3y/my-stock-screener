import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. Setup
st.set_page_config(page_title="Global Market Alpha", layout="centered")
st.title("🏛️ Full Sector Momentum Terminal")

# 2. All 11 Major Market Sectors
sectors = {
    "Energy": "XLE",
    "Materials": "XLB",
    "Industrials": "XLI",
    "Tech": "XLK",
    "Financials": "XLF",
    "Health Care": "XLV",
    "Cons. Discretionary": "XLY",
    "Cons. Staples": "XLP",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Communication": "XLC"
}

# 3. Pre-Populated "A-Class" Candidates for Every Sector
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

# 4. Market Data Engine
@st.cache_data(ttl=300)
def get_all_sector_perf():
    data = {}
    for name, ticker in sectors.items():
        try:
            h = yf.Ticker(ticker).history(period="2d")
            change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
            data[name] = round(change, 2)
        except: data[name] = 0.0
    return data

sector_perf_map = get_all_sector_perf()

# 5. Dashboard Visuals
df_perf = pd.DataFrame(list(sector_perf_map.items()), columns=['Sector', 'Change %']).sort_values(by="Change %")
fig = px.bar(df_perf, x='Change %', y='Sector', orientation='h', 
             color='Change %', color_continuous_scale='RdYlGn', text_auto=True)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# 6. Interactive Discovery
selected_name = st.selectbox("Switch Sector View:", df_perf['Sector'][::-1])
s_change = sector_perf_map[selected_name]

st.subheader(f"Top 8 in {selected_name} (Sector: {s_change:+.2f}%)")

# Grid display for mobile
cols = st.columns(2)
if selected_name in sector_stocks:
    for i, ticker in enumerate(sector_stocks[selected_name]):
        with cols[i % 2]:
            try:
                t_obj = yf.Ticker(ticker)
                h = t_obj.history(period="2d")
                price = h['Close'].iloc[-1]
                stock_pc = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                
                # RELATIVE STRENGTH CHECK
                is_leader = stock_pc > s_change
                badge = "⭐ LEADER" if is_leader else "◌ Laggard"
                b_color = "green" if is_leader else "gray"
                
                st.markdown(f"**{ticker}**")
                st.markdown(f"Price: `${price:.2f}`")
                st.markdown(f"1D: :{b_color}[{stock_pc:+.2f}%] | {badge}")
                st.write("---")
            except:
                st.write(f"{ticker}: Syncing...")
