# --- STEP 1: GLOBAL IMPORTS (CRITICAL FOR MOBILE/STABILITY) ---
import streamlit as st  # Fixes 'st' is not defined
import yfinance as yf
import pandas as pd

# --- STEP 2: ALPHA ENGINE INPUTS ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_price = st.sidebar.number_input("Actual Purchase Price", value=23.0) # Your PBR baseline
ticker_input = st.sidebar.text_input("Deep Dive Ticker", value="PBR")

# --- STEP 3: MILESTONE CALCULATOR ---
if buy_price > 0:
    st.header(f"🚀 {ticker_input} Path to Alpha")
    st.success(f"Ultimate Target (1.8x): ${round(buy_price * 1.8, 2)}")
    c1, c2 = st.columns(2)
    c1.warning(f"20% Trim: ${round(buy_price * 1.2, 2)}")
    c2.warning(f"50% Trim: ${round(buy_price * 1.5, 2)}")

# --- STEP 4: PORTFOLIO ALPHA & MEDALS ---
st.subheader("📊 Portfolio Alpha Spread")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
spy = yf.download("SPY", period="1mo")

if not spy.empty:
    spy_prices = spy['Close'].values.flatten()
    spy_perf = ((spy_prices[-1] - spy_prices[0]) / spy_prices[0]) * 100
    st.caption(f"S&P 500 (1mo) Benchmark: {round(spy_perf, 2)}%")
    
    cols = st.columns(len(portfolio))
    for i, ticker in enumerate(portfolio):
        t_data = yf.download(ticker, period="1mo")
        if not t_data.empty:
            t_prices = t_data['Close'].values.flatten()
            curr_price = float(t_prices[-1])
            t_perf = ((curr_price - t_prices[0]) / t_prices[0]) * 100
            alpha = t_perf - spy_perf
            
            # Medal Logic
            gain = (curr_price - buy_price) / buy_price
            medal = "🥇 " if gain >= 0.50 else "🥉 " if gain >= 0.20 else ""
            cols[i].metric(label=f"{medal}{ticker}", value=f"{round(alpha, 2)}%", delta=f"{round(t_perf, 2)}% Abs")

# --- STEP 5: SECTOR LEADERBOARD (TITAN VS. PORTFOLIO) ---
st.subheader("🏆 Sector Alpha Leaderboard")
titans = ["XOM", "CVX", "GEV"]
combined = portfolio + titans
lb_data = []

for t in combined:
    d = yf.download(t, period="1mo")
    if not d.empty:
        p = d['Close'].values.flatten()
        lb_data.append({"Ticker": t, "1mo Return": round(((p[-1] - p[0]) / p[0]) * 100, 2)})

df = pd.DataFrame(lb_data).sort_values(by="1mo Return", ascending=False)
st.dataframe(df, use_container_width=True) # Optimized for Mobile
