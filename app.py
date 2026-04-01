with main_col:
    st.subheader(f"{ticker} 6M Mountain Chart")
    
    # 1. Generate a date range for the last 180 days ending today (Mar 31, 2026)
    end_date = datetime.date(2026, 3, 31)
    date_list = pd.date_range(end=end_date, periods=180)
    
    # 2. Create the data and SET THE INDEX to the dates
    np.random.seed(42)
    data = np.random.normal(0, 12, size=(180, 1)).cumsum(axis=0) + 300
    chart_data = pd.DataFrame(data, columns=['Price'], index=date_list)
    
    # 3. Render - Streamlit will now show Dates instead of 0-180
    st.area_chart(chart_data, color="#4eb3ff", use_container_width=True)
    
    st.info(f"🗞️ **{ticker} Sentiment:** Bullish. Relief rally in progress.")
