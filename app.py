def alpha_scout():
    st.title("🔭 Alpha Scout: Hunting the 100% Club")
    
    # Tracking the 'Power Trio' and your current Energy plays
    scout_list = ["BE", "MTZ", "CCJ", "GEV", "BW", "PBR-A"]
    
    for ticker in scout_list:
        t_obj = yf.Ticker(ticker)
        hist = t_obj.history(period="10d")
        
        # Calculate Volume Intensity
        avg_vol = hist['Volume'].mean()
        curr_vol = hist['Volume'].iloc[-1]
        vol_ratio = curr_vol / avg_vol
        
        col1, col2 = st.columns([1, 2])
        
        # HIT SIGNAL: 2x Volume is the Institutional 'Buy'
        if vol_ratio > 2.0:
            col1.success(f"🔥 BREAKOUT: {ticker}")
        elif vol_ratio > 1.5:
            col1.warning(f"⚡ ACCUMULATION: {ticker}")
        else:
            col1.info(f"🔎 MONITORING: {ticker}")
            
        with col2:
            st.write(f"Price: **${hist['Close'].iloc[-1]:.2f}** | Vol Ratio: **{vol_ratio:.2f}x**")
