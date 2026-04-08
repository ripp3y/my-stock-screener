import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="Alpha Scout: Tactical Terminal", layout="wide")

def get_technical_signals(data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    ema_9 = data['Close'].ewm(span=9, adjust=False).mean()
    current_price = data['Close'].iloc[-1]
    current_ema = ema_9.iloc[-1]
    pct_dist = ((current_price - current_ema) / current_ema) * 100
    is_bottoming = (rsi.iloc[-1] > 30) and (rsi.iloc[-2] <= 30)
    return rsi, ema_9, pct_dist, is_bottoming

# --- 2. LIVE SCOUT ---
st.title("🚀 Alpha Scout: Institutional Command Center")
team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]

try:
    data = yf.download(team_tickers, period="6mo", group_by='ticker')
    cols = st.columns(len(team_tickers))
    
    latest_prices = {}
    for i, ticker in enumerate(team_tickers):
        ticker_df = data[ticker].dropna()
        price = ticker_df['Close'].iloc[-1]
        latest_prices[ticker] = price
        rsi_series, _, pct_dist, bottom_signal = get_technical_signals(ticker_df)
        
        with cols[i]:
            st.metric(ticker, f"${price:.2f}", f"{pct_dist:+.1f}% Floor")
            if bottom_signal: st.success("🎯 BOTTOM FOUND")
            elif pct_dist < 0: st.error("📉 TREND BREAK")
            elif rsi_series.iloc[-1] > 70: st.warning("🔥 BOOMING")
            else: st.info("🚀 STRONG")

    st.divider()

    # --- 3. DIRECTIONAL ANALYSIS & NEWS SCOUT ---
    col_chart, col_news = st.columns([2, 1])
    
    selected_ticker = st.selectbox("Select Ticker for Deep Dive", team_tickers)
    ticker_obj = yf.Ticker(selected_ticker)
    
    with col_chart:
        df = data[selected_ticker].dropna()
        rsi_s, ema_9_s, _, _ = get_technical_signals(df)
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.04, row_heights=[0.5, 0.2, 0.3])

        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ema_9_s, line=dict(color='orange', width=2), name="9-EMA"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=rsi_s, line=dict(color='#A020F0', width=2), name="RSI"), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="lime", row=2, col=1)

        fig.add_annotation(xref="paper", yref="paper", x=0.01, y=0.98, text="<span style='font-size:10px; color:orange;'>ORANGE: 9-DAY EMA FLOOR</span>", showarrow=False)
        fig.add_annotation(xref="paper", yref="paper", x=0.01, y=0.42, text="<span style='font-size:10px; color:#A020F0;'>PURPLE: RSI MOMENTUM</span>", showarrow=False)

        vol_colors = ['#26a69a' if c >= o else '#ef5350' for o, c in zip(df['Open'], df['Close'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vol_colors, name="Volume"), row=3, col=1)
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=800, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_news:
        st.subheader(f"📰 {selected_ticker} News Scout")
        news = ticker_obj.news
        if news:
            for item in news[:5]: # Show top 5 headlines
                st.write(f"**{item['title']}**")
                st.write(f"Source: {item['publisher']} | [Read Story]({item['link']})")
                st.divider()
        else:
            st.write("No recent headlines found.")

    # --- 4. HARVEST CALCULATOR ---
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💰 Harvest Calculator")
        shares = st.number_input("EQNR Shares", value=49)
        val = shares * latest_prices.get('EQNR', 0)
        st.success(f"Wednesday Harvest: ${val:,.2f}")
        st.progress(min(val/2055.55, 1.0))
    with c2:
        st.subheader("🎯 Tactical Strategy")
        st.write("**TPL Entry:** Waiting for '🎯 BOTTOM FOUND' (RSI > 30 crossover).")
        st.write("**EQNR Exit:** Harvesting Wednesday morning to fund the TPL rotation.")

except Exception as e:
    st.error(f"Sync Error: {e}")
