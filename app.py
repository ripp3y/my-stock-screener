import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. CONFIG & REFINED MOBILE CSS ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

st.markdown("""
    <style>
    /* Clean up the metric display for mobile lists */
    [data-testid="stMetricValue"] { font-size: 28px !important; color: #ffffff; }
    [data-testid="stMetricDelta"] { font-size: 18px !important; }
    div[data-testid="column"] { 
        padding: 15px; 
        border-radius: 10px;
        background: #1e1e1e;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

# PBRA removed to eliminate download errors
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

# --- 2. DATA PROCESSING ---
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
            
            if not pd.isna(price) and price > 0:
                stats.append({"ticker": t, "price": price, "rs": rs, "daily": day_pct})
        except: continue

    # Rank by Relative Strength
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # Tactical List Layout
    for s in sorted_stats:
        with st.container():
            c1, c2 = st.columns([2, 1])
            c1.metric(label=f"Ticker: {s['ticker']}", value=f"${s['price']:.2f}")
            c2.metric(label="Day %", value="", delta=f"{s['daily']:+.2f}%")
            st.caption(f"Relative Strength vs S&P: **{s['rs']*100:+.1f}%**")

    st.divider()

    # --- 3. TARGET FOCUS ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    t1, t2, t3 = st.tabs(["📊 Charts", "🛡️ Risk", "🕵️ Insiders"])

    with t1:
        df_sel = all_data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], 
                        high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        df_r = all_data[sel].dropna()
        # ATR Tooltip added here
        atr = (df_r['High'] - df_r['Low']).rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        st.metric("ATR Volatility", f"${atr:.2f}", 
                  help="Average True Range: Measures the daily price 'noise'. Higher values mean more swing.")
        st.metric("Trailing Stop", f"${t_stop:.2f}", 
                  delta=f"${df_r['Close'].iloc[-1]-t_stop:.2f} Buffer",
                  help="Volatility-adjusted exit floor. If price hits this, the trend is considered broken.")

    with t3:
        st.subheader("Insider Tracker")
        insider_df = fetch_insiders(sel)
        if not insider_df.empty:
            # Re-verified bracket safety
            view_cols = [c for c in ['transactionDate', 'name', 'share', 'change'] if c in insider_df.columns]
            st.dataframe(insider_df[view_cols], use_container_width=True)
        else:
            st.info("No recent Form 4 filings.")

else:
    st.error("📡 Connection lost. Check API connectivity.")
