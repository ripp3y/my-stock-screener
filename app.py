def home_page():
    st.title("🏠 Command Center")
    
    # 1. Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("PBR.A Yield on Cost", "596.1%", delta="Anchor Safe")
    with col2:
        st.metric("Portfolio Diversification", "68.9%", delta="Target: 70.3%")
    with col3:
        st.metric("Sector Leader", "Energy (XLE)", delta="+32.9% YTD")

    st.divider()

    # 2. THE POWER WALL (B: AI Infrastructure Plays)
    st.subheader("⚡ The Power Wall (100% Club Candidates)")
    p_col1, p_col2, p_col3 = st.columns(3)
    p_col1.metric("GEV", "$899.35", "Target: $1,735")
    p_col2.metric("BW", "$15.72", "Target: $25.00")
    p_col3.metric("KOS", "$4.20", "Top Energy Performer")
    st.caption("💡 These stocks own the electrical grid and fuel for AI data centers.")

    st.divider()

    # 3. BREAKOUT SCANNER (C: Technical Foreseer)
    st.subheader("🛡️ Breakout & Pullback Scanner")
    scan_ticker = st.text_input("Enter Ticker to Scan for Pullback Risk", value="EQNR").upper()
    
    if scan_ticker:
        t_data = yf.Ticker(scan_ticker)
        hist = t_data.history(period="3mo")
        
        # Calculate RSI (Simplified logic)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        current_rsi = hist['RSI'].iloc[-1]
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.line_chart(hist[['Close', 'RSI']], height=300)
        with c2:
            if current_rsi > 70:
                st.error(f"⚠️ {scan_ticker} is OVERBOUGHT (RSI: {current_rsi:.1f}). Pullback Likely.")
            elif current_rsi < 30:
                st.success(f"🔥 {scan_ticker} is OVERSOLD (RSI: {current_rsi:.1f}). Buy Opportunity.")
            else:
                st.info(f"✅ {scan_ticker} RSI: {current_rsi:.1f} (Neutral Momentum)")

    st.divider()
    
    # 4. Manual Harvest Logger
    st.subheader("📝 Manual Harvest Logger")
    with st.expander("Record your Wednesday Sell"):
        sell_p = st.number_input("Sell Price ($)", value=41.67)
        sell_q = st.number_input("Shares", value=49.15)
        if st.button("Confirm Harvest"):
            st.success(f"Harvested ${sell_p * sell_q:,.2f}. Goal Achieved.")
