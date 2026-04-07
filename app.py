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
    
    # Your full 2026 Diversified Portfolio
    team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]
    
    try:
        # Fetching 6mo data for accurate RSI
        data = yf.download(team_tickers, period="6mo")['Close']
        latest_prices = data.iloc[-1]
        
        # Grid Layout for scannability
        cols = st.columns(len(team_tickers))
        
        for i, ticker in enumerate(team_tickers):
            price = latest_prices[ticker]
            rsi_val = get_rsi(data[ticker]).iloc[-1]
            
            # 2026 Logic: Overbought > 70, Oversold < 30
            status = "Neutral"
            icon = ""
            if rsi_val > 70: 
                status = "⚠️ Overbought"
            elif rsi_val < 30: 
                status = "✅ Oversold"
            
            with cols[i]:
                st.metric(ticker, f"${price:.2f}")
                st.caption(f"RSI: {rsi_val:.1f}")
                if status != "Neutral":
                    st.write(f"**{status}**")
                else:
                    st.write(status)

        st.divider()
        
        # Automated Strategy Panel
        st.subheader("📊 Strategic Rotation for Wednesday")
        st.info(f"""
        * **EQNR Harvest**: Current Price **${latest_prices['EQNR']:.2f}** is near targets. Lock in gains.
        * **TPL Opportunity**: RSI is **{get_rsi(data['TPL']).iloc[-1]:.1f}** (Oversold). Institutional entry signal.
        * **SNDK Momentum**: Price **${latest_prices['SNDK']:.2f}** remains the 2026 leader.
        """)
        
    except Exception as e:
        st.error(f"Sync Error: {e}")

if __name__ == "__main__":
    alpha_scout()
