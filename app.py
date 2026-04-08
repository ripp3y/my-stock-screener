# --- Updated Dynamic Ranking Logic ---

try:
    data = fetch_ticker_data(team_tickers)
    
    # 1. First, calculate metrics for EVERY ticker and store them in a list
    ticker_stats = []
    for ticker in team_tickers:
        ticker_df = data[ticker].dropna()
        rsi_series, _, pct_dist, bottom_signal = get_technical_signals(ticker_df)
        
        ticker_stats.append({
            "ticker": ticker,
            "price": ticker_df['Close'].iloc[-1],
            "cushion": pct_dist,
            "rsi": rsi_series.iloc[-1],
            "bottom": bottom_signal
        })

    # 2. SORT the list: Best performing (highest cushion) goes first
    sorted_stats = sorted(ticker_stats, key=lambda x: x['cushion'], reverse=True)

    # 3. Now, display the metrics using the SORTED list
    cols = st.columns(len(sorted_stats))
    for i, stat in enumerate(sorted_stats):
        with cols[i]:
            st.metric(stat['ticker'], f"${stat['price']:.2f}", f"{stat['cushion']:+.1f}% Floor")
            
            # Smart Status logic using the sorted data
            if stat['bottom']: st.success("🎯 BOTTOM FOUND")
            elif stat['cushion'] < 0: st.error("📉 TREND BREAK")
            elif stat['rsi'] > 70: st.warning("🔥 BOOMING")
            else: st.info("🚀 STRONG")

    st.divider()
    # ... rest of your Deep Dive code ...
