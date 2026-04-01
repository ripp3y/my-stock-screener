import streamlit as st
import yfinance as yf

# --- VOLATILITY ENGINE ---
@st.cache_data(ttl=1800)
def get_stop_loss_data(symbol):
    ticker = yf.Ticker(symbol)
    # Fetching 14 days of data for ATR calculation
    hist = ticker.history(period="30d")
    if not hist.empty:
        # ATR Calculation (High - Low)
        hist['Range'] = hist['High'] - hist['Low']
        atr = hist['Range'].tail(14).mean()
        return atr
    return None

# --- UI LOGIC ---
st.header("🛡️ Dynamic Stop Loss Control")
buy_price = st.number_input("Your Purchase Price", value=0.0, step=0.10)
target = st.sidebar.selectbox("Active Ticker", ["PBR-A", "CENX", "EQNR", "INTT", "CNQ"])

atr = get_stop_loss_data(target)

if buy_price > 0 and atr:
    # Aggressive multiplier (2.5x) for 80% return targets
    stop_dist = atr * 2.5
    stop_price = buy_price - stop_dist
    stop_pct = (stop_dist / buy_price) * 100
    
    st.subheader(f"Strategy for {target}")
    c1, c2 = st.columns(2)
    
    # Custom Stop Level
    c1.metric("Calculated Stop", f"${round(stop_price, 2)}", f"-{round(stop_pct, 1)}%", delta_color="inverse")
    
    # Volatility Health
    c2.metric("ATR (14D)", f"${round(atr, 2)}", "Daily 'Noise' Level")

    # --- THE BOSS'S ADVICE ---
    st.divider()
    if stop_pct > 15:
        st.warning(f"⚠️ **High Volatility:** {target} is swinging wide. This stop is deep to avoid being 'shaken out', but requires smaller position sizing.")
    else:
        st.success(f"✅ **Stable Trend:** This stop is tight enough to protect gains without choking the trade.")
