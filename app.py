import streamlit as st
import yfinance as yf

# --- CACHE ENGINE ---
@st.cache_data(ttl=1800)
def get_analysis_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        sector = info.get('sector', '')
        b_symbol = "XLE" if "Energy" in sector else "XLI" if "Industrials" in sector else "SPY"
        bench_info = yf.Ticker(b_symbol).info
        return info, bench_info, b_symbol
    except:
        return None, None, None

# --- SIDEBAR CONTROL ---
target_stock = st.sidebar.selectbox("Select Ticker", ["SLB", "PBR-A", "CENX", "EQNR"])

st.title(f"🛡️ Alpha Terminal: {target_stock}")
info, bench, b_ticker = get_analysis_data(target_stock)

if info:
    # 1. FETCH 52-WEEK DATA
    curr = info.get('currentPrice')
    low_52 = info.get('fiftyTwoWeekLow')
    high_52 = info.get('fiftyTwoWeekHigh')

    # 2. CALCULATE POSITION
    # Where are we between 0 (Low) and 100 (High)?
    total_range = high_52 - low_52
    position = ((curr - low_52) / total_range) * 100

    # 3. VISUALIZE ZONE
    st.subheader("Yearly Price Position")
    # A read-only slider acts as a visual progress bar
    st.select_slider(
        "Current Position vs. 52-Week Range",
        options=["52W Low", "Value Zone", "Neutral", "Momentum Zone", "52W High"],
        value=("Value Zone" if position < 30 else "Momentum Zone" if position > 70 else "Neutral"),
        disabled=True
    )
    
    st.write(f"Current Price: **${curr}** | Range: **${low_52} - ${high_52}**")

    # 4. ACTION LOGIC
    if position < 25:
        st.success(f"💎 **BUY ZONE:** {target_stock} is trading within 25% of its yearly low. Potential value entry.")
    elif position > 85:
        st.error(f"🚀 **RESISTANCE ZONE:** {target_stock} is nearing its 52-week high. Watch for profit-taking.")
    else:
        st.info(f"⚖️ **NEUTRAL ZONE:** {target_stock} is currently in the middle of its yearly range.")

    # --- SECTOR COMPARISON ROW (from previous build) ---
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Forward PE", f"{round(info.get('forwardPE', 0), 1)}", f"{round(info.get('forwardPE', 0) - bench.get('forwardPE', 0), 1)} vs {b_ticker}")
    c2.metric("Beta", f"{round(info.get('beta', 0), 2)}", f"{round(info.get('beta', 0) - bench.get('beta', 1.0), 2)} vs {b_ticker}")
    
    ma50 = info.get('fiftyDayAverage', 1)
    alpha = round(((curr - ma50) / ma50) * 100, 1)
    c3.metric("Alpha (50D)", f"{alpha}%", f"{alpha}%")
