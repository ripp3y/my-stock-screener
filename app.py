import streamlit as st
import yfinance as yf

# --- CACHE ENGINE: Essential for preventing API lockouts ---
@st.cache_data(ttl=1800)
def get_alpha_terminal_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# --- UI RENDER ---
st.title("🛡️ Alpha Terminal")
symbol = "SLB"
info = get_alpha_terminal_data(symbol)

if info:
    col1, col2, col3 = st.columns(3)
    
    # 1. Valuation
    f_pe = info.get('forwardPE')
    col1.metric("Forward PE", f"{round(f_pe, 1)}" if f_pe else "N/A")
    
    # 2. Risk Sensitivity
    beta = info.get('beta')
    col2.metric("Beta", f"{round(beta, 2)}" if beta else "N/A")
    
    # 3. Performance Trend
    price = info.get('currentPrice')
    ma50 = info.get('fiftyDayAverage')
    if price and ma50:
        alpha_val = round(((price - ma50) / ma50) * 100, 1)
        col3.metric("Alpha (50D)", f"{alpha_val}%", delta=f"{alpha_val}%")
    else:
        col3.metric("Alpha (50D)", "N/A")

    # Dynamic Analysis Section
    st.divider()
    if beta:
        status = "Conservative" if beta < 1.0 else "Aggressive"
        risk_diff = abs(round((1 - beta) * 100))
        st.info(f"**Current Profile:** {status} ({symbol} is {risk_diff}% {'less' if beta < 1 else 'more'} volatile than the market)")
else:
    st.warning("Data sync cooling down. Metrics will restore automatically.")
