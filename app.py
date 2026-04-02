# --- STEP 5: ALPHA SPREAD (THE MULTI-INDEX FIX) ---
st.subheader("📊 Alpha Spread")
spy = yf.download("SPY", period="1mo")
if ticker_input and not spy.empty:
    ticker_data = yf.download(ticker_input, period="1mo")
    if not ticker_data.empty:
        # FIX: Flatten MultiIndex headers to get single numeric values
        # This ensures float() gets a number, not a table
        spy_prices = spy.xs('Close', axis=1) if isinstance(spy.columns, pd.MultiIndex) else spy['Close']
        tick_prices = ticker_data.xs('Close', axis=1) if isinstance(ticker_data.columns, pd.MultiIndex) else ticker_data['Close']

        spy_start = float(spy_prices.iloc[0])
        spy_end = float(spy_prices.iloc[-1])
        tick_start = float(tick_prices.iloc[0])
        tick_end = float(tick_prices.iloc[-1])

        # Calculation & Display
        spy_perf = ((spy_end - spy_start) / spy_start) * 100
        tick_perf = ((tick_end - tick_start) / tick_start) * 100
        spread = tick_perf - spy_perf
        
        st.metric("S&P 500 (1mo)", f"{round(spy_perf, 2)}%")
        st.metric("Alpha Spread", f"{round(spread, 2)}%", delta=f"{round(spread, 2)}%")
