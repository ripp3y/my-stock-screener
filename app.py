import streamlit as st
import yfinance as yf
import pandas as pd

# --- ANALYTICS ENGINE ---
@st.cache_data(ttl=1800)
def get_advanced_metrics(symbol):
    ticker = yf.Ticker(symbol)
    # Get 6 months of 1-hour data for volume profile
    hist = ticker.history(period="6mo", interval="1h")
    info = ticker.info
    
    if not hist.empty:
        # Calculate VWAP: Cumulative (Price * Volume) / Cumulative Volume
        hist['PV'] = hist['Close'] * hist['Volume']
        vwap = hist['PV'].sum() / hist['Volume'].sum()
        
        # Volume Profile (Horizontal Histogram)
        # We bin prices to find the "Point of Control" (POC)
        hist['Price_Bin'] = pd.cut(hist['Close'], bins=20)
        volume_profile = hist.groupby('Price_Bin', observed=False)['Volume'].sum()
        poc_bin = volume_profile.idxmax()
        poc_price = (poc_bin.left + poc_bin.right) / 2
        
        return info, vwap, poc_price
    return info, None, None

# --- UI LOGIC ---
st.title("🚀 Alpha Terminal: The 80% Pursuit")
target = st.sidebar.selectbox("Target", ["PBR-A", "CENX", "EQNR", "INTT", "CNQ"])
info, vwap, poc = get_advanced_metrics(target)

if info and vwap:
    # 1. THE "INSTITUTIONAL FLOOR"
    curr = info.get('currentPrice')
    st.subheader("Institutional Footprint")
    col1, col2 = st.columns(2)
    
    # VWAP is the "Fair Value" for big banks
    col1.metric("VWAP (6Mo)", f"${round(vwap, 2)}", f"{round(((curr-vwap)/vwap)*100, 1)}% vs Price")
    
    # POC is the price where the most shares changed hands
    col2.metric("Point of Control (POC)", f"${round(poc, 2)}", "Max Volume Node")

    # 2. ACTIONABLE LOGIC
    st.divider()
    if curr > vwap and curr > poc:
        st.success(f"🔥 **BULLISH ACCUMULATION:** {target} is trading above institutional support. The 'Big Money' is in the green.")
    elif curr < vwap and curr < poc:
        st.warning(f"❄️ **INSTITUTIONAL DISTRIBUTION:** Price is below major volume nodes. Wait for a reclaim of ${round(vwap, 2)}.")
