def moonshot_filter():
    st.subheader("🔭 400% Club: Institutional Footprint")
    # Candidates with massive 2026 backlogs
    scout_list = ["ORCL", "BE", "ETN", "MTZ", "GEV"]
    
    for t in scout_list:
        ticker = yf.Ticker(t)
        # Check if the RS is leading (Price > 200-day MA & 50-day MA)
        # And if 'Up Volume' > 'Down Volume' over 30 days
        st.write(f"Scanning {t} for 'Legit' Re-rating Signals...")
