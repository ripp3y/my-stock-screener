import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_terminal_data(tickers):
    syms = tickers + ["SPY", "QQQ"]
    try:
        return yf.download(syms, period="2y", group_by='ticker').ffill()
    except:
        return None

# --- 2. ENGINE ---
all_data = fetch_terminal_data(list(team_intel.keys()))

if all_data is not None:
    # --- ANALYSIS HUB ---
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3, t4 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🌐 Correlation", "🕵️ Insiders"])

    with t1:
        # FLAT CHART RATIO
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False, 
            height=350, margin=dict(l=5,r=5,t=10,b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # --- ELITE RISK & MOMENTUM SUITE ---
        cp = df_sel['Close'].iloc[-1]
        
        # 1. Z-Score (Mean Reversion)
        ma_20 = df_sel['Close'].rolling(20).mean()
        std_20 = df_sel['Close'].rolling(20).std()
        z_score = (cp - ma_20.iloc[-1]) / (std_20.iloc[-1] + 1e-6)
        
        # 2. VPT: Volume Price Trend
        vpt = (df_sel['Volume'] * (df_sel['Close'].pct_change())).cumsum()
        vpt_trend = "ACCUMULATING" if vpt.iloc[-1] > vpt.iloc[-10] else "DISTRIBUTING"
        
        # 3. Momentum Slope (Relative Speed)
        slope = (df_sel['Close'].pct_change(10).iloc[-1]) * 100
        
        # 4. Standard Risk Metrics
        hi_lo = df_sel['High'] - df_sel['Low']
        tr = pd.concat([hi_lo, (df_sel['High']-df_sel['Close'].shift()).abs()], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Z-Score", f"{z_score:.2f}", help="Standard Deviations from 20D Mean. Above 2.0 is overextended.")
            # NEW TOOLTIP SCALE
            st.metric(
                "10D Momentum", 
                f"{slope:+.2f}%", 
                help=f"Velocity Scale: \n > 5%: High Velocity \n 0-5%: Building \n < 0%: Decelerating"
            )
        with c2:
            st.metric("ATR Volatility", f"${atr:.2f}")
            st.metric("Volatility Stop", f"${t_stop:.2f}", delta=f"${cp - t_stop:.2f} Buffer")

        # Position Sizer
        st.divider()
        acc = st.number_input("Account Size ($)", value=10000)
        risk = st.slider("Risk %", 0.5, 3.0, 1.0)
        shares = int((acc * (risk/100)) / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        
        # BIG BLUE FOOTER
        rf = (atr / cp) * 100
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6;">
                <h3 style="color: white; margin: 0;">{sel}: {vpt_trend}</h3>
                <p style="color: #DBEAFE; margin: 5px 0;">Risk Factor: <b>{rf:.2f}%</b> | Shares: <b>{shares}</b></p>
                <p style="color: #93C5FD; font-size: 14px; margin: 0;">
                    Trend Velocity is <b>{"ACCELERATING" if slope > 0 else "DECELERATING"}</b>. 
                    Price is <b>{z_score:.2f} SD</b> from its mean.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # CORRELATION MATRIX
        st.subheader("🌐 Matrix (20-Day)")
        corr = all_data.xs('Close', axis=1, level=1).pct_change().corr()
        st.dataframe(corr.style.background_gradient(cmap='RdBu_r').format("{:.2f}"))

    with t4:
        # INSIDERS
        try:
            st.dataframe(ticker_obj.insider_transactions.head(10), hide_index=True)
        except:
            st.info("No recent Form 4 data.")
else:
    st.error("📡 Sync Issue.")
