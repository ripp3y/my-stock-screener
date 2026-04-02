# --- STEP 1: INITIALIZE (MUST BE AT THE TOP) ---
import streamlit as st  
import yfinance as yf    

# --- STEP 2: SIDEBAR INPUTS ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=23.0, step=0.1)
ticker_input = st.sidebar.text_input("Ticker for Volume Check", value="PBR")

# --- STEP 3: THE ALPHA ENGINE (80% PATH) ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")
    
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.2, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.5, 2)}")

# --- STEP 4: INSTITUTIONAL FLOW ---
st.subheader("🏦 Institutional Flow")
if ticker_input:
    data = yf.Ticker(ticker_input).history(period="5d")
    if not data.empty:
        vol_ratio = data['Volume'].iloc[-1] / data['Volume'].mean()
        st.write(f"Volume is normal ({round(vol_ratio, 2)}x avg).")

# --- STEP 5: ALPHA SPREAD (THE FIX) ---
st.subheader("📊 Alpha Spread")
spy = yf.download("SPY", period="1mo")
if ticker_input and not spy.empty:
    ticker_data = yf.download(ticker_input, period="1mo")
    if not ticker_data.empty:
        # FIX: Explicitly select the first and last values
        spy_start = float(spy['Close'].iloc[0])
        spy_end = float(spy['Close'].iloc[-1])
        tick_start = float(ticker_data['Close'].iloc[0])
        tick_end = float(ticker_data['Close'].iloc[-1])

        # Calculate Percentages
        spy_p = ((spy_end - spy_start) / spy_start) * 100
        tick_p = ((tick_end - tick_start) / tick_start) * 100
        spread = tick_p - spy_p
        
        # Display Metrics
        c1, c2 = st.columns(2)
        c1.metric("S&P 500 (1mo)", f"{round(spy_p, 2)}%")
        c2.metric("Alpha Spread", f"{round(spread, 2)}%", delta=f"{round(spread, 2)}%")
