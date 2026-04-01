# --- GLOBAL INPUTS (Top of Script) ---
# Ensure this variable exists before the Target Alpha logic runs
buy_price = st.sidebar.number_input("Enter Purchase Price", value=0.0, step=0.1)

# --- TARGET ALPHA: THE 80% PATH ---
st.header("🎯 Target Alpha: The 80% Path")

# Now the variable is guaranteed to be defined
if buy_price > 0:
    # Calculate the 'Moon' price
    target_80 = buy_price * 1.80
    target_100 = buy_price * 2.00
    
    st.success(f"🚀 **80% Target:** ${round(target_80, 2)}")
    st.info(f"🌕 **100% Target:** ${round(target_100, 2)}")
else:
    st.warning("Please enter a Purchase Price in the sidebar to visualize your targets.")
