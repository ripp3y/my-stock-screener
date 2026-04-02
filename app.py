# --- PROFIT HARVEST & ROTATION LOGIC ---
st.sidebar.header("💰 Profit Harvest Tool")
# Focus on tickers currently at "Target Hit" status
harvest_ticker = st.sidebar.selectbox("Ticker to Trim", ["EQNR", "CF"])
shares_owned = st.sidebar.number_input(f"Current {harvest_ticker} Shares", value=98)

# Calculate 50% Trim Value based on live data
current_p = raw_data[harvest_ticker].iloc[-1]
harvest_cash = (shares_owned * 0.5) * current_p

st.sidebar.success(f"Harvested Cash: ${harvest_cash:,.2f}")
st.sidebar.caption(f"Trim Price: ${round(current_p, 2)}")

# --- BUY POWER CALCULATION ---
st.sidebar.divider()
st.sidebar.header("🛒 Deployment Power")
for item in grid_data:
    if item['Return'] < 20: # Identifying laggards
        shares_to_buy = int(harvest_cash / item['Price'])
        st.sidebar.write(f"**{item['Ticker']}**: Buy ~{shares_to_buy} shares")
