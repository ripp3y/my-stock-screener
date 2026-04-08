import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & CACHING ---
st.set_page_config(page_title="Alpha Scout: Strategic Terminal", layout="wide")

# Static Analyst Targets for your Team
target_map = {
    "GEV": 863.61, "BW": 20.33, "PBR-A": 16.02, 
    "EQNR": 29.50, "TPL": 639.00, "SNDK": 95.00, 
    "MRNA": 115.00, "CIEN": 354.01, "TIGO": 73.20, "STX": 582.00
}

@st.cache_data(ttl=600) # Only talks to Yahoo every 10 mins to avoid blocks
def fetch_ticker_data(tickers):
    return yf.download(tickers, period="6mo", group_by='ticker')

def get_technical_signals(df):
    # RSI Momentum
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # 9-Day EMA (The "Boom Floor") and 50-Day EMA (Trend Health)
    ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    
    current_price = df['Close'].iloc[-1]
    
    # Logic for Upward Channels & Dips
    is_upward_trend = ema_50.iloc[-1] > ema_50.iloc[-5] 
    is_dipping = current_price < ema_9.iloc[-1] and current_price > ema_50.iloc[-1]
    cushion = ((current_price - ema_9.iloc[-1]) / ema_9.iloc[-1]) * 100
    bottom_signal = (rsi.iloc[-1] > 30) and (rsi.iloc[-2] <= 30)
    
    return rsi, ema_9, cushion, bottom_signal, is_upward_trend, is_dipping

# --- 2. LIVE SCOUT & LEADERBOARD ---
st.title("🚀 Alpha Scout: Tactical Command Center")
team_tickers = list(target_map.keys())

try:
    data = fetch_ticker_data(team_tickers)
    
    # Calculate stats for the leaderboard
    ticker_stats = []
    for ticker in team_tickers:
        t_df = data[ticker].dropna()
        rsi_s, _, cushion, bottom, is_up, is_dip = get_technical_signals(t_df)
        ticker_stats.append({
            "ticker": ticker, "price": t_df['Close'].iloc[-1], "cushion": cushion,
            "rsi": rsi_s.iloc[-1], "bottom": bottom, "is_up": is_up, "is_dip": is_dip
        })

    # AUTO-POPULATE: Sort by Cushion (Highest at the top/left)
    sorted_stats = sorted(ticker_stats, key=lambda x: x['cushion'], reverse=True)

    cols = st.columns(len(sorted_stats))
    for i, stat in enumerate(sorted_stats):
        with cols[i]:
            st.metric(stat['ticker'], f"${stat['price']:.2f}", f"{stat['cushion']:+.1f}% Floor")
            if stat['bottom']: st.success("🎯 BOTTOM FOUND")
            elif stat['is_dip'] and stat['is_up']: st.warning("💎 VALUE DIP")
            elif stat['cushion'] < 0: st.error("📉 TREND BREAK")
            elif stat['rsi'] > 70: st.warning("🔥 BOOMING")
            else: st.info("🚀 STRONG")

    st.divider()

    # --- 3. DIRECTIONAL ANALYSIS & NEWS ---
    col_chart, col_news = st.columns([2, 1])
    
    selected_ticker = st.selectbox("Select Ticker for Deep Dive", team_tickers)
    
    with col_chart:
        df = data[selected_ticker].dropna()
        rsi_s, ema_9_s, _, _, _, _ = get_technical_signals(df)
        
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.04, row_heights=[0.5, 0.2, 0.3])

        # Candlesticks & Floor
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ema_9_s, line=dict(color='orange', width=2), name="9-EMA"), row=1, col=1)

        # Analyst Target Line (White Dot)
        t_price = target_map.get(selected_ticker)
        fig.add_hline(y=t_price, line_dash="dot", line_color="white", row=1, col=1)
        fig.add_annotation(xref="paper", yref="y", x=0.98, y=t_price, text=f"TARGET: ${t_price}", showarrow=False, font=dict(size=10, color="white"), row=1, col=1)

        # RSI & Momentum Labels
        fig.add_trace(go.Scatter(x=df.index, y=rsi_s, line=dict(color='#A020F0', width=2), name="RSI"), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="lime", row=2, col=1)
        fig.add_annotation(xref="paper", yref="paper", x=0.01, y=0.98, text="<span style='font-size:10px; color:orange;'>ORANGE: 9-DAY EMA FLOOR</span>", showarrow=False)
        fig.add_annotation(xref="paper", yref="paper", x=0.01, y=0.42, text="<span style='font-size:10px; color:#A020F0;'>PURPLE: RSI MOMENTUM</span>", showarrow=False)

        # Volume
        vol_colors = ['#26a69a' if c >= o else '#ef5350' for o, c in zip(df['Open'], df['Close'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vol_colors, name="Volume"), row=3, col=1)
        
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=800, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_news:
        st.subheader(f"📰 {selected_ticker} News")
        news = yf.Ticker(selected_ticker).news
        if news:
            for item in news[:4]:
                st.write(f"**{item['title']}**")
                st.write(f"Source: {item['publisher']} | [Read]({item['link']})")
                st.divider()

except Exception as e:
    st.error(f"Sync Error: {e}. Try refreshing in 10 minutes.")
