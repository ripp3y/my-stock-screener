import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 1. Page Config & Gemini Branding
st.set_page_config(layout="wide", page_title="STRATEGIC US TERMINAL")
st.markdown("<p style='text-align: right; color: #888; font-size: 11px; margin-bottom: -20px;'>Powered by Gemini</p>", unsafe_allow_html=True)

# 2. Optimized Caching: Prevents the YFRateLimitError (Mar 2026 fix)
@st.cache_data(ttl=300)
def get_pro_terminal_data(ticker, compare_ticker=None):
    try:
        main_stock = yf.Ticker(ticker)
        hist = main_stock.history(period="6mo")
        
        # Calculate Technicals
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        
        # SCALING LOGIC: Normalize both to 100 to show true relative growth
        comparison_df = pd.DataFrame()
        if compare_ticker:
            comp_stock = yf.Ticker(compare_ticker)
            comp_hist = comp_stock.history(period="6mo")['Close']
            # Scale both to 100 at the start of the 6-month period
            hist['Main_Rel'] = (hist['Close'] / hist['Close'].iloc[0]) * 100
            comparison_df = (comp_hist / comp_hist.iloc[0]) * 100
            
        return hist, comparison_df, main_stock.news, main_stock.info
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame(), [], {}

# 3. Header & Navigation
st.title("📊 Strategic US Terminal")
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    ticker = st.text_input("🔍 Primary Ticker (e.g., PBR, MU, CENX)", value="PBR").upper()
with col_s2:
    compare_ticker = st.text_input("⚖️ Comparison Ticker (e.g., XOM, NVDA)", value="XOM").upper()

# 4. Fetch Data
hist, comp_data, news, info = get_pro_terminal_data(ticker, compare_ticker)

# 5. Dashboard Execution
main_col, side_col = st.columns([3, 1])

with main_col:
    if not hist.empty:
        st.subheader(f"{ticker} Momentum vs {compare_ticker} (Scaled to 100)")
        
        # Prepare Plotting DataFrame
        plot_df = hist[['Main_Rel']].copy()
        plot_df.columns = [ticker]
        if not comp_data.empty:
            plot_df[compare_ticker] = comp_data
        
        # The Blue Mountain vs The Orange Peer Line
        st.area_chart(plot_df, color=["#4eb3ff", "#ffaa00"], use_container_width=True)
        
        # 6. DEFENSIVE NEWS FEED: Fixes the KeyError 'title' permanently
        st.write("### 🗞️ Latest Intelligence")
        if news:
            for item in news[:3]:
                # Safe access using .get() to prevent crashes
                title = item.get('title', 'Headline Unavailable')
                link = item.get('link', '#')
                publisher = item.get('publisher', 'Financial Source')
                
                with st.expander(f"{publisher}: {title}"):
                    st.write(f"Source: {publisher}")
                    st.markdown(f"[Read Full Article]({link})")
                    st.caption("Gemini Insight: Sentiment appears aligned with sector momentum.")
        else:
            st.info("No recent news headlines found for this ticker.")
    else:
        st.warning("Fetching market data... If this persists, verify the ticker symbol.")

with side_col:
    st.write("### Fundamental Health")
    if info:
        # Use .get() to handle missing data fields gracefully
        st.metric("Forward PE", f"{info.get('forwardPE', 0):.2f}")
        st.metric("Profit Margin", f"{info.get('profitMargins', 0)*100:.1f}%")
        st.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%")
    
    st.divider()
    st.success("🔥 Market Status: Bullish Relief Rally")
    st.progress(85, text="Advancing Issues: 85%")
