def trade_scout():
    st.title("🔭 New Trade Scout")
    
    # The 2026 "Power Trio"
    scout_tickers = ["BE", "MTZ", "CCJ"]
    
    for ticker in scout_tickers:
        t_obj = yf.Ticker(ticker)
        # Getting today's volume vs 10-day average
        hist = t_obj.history(period="10d")
        avg_vol = hist['Volume'].mean()
        curr_vol = hist['Volume'].iloc[-1]
        
        col1, col2 = st.columns([1, 3])
        
        # ALERT: If volume is 2x average, show a "BUY SIGNAL"
        if curr_vol > (avg_vol * 2):
            col1.success(f"🔥 {ticker} BREAKOUT")
        else:
            col1.info(f"🔎 {ticker} Tracking")
            
        with col2:
            st.write(f"**{ticker}** | Volume: {curr_vol:,.00f} vs Avg: {avg_vol:,.00f}")
            st.progress(min(curr_vol/avg_vol/3, 1.0)) # Visual bar of volume intensity
