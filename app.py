# --- STEP 5: ALPHA SPREAD & BENCHMARK ---
st.subheader("📊 Alpha Spread")

# Fetch S&P 500 (Benchmark)
spy = yf.download("SPY", period="1mo")
if ticker_input and not spy.empty:
    ticker_data = yf.download(ticker_input, period="1mo")
    if not ticker_data.empty:
        # FIX: Select the last item [-1] and convert to float
        spy_start = float(spy['Close'].iloc[0])
        spy_end = float(spy['Close'].iloc[-1])
        tick_start = float(ticker_data['Close'].iloc[0])
        tick_end = float(ticker_data['Close'].iloc[-1])

        # Performance calculations
        spy_perf = ((spy_end - spy_start) / spy_start) * 100
        tick_perf = ((tick_end - tick_start) / tick_start) * 100
        spread = tick_perf - spy_perf
        
        # Display Metrics
        col1, col2 = st.columns(2)
        col1.metric("S&P 500 (1mo)", f"{round(spy_perf, 2)}%")
        col2.metric("Alpha Spread", f"{round(spread, 2)}%", delta=f"{round(spread, 2)}%")
