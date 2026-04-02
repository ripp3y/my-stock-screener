# --- STEP 4: PORTFOLIO ALPHA WITH MILESTONE ALERTS ---
st.subheader("📊 Portfolio Alpha Spread")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
spy = yf.download("SPY", period="1mo")

if not spy.empty:
    spy_prices = spy['Close'].values.flatten()
    spy_perf = ((spy_prices[-1] - spy_prices[0]) / spy_prices[0]) * 100
    st.caption(f"S&P 500 (1mo) Benchmark: {round(spy_perf, 2)}%")
    
    cols = st.columns(len(portfolio))
    for i, ticker in enumerate(portfolio):
        t_data = yf.download(ticker, period="1mo")
        if not t_data.empty:
            t_prices = t_data['Close'].values.flatten()
            curr_price = float(t_prices[-1])
            t_perf = ((curr_price - t_prices[0]) / t_prices[0]) * 100
            alpha = t_perf - spy_perf
            
            # --- MILESTONE LOGIC ---
            # Compare current price to your buy_price input
            gain = (curr_price - buy_price) / buy_price
            
            label_prefix = ""
            if gain >= 0.50:
                label_prefix = "🥇 " # Gold for 50%
            elif gain >= 0.20:
                label_prefix = "🥉 " # Bronze for 20%
                
            cols[i].metric(
                label=f"{label_prefix}{ticker}", 
                value=f"{round(alpha, 2)}%", 
                delta=f"{round(t_perf, 2)}% Abs"
            )
