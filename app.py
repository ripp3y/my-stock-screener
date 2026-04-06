def rotation_matrix():
    st.subheader("🔄 Sector Rotation Matrix (Foresee the Move)")
    
    # Compare Sector ETFs vs S&P 500
    sectors = {
        "Energy (XLE)": "XLE",
        "Industrials (XLI)": "XLI",
        "Materials (XLB)": "XLB",
        "Tech (XLK)": "XLK"
    }
    
    comparison_data = yf.download(list(sectors.values()) + ["SPY"], period="3mo")['Close']
    
    # Calculate Relative Strength (Sector / SPY)
    rs_df = pd.DataFrame()
    for name, ticker in sectors.items():
        rs_df[name] = comparison_data[ticker] / comparison_data["SPY"]
    
    st.line_chart(rs_df, title="Relative Strength vs. S&P 500 (Up = Pulling Ahead)")
    
    st.info("💡 **Alpha Tip:** If the line for Energy (XLE) is curving down, it's a 'Pullback' signal. If Industrials (XLI) is curving up, it's a 'Pull-Ahead' candidate.")
    
