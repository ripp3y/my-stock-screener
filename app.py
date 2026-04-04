import streamlit as st

# --- TAB 2: PROFIT HARVESTER ---
with st.expander("💰 Profit Harvest Calculator", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Adding unique 'key' parameters prevents the Duplicate ID error
        target_cash = st.number_input("Target Harvest ($)", value=2045.50, key="harvest_target_input")
        asset = st.selectbox("Source Asset", ["EQNR", "PBR", "CENX"], key="harvest_asset_select")
        
    # Example of a second calculator that would cause a conflict without unique keys:
    # secondary_cash = st.number_input("Target Harvest ($)", value=1000.0, key="secondary_target_input")
# --- TAB 2: PROFIT HARVESTER ---
with st.expander("💰 Profit Harvest Calculator", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_cash = st.number_input("Target Harvest ($)", value=2045.50)
        ticker_select = st.selectbox("Source Asset", ["EQNR", "PBR", "CENX"])
        
    # Using your known metrics for EQNR
    current_price = 28.50  # Static placeholder until sync resets
    cost_basis = 25.00
    
    shares_needed = target_cash / current_price
    total_profit = (current_price - cost_basis) * shares_needed
    
    with col2:
        st.metric("Shares to Liquivate", f"{shares_needed:.2f}")
        st.write(f"Estimated Taxable Gain: ${total_profit:.2f}")
        
    with col3:
        if st.button("✅ Log Intent to Harvest"):
            st.success(f"Harvest of {ticker_select} staged for execution.")
