import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. SETTINGS ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Technical Logic: RSI & Volume Spikes
def get_technical_signals(data):
    # RSI Calculation
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1+rs))
    
    # Volume Spike Detection
    avg_vol = data['Volume'].rolling(window=20).mean()
    vol_spike = data['Volume'] > (avg_vol * 1.5)
    
    return rsi.iloc[-1], vol_spike.iloc[-1]

# --- 2. THE ALPHA SCOUT FUNCTION ---
def alpha_scout():
    st.title("🔭 Alpha Scout: Institutional Volume Tracker")
    
    # The 2026 Team
    team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]
    
    try:
        # Fetching 6mo data for Volume & RSI
        data = yf.download(team_tickers, period="6mo", group_by='ticker')
        
        cols = st.columns(len(team_tickers))
        
        for i, ticker in enumerate(team_tickers):
            ticker_data = data[ticker]
            price = ticker_data['Close'].iloc[-1]
            rsi, spike = get_technical_signals(ticker_data)
            
            with cols[i]:
                st.metric(ticker, f"${price:.2f}")
                
                # Signal 1: RSI Status
                if rsi > 70: st.error(f"RSI: {rsi:.1f} (Overbought)")
                elif rsi < 30: st.success(f"RSI: {rsi:.1f} (Oversold)")
                else: st.caption(f"RSI: {rsi:.1f}")
                
                # Signal 2: Institutional Volume Spike
                if spike:
                    st.warning("🔥 VOLUME SPIKE")
                    st.write("Institutional Buying Detected")
                else:
                    st.write("Normal Volume")

        st.divider()
        st.subheader("📝 Monday Night Strategy")
        st.info("Watch for 'Oversold' RSI + 'Volume Spike' on the same day. That is the 400% moonshot entry signal.")
        
    except Exception as e:
        st.error(f"Sync Error: {e}")

if __name__ == "__main__":
    alpha_scout()
