import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & UPDATED PORTFOLIO ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Updated targets with your new BrokerageLink positions
target_map = {
    "FIX": 1800.00, "ATRO": 95.00, "CENX": 86.00, 
    "GEV": 1050.00, "BW": 20.33, "TPL": 639.00, 
    "CIEN": 430.00, "STX": 620.00, "PBRA": 16.20,
    "SNDK": 95.00, "MRNA": 115.00, "TIGO": 73.20
}

@st.cache_data(ttl=600)
def fetch_ticker_data(tickers):
    # Fetching history and info separately to avoid rate limit sync issues
    data = yf.download(tickers, period="1y", group_by='ticker')
    infos = {}
    for t in tickers:
        try:
            infos[t] = yf.Ticker(t).info
        except:
            infos[t] = {}
    return data, infos

def get_signals(df, target):
    price = df['Close'].iloc[-1]
    ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    
    cushion = ((price - ema_9.iloc[-1]) / ema_9.iloc[-1]) * 100
    is_up = ema_50.iloc[-1] > ema_50.iloc[-5]
    is_dip = price < ema_9.iloc[-1] and price > ema_50.iloc[-1]
    risk_score = ((price - target) / target) * 100
    return cushion, is_up, is_dip, risk_score

# --- 2. DATA EXECUTION ---
st.title("🚀 Alpha Scout: Strategic Command")
team_tickers = list(target_map.keys())

try:
    data, info_data = fetch_ticker_data(team_tickers)
    stats = []
    for t in team_tickers:
        if t in data and not data[t].dropna().empty:
            t_df = data[t].dropna()
            cush, up, dip, risk = get_signals(t_df, target_map[t])
            stats.append({
                "ticker": t, "cushion": cush, "up": up, 
                "dip": dip, "price": t_df['Close'].iloc[-1], "risk": risk
            })
    
    # Sort Leaderboard by Risk (Most room to run first)
    sorted_stats = sorted(stats, key=lambda x: x['risk'])

    # --- 3. MOBILE LEADERBOARD ---
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            risk_color = "normal" if s['risk'] < 0 else "inverse"
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['risk']:+.1f}%", delta_color=risk_color)
            if s['dip'] and s['up']: st.warning("💎 DIP")
            elif s['cushion'] < 0: st.error("📉 BREAK")
            else: st.info("🚀 STRNG")

    st.divider()

    # --- 4. TACTICAL ANALYSIS ---
    selected_ticker = st.selectbox("Strategic Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3 = st.tabs(["📊 Technicals", "💰 Financials", "📰 News"])

    with tab1:
        df = data[selected_ticker].dropna()
        ema_9_s = df['Close'].ewm(span=9, adjust=False).mean()
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ema_9_s, line=dict(color='orange', width=2), name="9-EMA"), row=1, col=1)
        t_price = target_map.get(selected_ticker)
        fig.add_hline(y=t_price, line_dash="dot", line_color="white", row=1, col=1)
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        info = info_data.get(selected_ticker, {})
        pe = info.get('trailingPE', 0.0)
        c1, c2, c3 = st.columns(3)
        c1.metric("EPS", f"${info.get('trailingEps', 0.0):.2f}")
        c2.metric("P/E Ratio", f"{pe:.1f}x")
        c3.metric("Margin", f"{info.get('profitMargins', 0.0)*100:.1f}%")
        st.write(f"**Overview:** {info.get('longBusinessSummary', 'N/A')[:500]}...")

    with tab3:
        news = yf.Ticker(selected_ticker).news
        for item in news[:3]:
            st.write(f"**{item['title']}** ({item['publisher']})")
            st.write(f"[Read Article]({item['link']})")
            st.divider()

except Exception as e:
    st.error(f"Sync Issue: {e}. Try refreshing in 1 minute.")
