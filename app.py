# --- STEP 5: MARKET RELATIVE STRENGTH ---
st.subheader("📈 Market Relative Strength")

# Fetch S&P 500 Benchmark data
spy = yf.download("SPY", period="1mo")
if not spy.empty:
    # Calculate monthly performance
    spy_perf = ((spy['Close'].iloc[-1] - spy['Close'].iloc[0]) / spy['Close'].iloc[0]) * 100
    
    # Display as a metric with Benchmark labeling
    st.metric("S&P 500 (1mo)", f"{round(float(spy_perf), 2)}%", help="Benchmark performance")
