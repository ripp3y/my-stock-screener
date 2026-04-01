import streamlit as st
import yfinance as yf

# --- CACHE ENGINE ---
@st.cache_data(ttl=1800)
def get_analysis_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        # Auto-benchmark: XLE for Energy, XLI for Industrials
        sector = info.get('sector', '')
        b_symbol = "XLE" if "Energy" in sector else "XLI" if "Industrials" in sector else "SPY"
        bench_info = yf.Ticker(b_symbol).info
        return info, bench_info, b_symbol
    except:
        return None, None, None

# --- SIDEBAR SELECTOR ---
st.sidebar.header("Alpha Control")
target_stock = st.sidebar.selectbox(
    "Select Ticker", 
    ["SLB", "PBR-A", "CENX", "EQNR"]
)

st.title("🛡️ Alpha Terminal: Sector Pro")
info, bench, b_ticker = get_analysis_data(target_stock)

if info and bench:
    st.subheader(f"Analysis vs. {b_ticker} Benchmark")
    c1, c2, c3 = st.columns(3)
    
    # Valuation vs Sector
    s_pe = info.get('forwardPE', 0)
    b_pe = bench.get('forwardPE', 1)
    pe_delta = round(s_pe - b_pe, 1)
    c1.metric("Forward PE", f"{round(s_pe, 1)}", f"{pe_delta} vs Sector", delta_color="inverse")
    
    # Risk vs Sector
    s_beta = info.get('beta', 0)
    b_beta = bench.get('beta', 1.0)
    beta_delta = round(s_beta - b_beta, 2)
    c2.metric("Beta", f"{round(s_beta, 2)}", f"{beta_delta} vs Sector", delta_color="inverse")
    
    # Momentum
    price, ma50 = info.get('currentPrice', 0), info.get('fiftyDayAverage', 1)
    alpha = round(((price - ma50) / ma50) * 100, 1)
    c3.metric("Alpha (50D)", f"{alpha}%", f"{alpha}%")

    # Dynamic Insights
    st.divider()
    if s_pe > b_pe:
        st.warning(f"⚠️ **Premium Pricing:** {target_stock} is more expensive than its sector benchmark.")
    else:
        st.success(f"✅ **Value Play:** {target_stock} is trading at a discount to the sector.")
