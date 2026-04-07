import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. SETTINGS ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# --- 2. THE ALPHA SCOUT FUNCTION ---
def alpha_scout():
    st.title("🚀 Alpha Scout: 400% Club Hunter")
    
    # 4-SPACE INDENTATION: REQUIRED FOR DEPLOYMENT
    # Note: Use 'PBR-A' for Petrobras Preferred to avoid sync errors
    power_tickers = ["GEV", "BW", "PBR-A", "EQNR"]
    
    try:
        # Pulling live data for April 6, 2026
        p_data = yf.download(power_tickers, period="5d")['Close'].iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        # --- POWER WALL METRICS ---
        # GEV: $150B Backlog | 2026 Revenue Target: $44B-$45B
        col1.metric("GEV", f"${p_data['GEV']:.2f}", "Backlog: $150B")
        
        # BW: $2.8B Backlog (Up 470%) | $12B+ Pipeline
        col2.metric("BW", f"${p_data['BW']:.2f}", "Backlog: $2.8B")
        
        # PBR-A: Dividend Yield ~7.1% - 10% 
        col3.metric("PBR-A", f"${p_data['PBR-A']:.2f}", "Yield: ~7.2%")
        
        # EQNR: Buy-back program active until March 30, 2026
        col4.metric("EQNR", f"${p_data['EQNR']:.2f}", "Sell: Wed")
        
        st.divider()
        st.info("💡 Pro Tip: BW's $12B project pipeline is currently ~5.7x its Market Cap.")
        
    except Exception as e:
        st.error(f"Sync Error: {e}")

# --- 3. EXECUTION ---
if __name__ == "__main__":
    alpha_scout()
