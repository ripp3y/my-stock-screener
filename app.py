import streamlit as st
import yfinance as yf
import pandas as pd

# 1. App Configuration (Mobile Optimized)
st.set_page_config(page_title="Sector Screener", layout="centered")

st.title("📊 Market Rotation Pro")
st.write("Real-time sector pulse for quick adjustments.")

# 2. Define Sectors & Tickers
sectors = {
    "Energy": "XLE",
    "Industrials": "XLI",
    "Materials": "XLB",
    "Tech": "XLK",
    "Health Care": "XLV",
    "Financials": "XLF",
    "Consumer Disc": "XLY",
    "Utilities": "XLU",
}

# Stocks you specifically track
my_watchlist = {
    "Energy": ["PBR.A", "EQNR", "OVV", "PTEN", "CVX"],
    "Materials": ["CENX"],
    "Tech": ["MU", "LRCX", "ASX"]
}

# 3. Fetch Sector Data
@st.cache_data(ttl=300) # Refresh data every 5 mins
def get_market_data():
    data = []
    for name, ticker in sectors.items():
        t = yf.Ticker(ticker)
        hist = t.history(period="2d")
        if len(hist) > 1:
            change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            data.append({"Sector": name, "Ticker": ticker, "Change %": round(change, 2)})
    return pd.DataFrame(data).sort_values(by="Change %", ascending=False)

df_sectors = get_market_data()

# 4. Display Sector Grid
st.subheader("Sector Performance (1D)")
cols = st.columns(2) # Two columns looks best on mobile

for i, (index, row) in enumerate(df_sectors.iterrows()):
    col = cols[i % 2]
    color = "green" if row['Change %'] >= 0 else "red"
    col.metric(row['Sector'], f"{row['Change %']}%", delta_color="normal")
    
st.divider()

st.subheader("🔥 Top Sector Movers")

# This pulls the biggest gainers in the selected sector automatically
ticker_search = yf.Ticker(sectors[selected_sector])
top_movers = ["XOM", "CVX", "BP"] # Placeholder: We can automate this to pull live Finviz leaders next!

for mover in top_movers:
    m_data = yf.Ticker(mover)
    m_price = m_data.history(period="1d")['Close'].iloc[-1]
    st.write(f"🚀 **{mover}** is trending in {selected_sector} at ${m_price:.2f}")

st.divider()

# 5. Deep Dive Selection
selected_sector = st.selectbox("Select a Sector to Drill Down:", df_sectors['Sector'])

if selected_sector in my_watchlist:
    st.write(f"### Top Picks in {selected_sector}")
    for ticker_symbol in my_watchlist[selected_sector]:
        try:
            stock_data = yf.Ticker(ticker_symbol)
            # Fetching the most recent closing price
            latest_price = stock_data.history(period="1d")['Close'].iloc[-1]
            st.write(f"**{ticker_symbol}:** ${latest_price:.2f}")
        except Exception:
            st.write(f"**{ticker_symbol}:** Connection busy, refresh in a moment")
else:
    st.info("Select a sector to see your primary watchlists.")
