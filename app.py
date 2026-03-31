import streamlit as st
import yfinance as yf
import pandas as pd

# 1. App Configuration
st.set_page_config(page_title="Stock Screener", layout="centered")
st.title("📊 Sector & Watchlist Pro")

# 2. Define Sectors & Your Specific Watchlist
sectors = {
    "Energy": "XLE",
    "Industrials": "XLI",
    "Materials": "XLB",
    "Tech": "XLK",
    "Financials": "XLF",
}

my_watchlist = {
    "Energy": ["PBR.A", "EQNR", "OVV", "PTEN", "CVX"],
    "Materials": ["CENX", "AA", "FCX"],
    "Tech": ["MU", "LRCX", "ASX"]
}

# 3. Sector Performance Logic
@st.cache_data(ttl=300)
def get_market_data():
    data = []
    for name, ticker in sectors.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            data.append({"Sector": name, "Change %": round(change, 2)})
        except:
            continue
    return pd.DataFrame(data).sort_values(by="Change %", ascending=False)

df_sectors = get_market_data()

# 4. Display Sector Grid
st.subheader("Sector Performance (1D)")
cols = st.columns(2)
for i, (index, row) in enumerate(df_sectors.iterrows()):
    col = cols[i % 2]
    col.metric(row['Sector'], f"{row['Change %']}%")

st.divider()

# 5. The "At a Glance" Drill Down
selected_sector = st.selectbox("Select a Sector to Drill Down:", df_sectors['Sector'])

# Display your Watchlist for that sector
if selected_sector in my_watchlist:
    st.write(f"### My {selected_sector} Watchlist")
    for ticker_symbol in my_watchlist[selected_sector]:
        try:
            stock_data = yf.Ticker(ticker_symbol)
            latest_price = stock_data.history(period="1d")['Close'].iloc[-1]
            st.write(f"**{ticker_symbol}:** ${latest_price:.2f}")
        except:
            st.write(f"**{ticker_symbol}:** Data pending...")

# 6. 🔥 Top Sector Movers (Discovery)
st.write("---")
st.subheader(f"🔥 Trending in {selected_sector}")
# For now, we list major liquid players in that sector to watch for momentum
trending_list = {
    "Energy": ["XOM", "SHEL", "BP"],
    "Materials": ["NEM", "BHP", "RIO"],
    "Tech": ["NVDA", "AAPL", "AMD"],
    "Industrials": ["CAT", "HON", "GE"]
}

if selected_sector in trending_list:
    for trend_ticker in trending_list[selected_sector]:
        try:
            t_stock = yf.Ticker(trend_ticker)
            t_price = t_stock.history(period="1d")['Close'].iloc[-1]
            st.write(f"🚀 **{trend_ticker}** is active at ${t_price:.2f}")
        except:
            continue
