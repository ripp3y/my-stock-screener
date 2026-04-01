import streamlit as st
import pandas as pd
import numpy as np

# ... (Previous Header & Sector Metrics Code) ...

with main_col:
    st.subheader(f"{ticker} 6M Mountain Chart")
    
    # 1. Create data with more "Volatility" to match your original mountain
    chart_data = pd.DataFrame(
        # We increase the 'scale' to 15 to create bigger peaks/valleys
        np.random.normal(0, 15, size=(180, 1)).cumsum(axis=0) + 350,
        columns=['Price']
    )
    
    # 2. FIX THE FLATLINE: 
    # Use use_container_width and don't force a static Y-axis range
    # Streamlit will automatically 'zoom' into the price action
    st.area_chart(
        chart_data, 
        color="#4eb3ff", 
        use_container_width=True
    )
    
    st.info(f"🗞️ **{ticker} Sentiment:** Bullish. Massive relief rally.")
