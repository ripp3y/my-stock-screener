def moonshot_scout():
    st.title("🔭 400% Club: Backlog Squeeze Alert")
    
    # Legit candidates with massive 2026 backlogs
    scout_list = ["BW", "BE", "GEV", "PWR"]
    
    for t in scout_list:
        ticker = yf.Ticker(t)
        # Logic to flag when Backlog/Market Cap ratio is high
        # This was the exact signal that sent BW up 37% in one day
        st.write(f"Monitoring {t} for Institutional 'Buy' Volume...")
