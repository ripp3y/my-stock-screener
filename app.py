import streamlit as st
import yfinance as yf

# --- CACHE ENGINE: Prevents API blocks during rapid development (cite: image_c59acc) ---
@st.cache_data(ttl=1800)
def get_terminal_metrics(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# --- UI HEADER ---
st.title("🛡️ Alpha Terminal")
symbol = "SLB" 
info = get_terminal_metrics(symbol)

if info:
    # Top Row: Primary Metrics (cite: image_c92b04)
    col1, col2, col3 = st.columns(3)
    
    # 1. Forward PE: Valuation
    f_pe = info.get('forwardPE')
    col1.metric("Forward PE", f"{round(f_pe, 1)}" if f_pe else "N/A")
    
    # 2. Beta: Market Sensitivity
    beta = info.get('beta')
    col2.metric("Beta", f"{round(beta, 2)}" if beta else "N/A")
    
    # 3. Alpha (50D): Performance vs. Trend
    price = info.get('currentPrice')
    ma50 = info.get('fiftyDayAverage')
    if price and ma50:
        alpha_val = round(((price - ma50) / ma50) * 100, 1)
        col3.metric("Alpha (50D)", f"{alpha_val}%", delta=f"{alpha_val}%")
    else:
        col3.metric("Alpha (50D)", "N/A")

    # Lower Section: Risk Analysis (cite: image_c92b04)
    st.divider()
    if beta:
        # Categorizes the stock based on its Beta coefficient
        status = "Conservative" if beta < 1.0 else "Aggressive"
        # Dynamic description based on current ticker
        risk_desc = f"{symbol} is {abs(round((1-beta)*100))}% {'less' if beta < 1 else 'more'} volatile than the market"
        st.info(f"**Current Profile:** {status} ({risk_desc})")
else:
    # Error state management
    st.warning("Terminal cooling down. Metrics will restore automatically shortly.")
