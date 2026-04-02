# --- STEP 1: GLOBAL IMPORTS (MANDATORY TOP POSITION) ---
import streamlit as st  # Fixes recurring NameErrors
import yfinance as yf
import pandas as pd

# --- STEP 2: ALPHA ENGINE & MILESTONES ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_price = st.sidebar.number_input("Purchase Price", value=23.0)
ticker_input = st.sidebar.text_input("Deep Dive Ticker", value="PBR")

if buy_price > 0:
    st.header(f"🚀 {ticker_input} Path to Alpha")
    st.success(f"Ultimate Target (1.8x): ${round(buy_price * 1.8, 2)}")
    c1, c2 = st.columns(2)
    c1.warning(f"20% Trim: ${round(buy_price * 1.2, 2)}")
    c2.warning(f"50% Trim: ${round(buy_price * 1.5, 2)}")

# --- STEP 3: THE PORTFOLIO & TITANS ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
titans = ["XOM", "CVX", "GEV"]
all_tickers = portfolio + titans

# --- STEP 4: INSTITUTIONAL FLOW VS. TITANS ---
st.subheader("🏦 Smart Money Flow (Volume Ratio)")
flow_data = []

for t in all_tickers:
    hist = yf.Ticker(t).history(period="5d")
    if not hist.empty:
        # Ratio of current volume vs 5-day average
        ratio = hist['Volume'].iloc[-1] / hist['Volume'].mean()
        flow_data.append({"Ticker": t, "Vol Ratio": round(float(ratio), 2)})

df_flow = pd.DataFrame(flow_data).sort_values(by="Vol Ratio", ascending=False)
st.dataframe(df_flow, width="stretch") # Responsive for Mobile/Chromebook

# --- STEP 5: PORTFOLIO ALPHA & MEDALS ---
st.subheader("📊 Portfolio Alpha Spread")
spy = yf.download("SPY", period="1mo")
if not spy.empty:
    spy_p = spy['Close'].values.flatten()
    spy_perf = ((spy_p[-1] - spy_p[0]) / spy_p[0]) * 100
    
    cols = st.columns(len(portfolio))
    for i, t in enumerate(portfolio):
        d = yf.download(t, period="1mo")
        if not d.empty:
            p = d['Close'].values.flatten()
            curr = float(p[-1])
            t_perf = ((curr - p[0]) / p[0]) * 100
            
            # Medal Logic
            gain = (curr - buy_price) / buy_price
            medal = "🥇 " if gain >= 0.50 else "🥉 " if gain >= 0.20 else ""
            cols[i].metric(label=f"{medal}{t}", value=f"{round(t_perf - spy_perf, 2)}%", delta=f"{round(t_perf, 2)}% Abs")
