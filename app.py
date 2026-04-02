# --- STEP 1: SETUP (MUST BE LINES 1 & 2) ---
import streamlit as st  # Fixes the NameError
import yfinance as yf    # Powers all market data

# --- STEP 2: SIDEBAR CONTROLS ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trailing_stop_pct = st.sidebar.slider("Trailing Stop %", 1, 20, 9)
ticker_input = st.sidebar.text_input("Ticker for Volume Check", value="PBR")

# --- STEP 3: ALPHA ENGINE (80% PATH) ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")
    
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

# --- STEP 4: INSTITUTIONAL FLOW ---
st.subheader("🏦 Institutional Flow")
if ticker_input:
    data = yf.Ticker(ticker_input).history(period="5d")
    if not data.empty:
        vol_ratio = data['Volume'].iloc[-1] / data['Volume'].mean()
        if vol_ratio > 1.5:
            st.success(f"🔥 VOLUME SURGE: {round(vol_ratio, 2)}x Normal Volume")
        else:
            st.write(f"Volume is normal ({round(vol_ratio, 2)}x avg).")

# --- STEP 5: ALPHA SPREAD & RELATIVE STRENGTH ---
st.subheader("📊 Alpha Spread")
spy = yf.download("SPY", period="1mo")
if ticker_input and not spy.empty:
    ticker_data = yf.download(ticker_input, period="1mo")
    if not ticker_data.empty:
        # Performance calculations
        spy_perf = ((spy['Close'].iloc[-1] - spy['Close'].iloc[0]) / spy['Close'].iloc[0]) * 100
        tick_perf = ((ticker_data['Close'].iloc[-1] - ticker_data['Close'].iloc[0]) / ticker_data['Close'].iloc[0]) * 100
        spread = tick_perf - spy_perf
        
        st.metric("S&P 500 (1mo)", f"{round(float(spy_perf), 2)}%")
        st.metric("Alpha Spread", f"{round(float(spread), 2)}%", delta=f"{round(float(spread), 2)}%")
