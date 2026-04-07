# Add this to your Strategy Notes in the app
st.subheader("🛡️ The Trend Guard: Exit Markers")
st.markdown("""
| Signal | Condition | Action |
| :--- | :--- | :--- |
| **9-EMA Floor** | Daily Close < 9-EMA | **Sell 50%** - Trend is weakening. |
| **Band Pierce** | Candle outside Upper BB | **Harvest** - Statistical extreme reached. |
| **Divergence** | Price Up / RSI Down | **Tighten Stops** - Momentum is fading. |
""")
