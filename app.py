import streamlit as st
import yfinance as yf

@st.cache_data(ttl=1800)
def get_full_analysis(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        # Determine benchmark based on sector
        sector = info.get('sector', '')
        benchmark_symbol = "XLE" if "Energy" in sector else "XLI" if "Industrials" in sector else "SPY"
        
        benchmark = yf.Ticker(benchmark_symbol)
        return info, benchmark.info, benchmark_symbol
    except:
        return None, None, None

st.title("🛡️ Alpha Terminal: Sector Pro")
symbol = "SLB"
info, bench_info, b_ticker = get_full_analysis(symbol)

if info and bench_info:
    # --- ROW 1: Stock vs Benchmark ---
    st.subheader(f"Analysis vs. {b_ticker} Benchmark")
    col1, col2, col3 = st.columns(3)
    
    # PE Comparison
    s_pe = info.get('forwardPE', 0)
    b_pe = bench_info.get('forwardPE', 0)
    col1.metric("Forward PE", f"{round(s_pe, 1)}", delta=f"{round(s_pe - b_pe, 1)} vs Sector", delta_color="inverse")
    
    # Beta Comparison
    s_beta = info.get('beta', 0)
    b_beta = bench_info.get('beta', 1.0) # ETFs usually near 1.0
    col2.metric("Beta", f"{round(s_beta, 2)}", delta=f"{round(s_beta - b_beta, 2)} vs Sector", delta_color="inverse")
    
    # Price Trend (Alpha)
    price = info.get('currentPrice', 0)
    ma50 = info.get('fiftyDayAverage', 1)
    alpha_val = round(((price - ma50) / ma50) * 100, 1)
    col3.metric("Alpha (50D)", f"{alpha_val}%", delta=f"{alpha_val}%")

    # --- ROW 2: Insights ---
    st.divider()
    if s_pe < b_pe:
        st.success(f"✅ **Value Play:** {symbol} is trading at a lower multiple than the {b_ticker} average.")
    else:
        st.warning(f"⚠️ **Premium Pricing:** {symbol} is more expensive than its sector benchmark.")
