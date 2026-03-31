
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. App Configuration
st.set_page_config(page_title="Stock Tracker", layout="centered")
st.title("📊 Sector Momentum Dashboard")

sectors = {
    "Energy": "XLE", "Industrials": "XLI", "Materials": "XLB", 
    "Tech": "XLK", "Financials": "XLF", "Utilities": "XLU"
}

my_watchlist = {
    "Energy": ["PBR.A", "EQNR", "OVV", "PTEN", "CVX"],
    "Materials": ["CENX", "AA"],
    "Tech": ["MU", "LRCX", "ASX"]
}

# 2. Fetch Data & Build Chart
@st.cache_data(ttl=300)
def get_market_summary():
    data = []
    for name, ticker in sectors.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            data.append({"Sector": name, "Change %": round(change, 2)})
        except: continue
    return pd.DataFrame(data).sort_values(by="Change %")

df_sectors = get_market_summary()

# 3. Visual Bar Chart
st.subheader("Market Heatmap (1D %)")
fig = px.bar(df_sectors, x='Change %', y='Sector', orientation='h',
             color='Change %', color_continuous_scale='RdYlGn',
             text_auto=True)
fig.update_layout(showlegend=False, height=300, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)

st.divider()

# 4. Watchlist with Percentage Logic
selected_sector = st.selectbox("Drill Down Sector:", df_sectors['Sector'][::-1])

if selected_sector in my_watchlist:
    st.write(f"### {selected_sector} Watchlist")
    for ticker in my_watchlist[selected_sector]:
        try:
            s = yf.Ticker(ticker)
            h = s.history(period="2d")
            price = h['Close'].iloc[-1]
            pct = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
            
            # Color coding the output
            color = "🟢" if pct >= 0 else "🔴"
            st.write(f"{color} **{ticker}**: ${price:.2f} ({pct:+.2f}%)")
        except:
            st.write(f"⚪ **{ticker}**: Data pending...")
