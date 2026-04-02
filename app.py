# --- STEP 7: BUY ZONE INTELLIGENCE ---
st.sidebar.divider()
st.sidebar.header("🛒 Tactical Buy Zones")

# Logic: If price is near or below your purchase target
for item in sorted_grid:
    ticker = item['Ticker']
    # Simplified logic assuming current market price vs sidebar value
    # You can expand this with live yf price data
    if item['Return'] < 20: 
        st.sidebar.warning(f"**{ticker}**: Accumulation Zone")
        st.sidebar.caption(f"Momentum is low ({item['Return']}%). Potential entry point.")
