# --- STEP 1: INITIALIZATION ---
import streamlit as st # Ensures 'st' is globally defined
import yfinance as yf
import pandas as pd

# --- STEP 2: ALPHA ENGINE ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_price = st.sidebar.number_input("Purchase Price", value=23.0) 

# --- STEP 3: MASTER DATA LOOP ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
titans = ["XOM", "CVX", "GEV"]
all_tickers = portfolio + titans

spy = yf.download("SPY", period="1mo")
spy_perf = ((spy['Close'].iloc[-1] - spy['Close'].iloc[0]) / spy['Close'].iloc[0]) * 100

master_data = []

for t in all_tickers:
    tick = yf.Ticker(t)
    hist = tick.history(period="1mo")
    v_hist = tick.history(period="5d")
    
    if not hist.empty:
        curr = float(hist['Close'].iloc[-1])
        abs_p = ((curr - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
        vol_r = v_hist['Volume'].iloc[-1] / v_hist['Volume'].mean() if not v_hist.empty else 0
        
        # Medal Logic
        gain = (curr - buy_price) / buy_price
        medal = "🥇 " if gain >= 0.50 else "🥉 " if gain >= 0.20 else ""
        
        master_data.append({
            "Ticker": f"{medal}{t}",
            "Alpha %": round(abs_p - spy_perf, 2),
            "Vol Ratio": round(float(vol_r), 2),
            "Abs Return %": round(abs_p, 2),
            "Raw": t # For sorting footer
        })

# --- STEP 4: INTERACTIVE TABLE ---
st.subheader("🏆 Strategic Alpha Leaderboard")
df = pd.DataFrame(master_data).sort_values(by="Alpha %", ascending=False)
st.dataframe(df.drop(columns=["Raw"]), width="stretch", hide_index=True)

# --- STEP 5: RANKED FOOTER (BEST TO LEAST) ---
# Sorting footer by Abs Return
ranked_footer = sorted(master_data, key=lambda x: x['Abs Return %'], reverse=True)
footer_str = " | ".join([f"{item['Raw']}: {item['Abs Return %']}%" for item in ranked_footer])

st.caption(f"📅 **Last Month Performance (Ranked):** {footer_str}")
st.caption(f"⚓ *S&P 500 Benchmark: {round(float(spy_perf), 2)}%*")
