# --- STEP 5: INSTITUTIONAL FOOTPRINT ---
st.subheader("🏦 Institutional Flow")
ticker_input = st.sidebar.text_input("Ticker for Volume Check", value="PBR")

if ticker_input:
    data = yf.Ticker(ticker_input).history(period="5d")
    if not data.empty:
        avg_vol = data['Volume'].mean()
        curr_vol = data['Volume'].iloc[-1]
        vol_ratio = curr_vol / avg_vol

        if vol_ratio > 1.5:
            st.success(f"🔥 VOLUME SURGE: {round(vol_ratio, 2)}x Normal Volume")
            st.info("Institutional 'Big Money' may be entering the position.")
        else:
            st.write(f"Volume is normal ({round(vol_ratio, 2)}x avg).")
