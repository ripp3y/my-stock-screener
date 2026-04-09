import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

# This CSS forces metrics to stay horizontal even on mobile screens
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 22px; }
    div[data-testid="column"] { width: 100% !important; flex: 1 1 calc(50% - 10px) !important; min-width: 150px !important; }
    </style>
    """, unsafe_allow_html=True)

FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0, "PBRA": 16.2
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY", "^VIX"]
    try:
        # Fetching data and cleaning up NaNs immediately
        df = yf.download(syms, period="1y", group_by='ticker')
        return df.fillna(method='ffill').dropna(how='all')
    except:
        return None

# --- 2. THE ENGINE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers)

if all_data is not None:
    stats = []
    spy_df = all_data["SPY"]
    
    for t in tickers:
        try:
            df = all_data[t].dropna()
            if df.empty: continue
            
            price = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            day_pct = ((price - prev_close) / prev_close) * 100
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            
            # Only add if the data is valid (not NaN)
            if not pd.isna(price):
                stats.append({"ticker": t, "price": price, "rs": rs, "daily": day_pct})
        except: continue

    # Sorted Leaderboard
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # Grid Layout: 2 items per row on mobile
    rows = [sorted_stats[i:i + 2] for i in range(0, len(sorted_stats), 2)]
    for row in rows:
        cols = st.columns(2)
        for i, s in enumerate(row):
            with cols[i]:
                # The 'label_visibility' helps keep the layout tight
                st.metric(
                    label=s['ticker'], 
                    value=f"${s['price']:.2f}", 
                    delta=f"{s['daily']:+.2f}%"
                )
                st.caption(f"RS: {s['rs']*100:+.1f}%")

    st.divider()

    # --- 3. TARGET FOCUS ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    t1, t2 = st.tabs(["📊 Technicals", "🛡️ Risk Scout"])

    with t1:
        df_sel = all_data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], 
                        high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        df_r = all_data[sel].dropna()
        atr = (df_r['High'] - df_r['Low']).rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        c1, c2 = st.columns(2)
        c1.metric("ATR Volatility", f"${atr:.2f}", help="Daily movement 'noise' range.")
        c2.metric("Trailing Stop", f"${t_stop:.2f}", delta=f"${df_r['Close'].iloc[-1]-t_stop:.2f} Buffer")

else:
    st.error("📡 Sync Issue: Connection lost.")
