def alpha_scout():
    st.title("🚀 Alpha Scout: 100% Club Hunter")
    
    # 1. THE POWER WALL (AI Infrastructure Watchlist)
    st.subheader("⚡ The Power Wall")
   power_tickers = ["GEV", "BW", "PBR-A", "EQNR"] # Swapped CAT/FLR for your core holdings
    p_data = yf.download(power_tickers, period="5d")['Close'].iloc[-1]
    
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("GEV", f"${p_data['GEV']:.2f}", "Target: $1,735")
    p2.metric("BW", f"${p_data['BW']:.2f}", "Target: $25.00")
    p3.metric("CAT", f"${p_data['CAT']:.2f}", "Heavy Equipment")
    p4.metric("FLR", f"${p_data['FLR']:.2f}", "Engineering")
    st.caption("💡 Institutional volume is currently heavy in GEV and BW as AI grid demand spikes.")

    st.divider()

    # 2. VOLUME BREAKOUT SCANNER
    st.subheader("🛡️ Breakout & Pullback Foreseer")
    scan_ticker = st.text_input("Enter Ticker to Scan", value="EQNR").upper()
    
    if scan_ticker:
        ticker_obj = yf.Ticker(scan_ticker)
        hist = ticker_obj.history(period="1mo")
        
        # Calculate Volume Spike (Current Volume vs 20-Day Average)
        avg_vol = hist['Volume'].iloc[:-1].mean()
        curr_vol = hist['Volume'].iloc[-1]
        vol_ratio = curr_vol / avg_vol
        
        # Calculate RSI for Pullback Warning
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        c1, c2 = st.columns(2)
        with c1:
            if vol_ratio > 2.0:
                st.success(f"🔥 BREAKOUT ALERT: {scan_ticker} volume is {vol_ratio:.1f}x normal!")
            else:
                st.info(f"Normal Volume: {vol_ratio:.1f}x average.")
                
        with c2:
            if rsi > 70:
                st.error(f"⚠️ PULLBACK RISK: RSI is {rsi:.1f} (Overbought).")
            elif rsi < 30:
                st.success(f"📈 BUY ZONE: RSI is {rsi:.1f} (Oversold).")
            else:
                st.write(f"Momentum: Neutral (RSI {rsi:.1f})")
