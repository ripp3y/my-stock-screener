import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. THE SCOUTING MAP ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Static intel to bypass Yahoo's sync blocks on mobile
team_intel = {
    "FIX": {"target": 1800.00, "own": 96.5, "earn": "2026-05-01"},
    "ATRO": {"target": 95.00, "own": 82.1, "earn": "2026-04-28"},
    "CENX": {"target": 86.00, "own": 61.6, "earn": "2026-04-23"},
    "GEV": {"target": 1050.00, "own": 41.1, "earn": "2026-04-21"},
    "TPL": {"target": 639.00, "own": 58.2, "earn": "2026-05-06"},
    "CIEN": {"target": 430.00, "own": 88.4, "earn": "2026-06-04"},
    "SNDK": {"target": 95.00, "own": 81.7, "earn": "2026-04-30"}
}

@st.cache_data(ttl=3600)
def fetch_scout_data(tickers):
    return yf.download(tickers, period="1y", group_by='ticker')

# --- 2. THE ENGINE ---
st.title("🚀 Alpha Scout: Strategic Terminal")
tickers = list(team_intel.keys())
data = fetch_scout_data(tickers)

if data is not None:
    # Calculations for Leaderboard
    stats = []
    for t in tickers:
        try:
            df = data[t].dropna()
            price = df['Close'].iloc[-1]
            # Days to Earnings
            e_date = datetime.strptime(team_intel[t]['earn'], "%Y-%m-%d")
            days_left = (e_date - datetime.now()).days
            stats.append({"ticker": t, "price": price, "days": days_left, "df": df})
        except: continue

    # LEADERBOARD
    cols = st.columns(len(stats))
    for i, s in enumerate(stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['days']} Days")
            if s['days'] < 7: st.warning("⚠️ EARNINGS ALERT")
            else: st.info("🔍 SCOUTING")

    st.divider()

    # --- 3. SURPRISE ANALYSIS ---
    sel = st.selectbox("Strategic Analysis Selection", [x['ticker'] for x in stats])
    tab1, tab2 = st.tabs(["📊 Technical Floor", "💰 Surprise Scout"])

    with tab1:
        df_sel = data[sel].dropna()
        ema_9 = df_sel['Close'].ewm(span=9, adjust=False).mean()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.add_trace(go.Scatter(x=df_sel.index, y=ema_9, line=dict(color='orange', width=2), name="9-EMA"))
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        intel = team_intel[sel]
        # P/E & Margin Data (Dynamic fetch for selected only to save bandwidth)
        t_info = yf.Ticker(sel).info
        pe = t_info.get('trailingPE', 0.0)
        margin = t_info.get('profitMargins', 0.0) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Institutional Own", f"{intel['own']}%")
        c2.metric("P/E Ratio", f"{pe:.1f}x", delta="EXTREME" if pe > 50 else "NORMAL", delta_color="inverse")
        c3.metric("Profit Margin", f"{margin:.1f}%")

        # SURPRISE ESTIMATE LOGIC
        st.subheader("Surprise Scout Estimate")
        # Logic: If Institutional Own > 70% and Price is near 9-EMA, probability of beat is HIGH
        if intel['own'] > 70 and pe < 50:
            st.success("✅ PROBABILITY: HIGH. Institutions are anchored and valuation is reasonable.")
        elif pe > 100:
            st.error("🚨 RISK: HIGH. Stock is priced for perfection. Any 'Surprise' less than a huge beat could cause a drop.")
        else:
            st.warning("⚖️ PROBABILITY: MODERATE. Watch for 9-EMA support before the report.")

else:
    st.error("Rate limit active. Wait 2 minutes.")
