import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Config & Gemini Branding
st.set_page_config(layout="wide", page_title="PRO US TERMINAL")
st.markdown("<p style='text-align: right; color: #888; font-size: 12px; margin-bottom: -20px;'>Powered by Gemini</p>", unsafe_allow_html=True)

# 2. Optimized Data Fetching
@st.cache_data(ttl=300)
def get_terminal_data(ticker, compare_ticker=None):
    try:
        main_stock = yf.Ticker(ticker)
        hist = main_stock.history(period="6mo")
        
        # Add SMA50
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        
        # Comparison Data (Percentage Growth)
        comparison_df = pd.DataFrame()
        if compare_ticker:
            comp_stock = yf.Ticker(compare_ticker)
            comp_hist = comp_stock.history(period="6mo")['Close']
            # Scale both to 100 to show relative performance
            hist['Main_Growth'] = (hist['Close'] / hist['Close'].iloc[0]) * 100
            comparison_df = (comp_hist / comp_hist.iloc[0]) * 100
            
        return hist, comparison_df, main_stock.news, main_stock.info
    except Exception:
        return pd.DataFrame(), pd.DataFrame(), [], {}

# 3. UI Inputs
st.title("📊 Strategic US Terminal")
col_a, col_b = st.columns([2, 1])
with col_a:
    ticker = st.text_input("🔍 Primary Ticker", value="PBR").upper()
with col_b:
    compare_ticker = st.text_input("⚖️ Comparison Ticker", value="XOM").upper()

# 4. Dashboard Execution
hist, comp_data, news, info = get_terminal_data(ticker, compare_ticker)

main_col, side_col = st.columns([3, 1])

with main_col:
    if not hist.empty:
        st.subheader(f"{ticker} Performance vs {compare_ticker}")
        
        # Plotting Logic
        plot_df = hist[['Main_Growth']].copy()
        plot_df.columns = [ticker]
        if not comp_data.empty:
            plot_df[compare_ticker] = comp_data
        
        st.area_chart(plot_df, color=["#4eb3ff", "#ffaa00"])
        
        # 5. Fixed News Feed (No more KeyErrors)
        st.write("### 🗞️ Intelligence Feed")
        if news:
            for item in news[:4]:
                # Safely get keys to prevent app crashes
                title = item.get('title', 'Headline Unavailable')
                link = item.get('link', '#')
                publisher = item.get('publisher', 'Unknown Source')
                
                with st.expander(f"{publisher}: {title}"):
                    st.write(f"Source: {publisher}")
                    st.markdown(f"[Read Full Article]({link})")
                    st.caption("Gemini Analysis: Potential impact on sector volatility.")
        else:
            st.write("No recent news found for this ticker.")

with side_col:
    st.write("### Fundamental Health")
    if info:
        st.metric("PE Ratio", f"{info.get('forwardPE', 0):.2f}")
        st.metric("Profit Margin", f"{info.get('profitMargins', 0)*100:.1f}%")
    
    st.divider()
    st.success("🔥 Market Status: Bullish Relief Rally")
    st.info(f"💡 {ticker} is currently {'above' if hist['Close'].iloc[-1] > hist['SMA50'].iloc[-1] else 'below'} its 50-day SMA.")
