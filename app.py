import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. SETTINGS & MOBILE CSS ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

# CSS to force performance % (delta) to the right of the price
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 24px !important; display: inline-block; }
    [data-testid="stMetricDelta"] { 
        display: inline-block;
        margin-left: 15px !important;
    }
    div[data-testid="column"] { 
        padding: 12px; 
        border-bottom: 1px solid #333; 
    }
    </style>
    """, unsafe_allow_html=True)

FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

# PBRA removed to clear download errors and 'nan' displays
team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY", "^VIX"]
    try:
        df = yf.download(syms, period="1y", group_by='ticker')
        return df.fillna(method='ffill')
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
            # RS Calculation vs S&P 500
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            
            if not pd.isna(price) and price > 0:
                stats.append({"ticker": t, "price": price, "rs": rs, "daily": day_pct})
        except: continue

    # Sorted Leaderboard by Relative Strength
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # 2-Column Grid for better mobile visibility
    rows = [sorted_stats[i:i + 2] for i in range(0, len(sorted_stats), 2)]
    for row in rows:
        cols = st.columns(2)
        for i, s in enumerate(row):
            with cols[i]:
                st.metric(label=s['ticker'], value=f"${s['price']:.2f}", delta=f"{s['daily']:+.2f}%")
                st.caption(f"RS: {s['rs']*100:+.1f}%")

    st.divider()

    # --- 3. TACTICAL ANALYSIS ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        df_sel = all_data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], 
                        high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        df_r = all_data[sel].dropna()
        # ATR-based Trailing Stop calculation
        atr = (df_r['High'] - df_r['Low']).rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        c1, c2 = st.columns(2)
        c1.metric("ATR Volatility", f"${atr:.2f}")
        c2.metric("Trailing Stop", f"${t_stop:.2f}", delta=f"${df_r['Close'].iloc[-1]-t_stop:.2f} Buffer")

    with t3:
        st.subheader("Insider Form 4 Activity")
        insider_df = fetch_insiders(sel)
        if not insider_df.empty:
            # Fixed unclosed parenthesis/bracket error
            valid_cols = [c for c in ['transactionDate', 'name', 'share', 'change'] if c in insider_df.columns]
            st.dataframe(insider_df[valid_cols], use_container_width=True)
        else:
            st.info("No recent insider data found.")

else:
    st.error("📡 Sync Issue: Connection lost.")
