import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG & DATA ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_terminal_data(tickers):
    syms = tickers + ["SPY"]
    try:
        return yf.download(syms, period="2y", group_by='ticker').ffill()
    except:
        return None

# --- 2. ENGINE ---
all_data = fetch_terminal_data(list(team_intel.keys()))

if all_data is not None:
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        # ULTRA-FLAT CHART
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False, 
            height=300, margin=dict(l=0, r=0, t=10, b=10),
            yaxis=dict(side="right")
        )
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # --- COMMANDER CORE ---
        cp = df_sel['Close'].iloc[-1]
        
        # Calculations
        ma_20 = df_sel['Close'].rolling(20).mean()
        std_20 = df_sel['Close'].rolling(20).std()
        z_score = (cp - ma_20.iloc[-1]) / (std_20.iloc[-1] + 1e-6)
        slope = (df_sel['Close'].pct_change(10).iloc[-1]) * 100
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # Accumulation Logic
        vpt = (df_sel['Volume'] * (df_sel['Close'].pct_change())).cumsum()
        vpt_trend = "ACCUMULATING" if vpt.iloc[-1] > vpt.iloc[-10] else "DISTRIBUTING"

        # Metric Grid
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Z-Score", f"{z_score:.2f}", help="Standard Deviations from mean. >2.0 is overextended.")
            st.metric("10D Momentum", f"{slope:+.2f}%", help="Velocity Scale: >5% High, 0-5% Building, <0% Decelerating.")
        with c2:
            st.metric("ATR Volatility", f"${atr:.2f}")
            st.metric("Stop Loss", f"${t_stop:.2f}", delta=f"${cp - t_stop:.2f} Buffer")

        # POSITION SIZER
        st.divider()
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 3.0, 1.0, help="Max % of account to lose if Stop is hit.")
        
        # Sizing
        risk_amt = acc * (risk_pct / 100)
        stop_dist = cp - t_stop
        shares = int(risk_amt / stop_dist) if stop_dist > 0 else 0
        
        # --- THE CLEAN BLUE BOX ---
        risk_factor = (atr / cp) * 100
        # Color coding risk status
        if risk_factor < 2.5:
            status_color, status_text = "#4ADE80", "LOW RISK" # Green
        elif risk_factor < 4.5:
            status_color, status_text = "#FBBF24", "HIGH RISK" # Yellow
        else:
            status_color, status_text = "#F87171", "EXTREME RISK" # Red
        
        st.markdown(f"### {sel} Status: {vpt_trend}", help="Accumulating: 'Big Money' is buying the dip/trend. Distributing: Selling pressure is dominant.")
        
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 10px solid {status_color};">
                <p style="color: #DBEAFE; font-size: 20px; margin: 0;">
                    <b>Risk Factor:</b> {risk_factor:.2f}% | <b>Shares:</b> {shares}
                </p>
                <p style="color: {status_color}; font-size: 16px; margin: 5px 0; font-weight: bold;">
                    CONDITION: {status_text}
                </p>
                <p style="color: #93C5FD; font-size: 14px; margin: 0;">
                    Z-Score: {z_score:.2f} | Max Loss: ${risk_amt:.0f}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # INSIDERS
        try:
            st.dataframe(ticker_obj.insider_transactions.head(10), hide_index=True)
        except:
            st.info("No recent Form 4 data.")
else:
    st.error("📡 Sync Issue.")
