import streamlit as st
import yfinance as yf

# --- CACHE ENGINE ---
@st.cache_data(ttl=1800)
def get_analysis_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        sector = info.get('sector', '')
        # Dynamic benchmark mapping
        b_symbol = "XLE" if "Energy" in sector else "XLI" if "Industrials" in sector else "SPY"
        bench_info = yf.Ticker(b_symbol).info
        return info, bench_info, b_symbol
    except:
        return None, None, None

# --- SIDEBAR CONTROL ---
st.sidebar.header("Alpha Control")
# Core holdings and watchlist
target_stock = st.sidebar.selectbox("Select Ticker", ["SLB", "PBR-A", "CENX", "EQNR", "CNQ", "INTT"])
shares = st.sidebar.number_input("Projected Shares", value=100, step=10)

st.title(f"🛡️ Alpha Terminal: {target_stock}")
info, bench, b_ticker = get_analysis_data(target_stock)

if info:
    # --- 1. PRICE POSITION ---
    curr = info.get('currentPrice')
    low_52, high_52 = info.get('fiftyTwoWeekLow'), info.get('fiftyTwoWeekHigh')
    range_pos = ((curr - low_52) / (high_52 - low_52)) * 100
    
    st.subheader("Yearly Price Position")
    st.select_slider("Range Status", 
        options=["52W Low", "Value Zone", "Neutral", "Momentum Zone", "52W High"],
        value=("Value Zone" if range_pos < 30 else "Momentum Zone" if range_pos > 70 else "Neutral"),
        disabled=True)
    
    # --- 2. SECTOR PRO METRICS ---
    st.divider()
    c1, c2, c3 = st.columns(3)
    
    s_pe = info.get('forwardPE', 0)
    pe_delta = round(s_pe - bench.get('forwardPE', 0), 1)
    c1.metric("Forward PE", f"{round(s_pe, 1)}", f"{pe_delta} vs {b_ticker}", delta_color="inverse")
    
    s_beta = info.get('beta', 0)
    beta_delta = round(s_beta - bench.get('beta', 1.0), 2)
    c2.metric("Beta", f"{round(s_beta, 2)}", f"{beta_delta} vs {b_ticker}", delta_color="inverse")
    
    ma50 = info.get('fiftyDayAverage', 1)
    alpha = round(((curr - ma50) / ma50) * 100, 1)
    c3.metric("Alpha (50D)", f"{alpha}%", f"{alpha}%")

    # --- 3. RISK CALCULATOR ---
    st.divider()
    st.subheader("Allocation Impact")
    position_value = curr * shares
    st.write(f"Total Value of **{shares}** shares: **${position_value:,.2f}**")
    
    # Simple risk insight based on Beta
    if s_beta < 1.0:
        st.info(f"💡 This position acts as a **volatility buffer**. It is {abs(round((1-s_beta)*100))}% less reactive than the S&P 500.")
    else:
        st.warning(f"⚠️ This is an **aggressive position**. It will amplify market moves by {round((s_beta-1)*100)}%.")
