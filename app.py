import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. SETTINGS ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# --- 2. THE ALPHA SCOUT FUNCTION ---
def alpha_scout():
    st.title("🚀 Alpha Scout: 100% Club Hunter")
    
    # EXACT 4-SPACE INDENTATION
    power_tickers = ["GEV", "BW", "PBR-A", "EQNR"]
    
    try:
        # Pulling live data for April 6, 2026
        p_data = yf.download(power_tickers, period="5d")['Close'].iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Displaying the "Power Wall"
        col1.metric("GEV", f"${p_data['GEV']:.2f}", "Target: $1,735")
        col2.metric("BW", f"${p_data['BW']:.2f}", "Target: $25.00")
        col3.metric("PBR-A", f"${p_data['PBR-A']:.2f}", "Div: Apr 24")
        col4.metric("EQNR", f"${p_data['EQNR']:.2f}", "Sell: Wed")
        
    except Exception as e:
        st.error(f"Sync Error: {e}")

# --- 3. EXECUTION ---
if __name__ == "__main__":
    alpha_scout()
