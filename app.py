# --- STEP 1: GLOBAL IMPORTS (TOP OF FILE) ---
import streamlit as st  # Fixes recurring NameErrors
import yfinance as yf
import pandas as pd

# --- STEP 2: ALPHA ENGINE & MILESTONES ---
st.sidebar.header("🎯 Target Alpha Engine")
buy_price = st.sidebar.number_input("Purchase Price", value=23.0) # Your PBR baseline

# --- STEP 3: MASTER DATA AGGREGATION ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
titans = ["XOM", "CVX", "GEV"]
all_tickers = portfolio + titans

spy = yf.download("SPY", period="1mo")
spy_p = spy['Close'].values.flatten()
spy_perf = ((spy_p[-1] - spy_p[0]) / spy_p[0]) * 100

master_list = []

for t in all_tickers:
    # Fetch 1-month data for Alpha and 5-day for Volume
    tick = yf.Ticker(t)
    hist_mo = tick.history(period="1mo")
    hist_5d = tick.history(period="5d")
    
    if not hist_mo.empty and not hist_5d.empty:
        # Calculate Alpha Spread
        p_mo = hist_mo['Close'].values.flatten()
        abs_perf = ((p_mo[-1] - p_mo[0]) / p_mo[0]) * 100
        alpha = abs_perf - spy_perf
        
        # Calculate Volume Ratio
        vol_ratio = hist_5d['Volume'].iloc[-1] / hist_5d['Volume'].mean()
        
        # Determine Medal Status
        gain = (float(p_mo[-1]) - buy_price) / buy_price
        medal = "🥇 " if gain >= 0.50 else "🥉 " if gain >= 0.20 else ""
        
        master_list.append({
            "Ticker": f"{medal}{t}",
            "Alpha %": round(alpha, 2),
            "Vol Ratio": round(float(vol_ratio), 2),
            "Abs Return %": round(abs_perf, 2)
        })

# --- STEP 4: INTERACTIVE SORTABLE DASHBOARD ---
st.subheader("🏆 Strategic Alpha Leaderboard")
df_master = pd.DataFrame(master_list)

# Default sort by Alpha % (Descending) as requested
df_sorted = df_master.sort_values(by="Alpha %", ascending=False)

# Render as an interactive table with clickable headers
st.dataframe(
    df_sorted, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "Alpha %": st.column_config.NumberColumn(format="%.2f%%"),
        "Abs Return %": st.column_config.NumberColumn(format="%.2f%%"),
        "Vol Ratio": st.column_config.ProgressColumn(min_value=0, max_value=2)
    }
)
