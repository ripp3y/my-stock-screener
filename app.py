# --- STEP 5: ALPHA SPREAD & BENCHMARK ---
st.subheader("📊 Alpha Spread")

# Fetch 1-month data for SPY and your Ticker
spy = yf.download("SPY", period="1mo")
if ticker_input and not spy.empty:
    ticker_data = yf.download(ticker_input, period="1mo")
    if not ticker_data.empty:
        # FIX: Explicitly extract the single value from the Series
        spy_start = float(spy['Close'].iloc[0])
        spy_end = float(spy['Close'].iloc[-1])
        tick_start = float(ticker_data['Close'].iloc[0])
        tick_end = float(ticker_data['Close'].iloc[-1])

        # Performance calculations
        spy_p = ((spy_end - spy_start) / spy_start) * 100
        tick_p = ((tick_end - tick_start) / tick_start) * 100
        alpha_spread = tick_p - spy_p
        
        # Display Metrics
        c1, c2 = st.columns(2)
        c1.metric("S&P 500 (1mo)", f"{round(spy_p, 2)}%")
        c2.metric("Alpha Spread", f"{round(alpha_spread, 2)}%", delta=f"{round(alpha_spread, 2)}%")
