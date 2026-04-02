import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- 1. DATA ENGINE ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
raw_data = yf.download(portfolio, period="2mo")['Close']
returns_df = raw_data.pct_change().dropna()

# --- 2. DIVERSIFICATION SCORE CALCULATION ---
if not returns_df.empty:
    corr_matrix = returns_df.corr()
    # Average of the upper triangle of the matrix (excluding 1.0 diagonals)
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    avg_corr = upper_tri.stack().mean()
    
    # Score: 1 minus average correlation
    div_score = round((1 - avg_corr) * 100, 1)
    
    # Visual Status
    status = "Strong" if div_score > 70 else "Moderate" if div_score > 40 else "Concentrated"
    
    st.subheader("🛡️ Portfolio Alpha Guardian")
    st.metric(label="Diversification Score", value=f"{div_score}%", help="Higher is better. 100% means total independence.")
    st.caption(f"**Current Status:** {status} (Avg Correlation: {round(avg_corr, 2)})")

# --- 3. CORRELATION MATRIX ---
st.subheader("🔗 Portfolio Correlation Matrix")
st.dataframe(corr_matrix.round(2), use_container_width=True)

# --- 4. MOMENTUM GRID & FOOTER (STABLE) ---
# ... [Keeping previous ranked sorting logic] ...
