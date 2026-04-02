# --- STEP 1: DEFINE THE BUY ZONE PARAMETERS ---
# We use a 2% buffer around your floor for the "conviction zone"
entry_floor = st.sidebar.number_input("Institutional Floor Price", value=0.0, step=0.1)

# --- STEP 2: THE ALERT ENGINE ---
if entry_floor > 0 and 'info' in locals():
    current_price = info.get('currentPrice', 0)
    
    # Calculate the distance to the floor
    price_diff = ((current_price - entry_floor) / entry_floor) * 100
    
    st.subheader("🛡️ Strategic Entry Status")
    
    if 0 <= price_diff <= 2.0:
        # Visual Green Alert for the "Buy Zone"
        st.success(f"✅ **IN BUY ZONE:** Price is only {round(price_diff, 2)}% above floor (${entry_floor})")
        st.balloons() # Optional: Celebration for hitting the target pullback
    elif price_diff < 0:
        st.warning(f"⚠️ **BELOW FLOOR:** Price (${current_price}) has broken the support level.")
    else:
        st.info(f"⌛ **WAITING:** Price is {round(price_diff, 2)}% away from the Buy Zone.")
