import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIG & TEAM ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY"]
    try:
        return yf.download(syms, period="1y", group_by='ticker').ffill()
    except:
        return None

# --- CORE ENGINE ---
all_data = fetch_scout_data(list(team_intel.keys()))

if all_data is not None:
    stats = []
    spy_df = all_data["SPY"]
    
    for t in team_intel.keys():
        try:
            df = all_data[t].dropna()
            p = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            # RS Calculation vs S&P 500
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": p, "rs": rs, "daily": ((p-prev)/prev)*100})
        except: continue

    # Ranked Leaderboard
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(2)
    for i, s in enumerate(sorted_stats):
        with cols[i % 2]:
            st.metric(f"{s['ticker']} (RS: {s['rs']*100:+.1f}%)", f"${s['price']:.2f}", f"{s['daily']:+.2f}%")

    st.divider()

    # --- THE RISK SCOUT ENGINE ---
    sel = st.selectbox("Select Target for Analysis", [x['ticker'] for x in sorted_stats])
    
    # Isolate data for selected stock
    df_sel = all_data[sel].dropna()
    
    # ATR Calculation (Volatilty Measurement)
    # Using the standard 14-day True Range method
    high_low = df_sel['High'] - df_sel['Low']
    high_cp = (df_sel['High'] - df_sel['Close'].shift()).abs()
    low_cp = (df_sel['Low'] - df_sel['Close'].shift()).abs()
    tr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().iloc[-1]
    
    # Trailing Stop: Price minus (2.5 * ATR)
    curr_p = df_sel['Close'].iloc[-1]
    t_stop = curr_p - (atr * 2.5)
    buffer = curr_p - t_stop

    # Display Metrics with Help Tooltips
    st.subheader(f"🛡️ Risk Assessment: {sel}")
    st.metric("ATR Volatility", f"${atr:.2f}", 
              help="Average daily price swing. High ATR indicates a volatile 'wild' stock.")
    
    st.metric("Volatility Stop", f"${t_stop:.2f}", 
              delta=f"${buffer:.2f} Buffer",
              help="The logical trend floor. If price breaks this, the trend is likely broken.")

else:
    st.error("📡 Sync Issue: Reconnect to data feed.")
