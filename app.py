# --- STEP 1: INITIALIZE (MUST BE LINES 1 & 2) ---
import streamlit as st  # Kills the NameError
import yfinance as yf    # Powers your live market data

# --- STEP 2: USER INPUT GATE ---
# Now that 'st' is defined, these sidebar tools will work
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trail_percent = st.sidebar.slider("Trailing Stop %", 5, 20, 9)

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    # 80% Pursuit Logic
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")

    # Profit-Taking Milestones
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

    # --- STEP 4: MARKET RELATIVE STRENGTH ---
    st.subheader("📈 Market Relative Strength")
    # Matches your 17:35:57 live view
    spy = yf.download("SPY", period="1mo")['Close']
    spy_perf = ((spy.iloc[-1] - spy.iloc[0]) / spy.iloc[0]) * 100
    st.metric("S&P 500 (1mo)", f"{round(spy_perf, 2)}%", delta="Benchmark")
