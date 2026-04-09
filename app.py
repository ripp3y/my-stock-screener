import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# --- 1. CONFIG & TEAM ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

target_map = {
    "FIX": 1800.00, "ATRO": 95.00, "CENX": 86.00, 
    "GEV": 1050.00, "BW": 20.33, "TPL": 639.00, 
    "CIEN": 430.00, "STX": 620.00, "PBRA": 16.20,
    "SNDK": 95.00, "MRNA": 115.00, "TIGO": 73.20
}

@st.cache_data(ttl=600)
def fetch_ticker_data(tickers):
    data = yf.download(tickers, period="1y", group_by='ticker')
    infos = {}
    for t in tickers:
        try:
            tick = yf.Ticker(t)
            infos[t] = {
                "info": tick.info,
                "calendar": tick.calendar
            }
        except:
            infos[t] = {"info": {}, "calendar": {}}
    return data, infos

def get_signals(df, target):
    price = df['Close'].iloc[-1]
    ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    risk_score = ((price - target) / target) * 100
    is_up = ema_50.iloc[-1] > ema_50.iloc[-5]
    is_dip = price < ema_9.iloc[-1] and price > ema_50.iloc[-1]
    return price, risk_score, is_up, is_dip

# --- 2. EXECUTION ---
st.title("🚀 Alpha Scout: Institutional Terminal")
team_tickers = list(target_map.keys())

try:
    data, info_data = fetch_ticker_data(team_tickers)
    stats = []
    for t in team_tickers:
        if t in data and not data[t].dropna().empty:
            p, r, up, dip = get_signals(data[t].dropna(), target_map[t])
            stats.append({"ticker": t, "price": p, "risk": r, "up": up, "dip": dip})
    
    sorted_stats = sorted(stats, key=lambda x: x['risk'])

    # LEADERBOARD
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['risk']:+.1f}% Risk", delta_color="normal" if s['risk'] < 0 else "inverse")
            if s['dip'] and s['up']: st.warning("💎 DIP")
            elif s['price'] < target_map[s['ticker']]: st.info("🚀 STRNG")

    st.divider()

    # ANALYSIS
    sel = st.selectbox("Strategic Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3 = st.tabs(["📊 Technicals", "💰 Financials", "📰 News"])

    with tab1:
        df = data[sel].dropna()
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"))
        fig.add_hline(y=target_map[sel], line_dash="dot", line_color="white")
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        inf = info_data[sel].get("info", {})
        cal = info_data[sel].get("calendar", {})
        
        # New Metrics
        inst_own = inf.get('heldPercentInstitutions', 0.0) * 100
        earn_date = "TBD"
        if isinstance(cal, dict) and 'Earnings Date' in cal:
            earn_date = cal['Earnings Date'][0].strftime('%b %d')
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Institutional Own", f"{inst_own:.1f}%")
        c2.metric("Next Earnings", earn_date)
        c3.metric("P/E Ratio", f"{inf.get('trailingPE', 0.0):.1f}x")
        c4.metric("Net Margin", f"{inf.get('profitMargins', 0.0)*100:.1f}%")
        
        st.write(f"**Institutional Insight:** {sel} is {inst_own:.1f}% owned by major funds.")
        st.progress(min(inst_own/100, 1.0))

    with tab3:
        for item in yf.Ticker(sel).news[:3]:
            st.write(f"**{item['title']}**")
            st.write(f"[Link]({item['link']})")
            st.divider()

except Exception as e:
    st.error(f"Sync Issue: {e}")
