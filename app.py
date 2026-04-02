# --- STEP 5: MULTI-ALPHA TRACKER ---
st.subheader("📊 Portfolio Alpha Spread")

# Define your core holdings and watchlist
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
spy = yf.download("SPY", period="1mo")

if not spy.empty:
    spy_prices = spy['Close'].values.flatten()
    spy_perf = ((spy_prices[-1] - spy_prices[0]) / spy_prices[0]) * 100
    
    st.metric("S&P 500 (1mo) Benchmark", f"{round(spy_perf, 2)}%")
    
    # Create columns for your holdings
    cols = st.columns(len(portfolio))
    for i, ticker in enumerate(portfolio):
        tick_data = yf.download(ticker, period="1mo")
        if not tick_data.empty:
            t_prices = tick_data['Close'].values.flatten()
            t_perf = ((t_prices[-1] - t_prices[0]) / t_prices[0]) * 100
            alpha = t_perf - spy_perf
            
            # Display each as a metric
            cols[i].metric(ticker, f"{round(alpha, 2)}%", delta=f"{round(t_perf, 2)}% Abs")
