import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

# Simplied CSS to prevent mobile stacking issues
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 26px !important; }
    div.stButton > button { width: 100%; border-radius: 5px; }
    .reportview-container .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

# PBRA removed to fix download errors
team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY", "^VIX"]
    try:
        df = yf.download(syms, period="1y", group_by='ticker')
        return df.ffill()
    except:
        return None

def fetch_insiders(symbol):
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}"
    try:
        r = requests.get(url).json()
        data = r.get('data', [])
        return pd.DataFrame(data) if data else pd.DataFrame()
    except:
        return pd.DataFrame()

# --- 2. DATA ENGINE ---
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
            
            p = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            day_pct = ((p - prev) / prev) * 100
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            
            if not pd.isna(p) and p > 0:
                stats.append({"ticker": t, "price": p, "rs": rs, "daily": day_pct})
        except: continue

    # Leaderboard by Relative Strength
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # Grid Layout: Reliable 2-column display for mobile
    rows = [sorted_stats[i:i + 2] for i in range(0, len(sorted_stats), 2)]
    for row in rows:
        cols = st.columns(2)
        for i, s in enumerate(row):
            with cols[i]:
                # Combined metric for better readability
                st.metric(
                    label=f"{s['ticker']} (RS: {s['rs']*100:+.1f}%)", 
                    value=f"${s['price']:.2f}", 
                    delta=f"{s['daily']:+.2f}%"
                )

    st.divider()

    # --- 3. TARGET DRILL-DOWN ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        df_sel = all_data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], 
                        high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        df_r = all_data[sel].dropna()
        atr = (df_r['High'] - df_r['Low']).rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        # Tooltips added for better understanding of risk metrics
        st.metric("ATR Volatility", f"${atr:.2f}", help="Daily movement 'noise' range.")
        st.metric("Trailing Stop", f"${t_stop:.2f}", 
                  delta=f"${df_r['Close'].iloc[-1]-t_stop:.2f} Buffer",
                  help="Volatility-adjusted floor to protect gains.")

    with t3:
        st.subheader("Insider Form 4 Tracker")
        insider_df = fetch_insiders(sel)
        if not insider_df.empty:
            view_cols = [c for c in ['transactionDate', 'name', 'share', 'change'] if c in insider_df.columns]
            df_display = insider_df[view_cols]
            # FIXED: use_container_width placed correctly
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No recent insider filings.")

else:
    st.error("📡 Sync Issue: Connection lost.")
