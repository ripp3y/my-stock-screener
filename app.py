# --- STEP 1: INITIALIZE (MUST BE TOP LINES) ---
import streamlit as st  # Powers the dashboard
import yfinance as yf    # Powers the live data

# --- STEP 2: USER INPUT GATE ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trail_percent = st.sidebar.slider("Trailing Stop %", 5, 20, 9)

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")

    # Profit Milestones
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

    # --- STEP 4: MARKET RELATIVE STRENGTH ---
    st.subheader("📈 Market Relative Strength")
    spy_data = yf.download("SPY", period="1mo")['Close']
    
    # Calculation Logic
    spy_perf = ((spy_data.iloc[-1] - spy_data.iloc[0]) / spy_data.iloc[0]) * 100
    
    # THE FIX: Ensuring spy_perf is a single float, not a Series
    clean_val = float(spy_perf.iloc[0]) if hasattr(spy_perf, 'iloc') else float(spy_perf)
    
    st.metric("S&P 500 (1mo)", f"{round(clean_val, 2)}%", delta="Benchmark")
