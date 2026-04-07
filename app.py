def moonshot_scout():
    # Filter for the 'Power Alley' candidates
    candidates = ["GEV", "BW", "BE", "MTZ", "CCJ"]
    
    for t in candidates:
        ticker = yf.Ticker(t)
        hist = ticker.history(period="1y")
        
        # 1. Check for RS Line Breakout (Higher Highs while SPY is lower)
        # 2. Check for Volume Accumulation (Up days volume > Down days volume)
        up_vol = hist[hist['Close'] > hist['Open']]['Volume'].mean()
        dn_vol = hist[hist['Close'] < hist['Open']]['Volume'].mean()
        vol_intensity = up_vol / dn_vol
        
        if vol_intensity > 1.5:
            st.success(f"🚀 {t}: Institutional Accumulation detected!")
