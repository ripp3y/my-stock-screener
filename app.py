import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. SETTINGS & DATA ---
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

# --- 2. THE ENGINE ---
all_data = fetch_terminal_data(list(team_intel.keys()))

if all_data is not None:
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Intel"])

    with t1:
        # ULTRA-FLAT CHART
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False, 
            height=300, margin=dict(l=0, r=0, t=10, b=10), yaxis=dict(side="right")
        )
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # --- RISK SCOUT (15% Max Risk) ---
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 15.0, 3.0)
        
        risk_amt = acc * (risk_pct / 100)
        shares = int(risk_amt / (cp - t_stop)) if (cp - t_
