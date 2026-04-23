# --- [TAB 3: HEAT MAP - REBUILT] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Momentum (RVOL)")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        h_list = []
        for h in h_tickers:
            try:
                # Direct RVOL calculation
                rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                h_list.append({
                    "Ticker": h,
                    "RVOL": rvol,
                    "Price": h_data[h]['Close'].iloc[-1],
                    "Intensity": "🚨 EXTREME" if rvol > 2.2 else "🔥 HIGH" if rvol > 1.5 else "Normal"
                })
            except: continue
        
        df_h = pd.DataFrame(h_list)

        # MANUAL COLOR LOGIC (No Matplotlib required)
        def color_rvol(val):
            color = '#00FF00' if val > 2.0 else '#008000' if val > 1.5 else ''
            # Using black text for the high-intensity green cells for readability
            text_color = 'black' if val > 1.5 else 'white'
            return f'background-color: {color}; color: {text_color}'

        # Display using the reliable dataframe engine
        st.dataframe(
            df_h.style.applymap(color_rvol, subset=['RVOL'])
            .format({"RVOL": "{:.2f}x", "Price": "${:.2f}"}),
            use_container_width=True,
            hide_index=True
        )
        st.info("Strategy: Green highlights represent 1.5x+ volume accumulation.")
