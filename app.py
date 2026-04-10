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
    # Target Selector
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    # 3-Tab System
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        # --- THE FLAT CHART (Height set to 300 for maximum flattening) ---
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_rangeslider_visible=False, 
            height=300, # Ultra-flat ratio
            margin=dict(l=0, r=0, t=10, b=10), # Zero side margins
            yaxis=dict(side="right") # Price on right for better visibility
        )
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # --- RISK & MOMENTUM COMMAND ---
        cp = df_sel['Close'].iloc[-1]
        
        # Calculations
        ma_20 = df_sel['Close'].rolling(20).mean()
        std_20 = df_sel['Close'].rolling(20).std()
        z_score = (cp - ma_20.iloc[-1]) / (std_20.iloc[-1] + 1e-6)
        slope = (df_sel['Close'].pct_change(10).iloc[-1]) * 100
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # VPT Accumulation Logic
        vpt = (df_sel['Volume'] * (df_sel['Close'].pct_change())).cumsum()
        vpt_trend = "ACCUMULATING" if vpt.iloc[-1] > vpt.iloc[-10] else "DISTRIBUTING"

        # Metric Grid
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Z-Score", f"{z_score:.2f}")
            st.metric("10D Momentum", f"{slope:+.2f}%")
        with c2:
            st.metric("ATR Volatiltiy", f"${atr:.2f}")
            st.metric("Stop Loss", f"${t_stop:.2f}")

        # Position Sizing
        st.divider()
        acc = st.number_input("Account Size ($)", value=10000)
        risk = st.slider("Risk Per Trade %", 0.5, 3.0, 1.0)
        shares = int((acc * (risk/100)) / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        
        # THE BIG BLUE FOOTER
        rf = (atr / cp) * 100
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6;">
                <h3 style="color: white; margin: 0;">{sel} Status: {vpt_trend}</h3>
                <p style="color: #DBEAFE; margin: 5px 0;">Risk Factor: <b>{rf:.2f}%</b> | Max: <b>{shares} shares</b></p>
                <p style="color: #93C5FD; font-size: 14px; margin: 0;">
                    Price is <b>{z_score:.2f} SD</b> from the mean ({"OVEREXTENDED" if abs(z_score) > 2 else "STABLE"}).
                </p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # INSIDERS
        try:
            st.dataframe(ticker_obj.insider_transactions.head(10), hide_index=True)
        except:
            st.info("No recent Form 4 data available.")
else:
    st.error("📡 Connecting to Market Data...")
