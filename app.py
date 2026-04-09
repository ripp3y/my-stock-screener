# --- ADD THIS TO YOUR SIGNAL CALCULATIONS ---
def get_advanced_signals(df, market_df):
    # 1. Volume Accumulation (Is volume > 120% of 20-day average?)
    avg_vol = df['Volume'].rolling(window=20).mean().iloc[-1]
    curr_vol = df['Volume'].iloc[-1]
    acc_signal = curr_vol > (avg_vol * 1.2)
    
    # 2. Relative Strength (Stock vs SPY)
    stock_perf = df['Close'].pct_change(periods=20).iloc[-1]
    mkt_perf = market_df['Close'].pct_change(periods=20).iloc[-1]
    rs_score = stock_perf - mkt_perf # Positive = Outperforming Market
    
    return acc_signal, rs_score

# --- ADD TO YOUR FINANCIALS TAB (TAB 2) ---
# Fetch SPY for comparison
spy_data = yf.download("SPY", period="1y")
acc, rs = get_advanced_signals(df_sel, spy_data)

c1, c2 = st.columns(2)
c1.metric("Relative Strength", f"{rs*100:+.1f}%", delta="OUTPERFORMING" if rs > 0 else "LAGGING")
c2.metric("Accumulation", "ACTIVE" if acc else "QUIET", delta_color="normal" if acc else "off")
