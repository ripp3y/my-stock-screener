# --- STEP 1: INITIALIZE (THIS MUST BE LINES 1 & 2) ---
import streamlit as st  # Kills the 'st' is not defined error
import yfinance as yf    # Powers your market data

# --- STEP 2: USER INPUT GATE ---
# Now 'st' is defined, so these sidebar tools work perfectly
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
ticker_input = st.sidebar.text_input("Ticker for Volume Check", value="PBR")

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")
    
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

# --- STEP 4: INSTITUTIONAL FLOW ---
st.subheader("🏦 Institutional Flow")
if ticker_input:
    data = yf.Ticker(ticker_input).history(period="5d")
    if not data.empty:
        avg_vol = data['Volume'].mean()
        curr_vol = data['Volume'].iloc[-1]
        vol_ratio = curr_vol / avg_vol
        
        # Signals if 'Big Money' is supporting the price
        if vol_ratio > 1.5:
            st.success(f"🔥 VOLUME SURGE: {round(vol_ratio, 2)}x Normal Volume")
        else:
            st.write(f"Volume is normal ({round(vol_ratio, 2)}x avg).")
