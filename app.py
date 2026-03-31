import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="The Best Momentum", layout="centered")

# 1. Market Infrastructure
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

# 2. Data Engine (Calculates Alpha for everything)
@st.cache_data(ttl=300)
def get_full_market_rankings():
    # Get Sector Baselines
    sector_perf = {}
    for name, ticker in sectors.items():
        try:
            h = yf.Ticker(ticker).history(period="2d")
            sector_perf[name] = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
        except: sector_perf[name] = 0.0
    
    # Rank all stocks
    all_stocks = []
    for sector, tickers in sector_stocks.items():
        s_base = sector_perf[sector]
        for t in tickers:
            try:
                obj = yf.Ticker(t)
                h = obj.history(period="2d")
                price = h['Close'].iloc[-1]
                change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                alpha = change - s_base  # This is the momentum score
                all_stocks.append({
                    "Ticker": t, "Price": price, "Change": change, 
                    "Sector": sector, "Alpha": alpha, "S_Perf": s_base
                })
            except: continue
    return pd.DataFrame(all_stocks), sector_perf

df_all, sector_map = get_full_market_rankings()

# 3. TOP NAVIGATION
st.title("🏆 Momentum Elite")
show_best = st.button("⭐ CLICK FOR: THE BEST (Top 10 Global)", use_container_width=True)

if show_best:
    st.subheader("🔥 The Best: Top 10 Momentum Leaders")
    top_10 = df_all.sort_values(by="Alpha", ascending=False).head(10)
    for _, row in top_10.iterrows():
        st.success(f"**{row['Ticker']}** ({row['Sector']}) | Momentum: +{row['Alpha']:.2f}% vs Sector | Price: ${row['Price']:.2f}")
    st.divider()

# 4. SECTOR VIEWER WITH SORTING
selected_sector = st.selectbox("Switch Sector View:", list(sectors.keys()))
s_change = sector_map[selected_sector]

st.subheader(f"Ranked: {selected_sector} (Sector: {s_change:+.2f}%)")

# Filter and Sort: Leaders at top, Laggards at bottom
df_sector = df_all[df_all['Sector'] == selected_sector].sort_values(by="Alpha", ascending=False)

for _, row in df_sector.iterrows():
    is_leader = row['Alpha'] > 0
    badge = "⭐ LEADER" if is_leader else "◌ Laggard"
    color = "green" if is_leader else "gray"
    
    with st.container():
        st.markdown(f"### **{row['Ticker']}** | {badge}")
        st.markdown(f"Price: `${row['Price']:.2f}` | 1D: :{color}[{row['Change']:+.2f}%]")
        st.progress(max(0, min((row['Alpha'] + 5) / 10, 1.0))) # Visual Momentum Bar
        st.write("---")
