# --- STEP 6: ALPHA SPREAD (THE "BEAT THE MARKET" METRIC) ---
st.subheader("📊 Alpha Spread")

if ticker_input:
    # Fetch ticker performance
    ticker_data = yf.download(ticker_input, period="1mo")
    if not ticker_data.empty:
        ticker_perf = ((ticker_data['Close'].iloc[-1] - ticker_data['Close'].iloc[0]) / ticker_data['Close'].iloc[0]) * 100
        
        # Calculate the Spread
        # positive = outperforming market | negative = lagging market
        spread = ticker_perf - spy_perf
        
        col_a, col_b = st.columns(2)
        col_a.metric(f"{ticker_input} (1mo)", f"{round(float(ticker_perf), 2)}%")
        col_b.metric("Alpha Spread", f"{round(float(spread), 2)}%", delta=f"{round(float(spread), 2)}%")
