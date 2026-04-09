# --- Updated tab2 (Financials) with Surprise Logic ---
with tab2:
    intel = hardwired_intel[sel]
    # Fetching historical surprise data
    try:
        surprises = yf.Ticker(sel).earnings_dates
        # Get the most recent surprise percentage
        last_s = surprises['Surprise(%)'].dropna().iloc[0] if 'Surprise(%)' in surprises.columns else 0.0
    except:
        last_s = 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Institutional Own", f"{intel['own']}%")
    c2.metric("Next Earnings", intel['earn'])
    
    # Surprise Gauge: High historical surprise + high institutional ownership = High Conviction
    s_label = "BULLISH HEAT" if last_s > 10 else "NEUTRAL" if last_s >= 0 else "BEARISH HEAT"
    c3.metric("Surprise Scout", f"{last_s:+.1f}%", delta=s_label)
    
    # Tactical Guidance based on 2026 Institutional Trends
    if intel['own'] > 80 and last_s > 5:
        st.success(f"💎 HIGH CONVICTION: Institutions are 'locked in' for a repeat beat.")
    elif last_s < 0:
        st.warning(f"⚠️ VOLATILITY ALERT: {sel} missed last time. Watch the 9-EMA floor.")
