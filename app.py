import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- STEP 1: DATA HARVESTING ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
price_data = {}

for t in portfolio:
    # Fetching 2 months to ensure we have a solid 30 days of change data
    df = yf.download(t, period="2mo")
    if not df.empty:
        # We use daily percentage change for correlation, not raw price
        price_data[t] = df['Close'].pct_change()

# Create a single Master DataFrame of returns
returns_df = pd.DataFrame(price_data).dropna()

# --- STEP 2: CORRELATION CALCULATION ---
# The .corr() method uses Pearson correlation by default (-1 to +1)
corr_matrix = returns_df.corr().round(2)

# --- STEP 3: VISUAL MATRIX ---
st.subheader("🔗 Portfolio Correlation Matrix")
st.write("Checking how closely your picks move together (1.0 = Identical).")

# Using Pandas Styling to create a "Heatmap" without extra libraries
st.dataframe(
    corr_matrix.style.background_gradient(cmap='RdYlGn', vmin=-1, vmax=1),
    use_container_width=True
)

# --- STEP 4: DIVERSIFICATION INTEL ---
# Identify the highest and lowest correlations for quick insight
st.info("💡 **Diversification Tip:** Look for values below **0.3** to find true 'Zigs' when the market 'Zags'.")

# --- STEP 5: THE UPDATED RANKED FOOTER ---
# (Keeping your existing logic stable)
st.caption("📅 **Last Month Performance:** Sorted by Alpha Rank")
