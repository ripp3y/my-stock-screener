def alpha_scout():
    st.title("🚀 Alpha Scout: 100% Club Hunter")
    
    # FIX: Using 'PBR-A' (dash) instead of 'PBR.A' (period)
    power_tickers = ["GEV", "BW", "PBR-A", "EQNR"]
    
    try:
        p_data = yf.download(power_tickers, period="5d")['Close'].iloc[-1]
        
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("GEV", f"${p_data['GEV']:.2f}", "Target: $1,735")
        p2.metric("BW", f"${p_data['BW']:.2f}", "Target: $25.00")
        p3.metric("PBR-A", f"${p_data['PBR-A']:.2f}", "Div: Apr 24")
        p4.metric("EQNR", f"${p_data['EQNR']:.2f}", "Sell: Wed")
    except Exception as e:
        st.error(f"Data Sync Error: {e}")

    st.divider()

    # 2. Breakout Scanner with updated width parameter
    st.subheader("🛡️ Breakout & Pullback Foreseer")
    scan_ticker = st.text_input("Enter Ticker to Scan", value="PBR-A").upper()
    
    if scan_ticker:
        t_obj = yf.Ticker(scan_ticker)
        hist = t_obj.history(period="1mo")
        # Updated 'width' to clear deprecation warnings in your logs
        st.line_chart(hist['Close'], width='stretch')
