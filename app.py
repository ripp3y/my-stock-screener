# Create two columns for the metrics row
col1, col2 = st.columns(2)

# Column 1: Forward PE (already working!)
f_pe = round(info.get('forwardPE', 0), 1)
col1.metric("Forward PE", f"{f_pe}")

# Column 2: Dividend Yield (New)
# yfinance provides this as a decimal (e.g., 0.035), so we multiply by 100
div_yield = info.get('dividendYield', 0)
if div_yield:
    formatted_yield = f"{round(div_yield * 100, 2)}%"
else:
    formatted_yield = "0.0%"

col2.metric("Div Yield", formatted_yield)
