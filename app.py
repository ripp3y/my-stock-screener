# --- STEP 6: THE EXECUTIVE SUMMARY ---
st.sidebar.divider()
st.sidebar.header("👔 Executive Directives")

for item in sorted_grid:
    ticker = item['Ticker']
    ret = item['Return']
    
    # Simple logic based on your alpha milestones
    if ret > 50:
        directive = "🎯 TARGET HIT: Consider 50% Trim"
    elif ret > 20:
        directive = "✅ STRONG: Hold & Trail"
    elif ret < 5:
        directive = "⏳ LAGGARD: Re-evaluate Entry"
    else:
        directive = "📈 TRENDING: Neutral"
        
    st.sidebar.write(f"**{ticker}**: {directive}")
