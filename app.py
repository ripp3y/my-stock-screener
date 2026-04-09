# --- Update for your 'tab2' (Financials) ---
with tab2:
    intel = hardwired_intel[sel]
    # Fetching the most recent surprise from Yahoo
    try:
        surprises = yf.Ticker(sel).earnings_dates
        last_surprise = surprises['Surprise(%)'].dropna().iloc[0] if 'Surprise(%)' in surprises.columns else 0.0
    except:
        last_surprise = 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Institutional Own", f"{intel['own']}%")
    c2.metric("Next Earnings", intel['earn'])
    
    # Surprise Meter
    s_label = "BEAT" if last_surprise > 0 else "MISS" if last_surprise < 0 else "FLAT"
    c3.metric("Last Surprise", f"{last_surprise:+.1f}%", delta=s_label)
    
    c4.metric("Target Price", f"${intel['target']}")
    
    # Tactical Advice
    if last_surprise > 10 and intel['own'] > 70:
        st.success(f"🔥 CONVICTION: {sel} is a consistent 'Beater' with high institutional backing.")
    elif last_surprise < 0:
        st.warning(f"⚠️ CAUTION: {sel} missed expectations last time. Watch the 9-EMA floor closely.")
