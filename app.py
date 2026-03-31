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

# 5. Deep Dive Selection
selected_sector = st.selectbox("Select a Sector to Drill Down:", df_sectors['Sector'])

if selected_sector in my_watchlist:
    st.write(f"### Top Picks in {selected_sector}")
    for ticker in my_watchlist[selected_sector]:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        st.write(f"**{ticker}:** ${price:.2f}")
else:
    st.info("Select a sector to see your primary watchlists.")

st.caption("Data refreshed every 5 minutes. Build v1.0")
