import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & CACHING ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

target_map = {
    "GEV": 863.61, "BW": 20.33, "PBR-A": 16.02, 
    "TPL": 639.00, "SNDK": 95.00, "MRNA": 115.00, 
    "CIEN": 354.01, "TIGO": 73.20, "STX": 582.00
}

@st.cache_data(ttl=600)
def fetch_ticker_data(tickers):
    # Bulk fetch history and info for financial metrics
    data = yf.download(tickers, period="1y", group_by='ticker')
    infos = {t: yf.Ticker(t).info for t in tickers}
    return data, infos

def get_signals(df):
    ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    price = df['Close'].iloc[-1]
    cushion = ((price - ema_9.iloc[-1]) / ema_9.iloc[-1]) * 100
    is_up = ema_50.iloc[-1] > ema_50.iloc[-5]
    is_dip = price < ema_9.iloc[-1] and price > ema_50.iloc[-1]
    return cushion, is_up, is_dip

# --- 2. DATA LOAD ---
st.title("🚀 Alpha Scout: Strategic Terminal")
team_tickers = list(target_map.keys())

try:
    data, info_data = fetch_ticker_data(team_tickers)
    
    # Leaderboard Logic
    stats = []
    for t in team_tickers:
        t_df = data[t].dropna()
        cush, up, dip = get_signals(t_df)
        stats.append({"ticker": t, "cushion": cush, "up": up, "dip": dip, "price": t_df['Close'].iloc[-1]})
    
    # Sort by Cushion (Highest to Left)
    sorted_stats = sorted(stats, key=lambda x: x['cushion'], reverse=True)

    # 3. KPI HEADER (Professional Layout)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(s['ticker'], f"${s['price']:.2f}", f"{s['cushion']:+.1f}%")
            if s['dip'] and s['up']: st.warning("💎 VALUE DIP")
            elif s['cushion'] < 0: st.error("📉 BREAK")
            else: st.info("🚀 STRONG")

    st.divider()

    # 4. DEEP DIVE TABS
    selected_ticker = st.selectbox("Strategic Analysis Selection", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3 = st.tabs(["📊 Technical Chart", "💰 Financial Intel", "📰 News Feed"])

    with tab1:
        # --- Chart Logic (Candles + Targets) ---
        df = data[selected_ticker].dropna()
        ema_9_s = df['Close'].ewm(span=9, adjust=False).mean()
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ema_9_s, line=dict(color='orange', width=2), name="9-EMA"), row=1, col=1)
        
        # Target Line
        t_price = target_map.get(selected_ticker)
        fig.add_hline(y=t_price, line_dash="dot", line_color="white", row=1, col=1)
        
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # --- Inside your Financial Intel Tab ---
with tab2:
    info = info_data.get(selected_ticker, {})
    pe = info.get('trailingPE', 0.0)
    
    # Value Logic: Is it cheap or expensive?
    pe_color = "normal"
    if pe > 60: pe_color = "inverse" # High P/E (Red/Warning)
    elif pe < 25: pe_color = "normal" # Low P/E (Green/Value)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("EPS (TTM)", f"${info.get('trailingEps', 0.0):.2f}")
    c2.metric("P/E Ratio", f"{pe:.1f}x", delta="EXTREME" if pe > 60 else None, delta_color=pe_color)
    c3.metric("Profit Margin", f"{info.get('profitMargins', 0.0)*100:.1f}%")
    c4.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B")

    with tab3:
        # --- News Scout ---
        news = yf.Ticker(selected_ticker).news
        for item in news[:5]:
            st.write(f"**{item['title']}** ({item['publisher']})")
            st.write(f"[Read Article]({item['link']})")
            st.divider()

except Exception as e:
    st.error(f"Sync Issue: {e}")
