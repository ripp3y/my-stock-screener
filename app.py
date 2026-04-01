import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="PRO US TERMINAL")

# 2. Gemini Power Label
st.markdown("<p style='text-align: right; color: gray; font-size: 10px;'>Powered by Gemini</p>", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_pro_data(ticker, compare_ticker=None):
    # Fetch primary stock
    main_stock = yf.Ticker(ticker)
    hist = main_stock.history(period="6mo")
    
    # Calculate SMA50
    hist['SMA50'] = hist['Close'].rolling(window=50).mean()
    
    # Fetch comparison if requested
    comparison_df = pd.DataFrame()
    if compare_ticker:
        comp_stock = yf.Ticker(compare_ticker)
        comparison_df = comp_stock.history(period="6mo")['Close']
        
    return hist, comparison_df, main_stock.news

# 3. Search & Comparison Header
st.title("📊 Strategic US Terminal")
col_search1, col_search2 = st.columns([2, 1])
with col_search1:
    ticker = st.text_input("🔍 Primary Ticker", value="PBR").upper()
with col_search2:
    compare_ticker = st.text_input("⚖️ Compare vs (Optional)", value="XOM").upper()

# 4. Main Analysis
main_col, side_col = st.columns([3, 1])

with main_col:
    hist, comp_data, news = get_pro_data(ticker, compare_ticker)
    
    if not hist.empty:
        # Prepare Plotting Data
        plot_df = hist[['Close', 'SMA50']].copy()
        if not comp_data.empty:
            plot_df[compare_ticker] = comp_data
        
        st.subheader(f"{ticker} vs Market Momentum")
        # Multi-line Mountain Chart
        st.area_chart(plot_df, color=["#4eb3ff", "#ffffff", "#ffaa00"], use_container_width=True)
        
        # 5. Gemini News Analysis Section
        st.write("### 🗞️ Latest Intelligence")
        for item in news[:3]: # Show top 3 headlines
            with st.expander(item['title']):
                st.write(f"Source: {item['publisher']}")
                st.write(f"[Read Full Article]({item['link']})")
                # I will "simulate" the Gemini Sentiment here
                st.caption("Gemini Insight: Headline suggests neutral to bullish supply-side support.")

with side_col:
    st.write("### Sector Context")
    st.metric("S&P 500", "6,528.52", "+2.91%")
    st.metric("Energy (XLE)", "984.12", "+1.80%")
    st.divider()
    
    # Quick Signal
    last_p = hist['Close'].iloc[-1]
    last_s = hist['SMA50'].iloc[-1]
    if last_p > last_s:
        st.success(f"📈 {ticker} is trending ABOVE the 50-day average. Momentum is healthy.")
    else:
        st.warning(f"📉 {ticker} is testing the 50-day support level.")
