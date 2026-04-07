import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. SETTINGS ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Function to calculate RSI (Relative Strength Index)
def get_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1+rs))

# --- 2. THE ALPHA SCOUT FUNCTION ---
def alpha_scout():
    st.title("🔭 Alpha Scout: The 400% Expansion Team")
    
    # Diversified 2026 Tickers
    # GEV/BW (Power), PBR-A/EQNR/TPL (Energy/Land), SNDK (Storage), MRNA (Biotech)
    team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]
    
    try:
        # Fetch 6 months of data for RSI calculation
        data = yf.download(team_tickers, period="6mo")['Close']
        latest_prices = data.iloc[-1]
        
        # Build Grid Layout
        cols = st.columns(len(team_tickers))
        
        for i, ticker in enumerate(team_tickers):
            price = latest_prices[ticker]
            rsi_val = get_rsi(data[ticker]).iloc[-1]
            
            # Status Logic
            status = "Neutral"
            if rsi_val > 70: status = "⚠️ Overbought"
            elif rsi_val < 30: status = "✅ Oversold"
            
            with cols[i]:
                st.metric(ticker, f"${price:.2f}")
                st.caption(f"RSI: {rsi_val:.1f}")
                st.write(f"**{status}**")

        st.divider()
        st.subheader("📊 Strategic Rotation for Wednesday")
        st.info("""
        * **EQNR Harvest**: Target $41.95+ to lock in $2,045.50.
        * **SNDK Rotation**: Watch the RSI. If SNDK stays below 70, it's the 2026 Momentum play.
        * **MRNA Value**: Currently showing 'Oversold' signals; potential long-term biotech recovery.
        """)
        
    except Exception as e:
        st.error(f"Sync Error: {e}")

# --- 3. EXECUTION ---
if __name__ == "__main__":
    alpha_scout()
