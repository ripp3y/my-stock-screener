import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- 1. CONFIG & RECOVERY DATA ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

team_intel = {
    "FIX": {"target": 1800.0, "own": 96.5, "earn": "2026-05-01"},
    "ATRO": {"target": 95.0, "own": 82.1, "earn": "2026-04-28"},
    "CENX": {"target": 86.0, "own": 61.6, "earn": "2026-04-23"},
    "GEV": {"target": 1050.0, "own": 41.1, "earn": "2026-04-21"},
    "TPL": {"target": 639.0, "own": 58.2, "earn": "2026-05-06"},
    "CIEN": {"target": 430.0, "own": 88.4, "earn": "2026-06-04"},
    "STX": {"target": 620.0, "own": 79.5, "earn": "2026-04-16"},
    "PBRA": {"target": 16.2, "own": 25.4, "earn": "2026-05-14"}
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    all_syms = tickers + ["SPY"]
    try:
        return yf.download(all_syms, period="1y", interval="1d", group_by='ticker')
    except: return None

# --- 2. ENGINE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
data = fetch_scout_data(tickers)

if data is not None:
    stats = []
    spy_df = data["SPY"].dropna()
    for t in tickers:
        try:
            df = data[t].dropna()
            price = df['Close'].iloc[-1]
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            days = (datetime.strptime(team_intel[t]['earn'], "%Y-%m-%d") - datetime.now()).days
            stats.append({"ticker": t, "price": price, "rs": rs, "days": days})
        except: continue

    # LEADERBOARD
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['rs']*100:+.1f}% RS")

    st.divider()

    # --- 3. TACTICAL ANALYSIS ---
    sel = st.selectbox("Strategic Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🔗 Correlation", "💰 Institutional"])

    with tab1:
        df_sel = data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(f"Volatility Protection for {sel}")
        df_r = data[sel].dropna()
        # Calculate ATR (14-day)
        high_low = df_r['High'] - df_r['Low']
        high_cp = (df_r['High'] - df_r['Close'].shift()).abs()
        low_cp = (df_r['Low'] - df_r['Close'].shift()).abs()
        atr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1).rolling(14).mean().iloc[-1]
        
        curr_p = df_r['Close'].iloc[-1]
        t_stop = curr_p - (atr * 2.5) # 2.5x ATR is the pro standard
        
        c1, c2 = st.columns(2)
        c1.metric("ATR Volatility", f"${atr:.2f}")
        c2.metric("Trailing Stop", f"${t_stop:.2f}", delta=f"${curr_p - t_stop:.2f} Buffer")
        
        if curr_p < t_stop: st.error("🚨 EXIT ALERT: Price has breached the volatility floor.")
        else: st.success("✅ STATUS: Trend is stable. Holding above volatility floor.")

    with tab3:
        st.subheader("Portfolio Correlation Matrix")
        # Build correlation table
        corr_df = pd.DataFrame()
        for t in tickers:
            corr_df[t] = data[t]['Close'].pct_change()
        
        matrix = corr_df.corr()
        fig_corr = px.imshow(matrix, text_auto=True, color_continuous_scale='RdBu_r', aspect="auto")
        fig_corr.update_layout(template="plotly_dark")
        st.plotly_chart(fig_corr, use_container_width=True)
        st.info("💡 High Correlation (>0.7): Stocks move together. Low Correlation (<0.3): Good Diversification.")

    with tab4:
        intel = team_intel[sel]
        st.metric("Institutional Ownership", f"{intel['own']}%")
        st.progress(min(intel['own']/100, 1.0))

else:
    st.error("Rate limit active. Refresh in 2m.")
