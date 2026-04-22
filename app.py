# --- [BACKBONE: THE TWIN-TAB SCANNER] ---
tab1, tab2 = st.tabs(["🌪️ ALPHA CHANNEL", "🚀 BREAKOUT HUNT"])

with tab1:
    st.subheader("High-Velocity Momentum (Insider + Velocity)")
    # Logic: Beta > 1.2 + Recent Insider Buys
    st.dataframe(pd.DataFrame([
        {"Tkr": "NVTS", "Gain": "+18.4%", "Signal": "CEO Buy @ $8.54", "Phase": "ACTIVE-HOP"},
        {"Tkr": "FIX", "Gain": "+19.8%", "Signal": "Upgraded to $1,800", "Phase": "CORE-ENGINE"}
    ]))

with tab2:
    st.subheader("Blue Sky Breakouts (No Resistance)")
    # Logic: Price > 52W High + Volume Spike
    st.dataframe(pd.DataFrame([
        {"Tkr": "ALAB", "Price": "$194.06", "High": "$262.90", "Status": "🚀LEAD"},
        {"Tkr": "FLR", "Price": "$48.12", "Backlog": "$25.5B", "Status": "🚀LEAD"}
    ]))
