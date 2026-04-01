import streamlit as st
import yfinance as yf

# --- CACHE ENGINE: Essential to prevent IP lockout (cite: image_c59acc) ---
@st.cache_data(ttl=1800)
def get_terminal_metrics(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception:
        return None

# --- UI HEADER ---
st.title("🛡️ Alpha Terminal")
symbol = "SLB" # Standard energy sector benchmark
info = get_terminal_metrics(symbol)

if info:
    # Creating a cleaner 3-column dashboard (cite: image_c8d88b)
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
        # Delta shows green for positive performance (cite: image_c8d88b)
        col3.metric("Alpha (50D)", f"{alpha_val}%", delta=f"{alpha_val}%")
    else:
        col3.metric("Alpha (50D)", "N/A")

    # --- NEW: VOLATILITY INSIGHT ---
    st.divider()
    if beta:
        status = "Conservative" if beta < 1.0 else "Aggressive"
        st.info(f"**Current Profile:** {status} ({symbol} is {round((1-beta)*100)}% less volatile than the market)")

else:
    # Fallback to prevent app crash (cite: image_7f34e8)
    st.warning("Data sync cooling down. Please wait 10-15 minutes for terminal reset.")
