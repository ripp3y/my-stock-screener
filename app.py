import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG & WATCHLIST ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")
WATCHLIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO"]

@st.cache_data(ttl=600)
def fetch_prices(ticker_list):
    try:
        return yf.download(list(ticker_list), period="2y", group_by='ticker').ffill()
    except: return None

# --- 2. THE ENGINE ---
all_data = fetch_prices(WATCHLIST)

if all_data is not None:
    sel = st.selectbox("Select Target", WATCHLIST)
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Intel"])

    with t1:
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=300, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # THE COMMANDER BOX: Shares + Stop + Risk Factor
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        
        t_stop = cp - (atr * 2.5)
        stop_gap = cp - t_stop
        
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 15.0, 3.0)
        risk_amt = acc * (risk_pct / 100)
        
        shares = int(risk_amt / stop_gap) if stop_gap > 0 else 0
        risk_f = (atr / cp) * 100
        
        # Color Logic: Green (Steady), Amber (Aggressive), Red (Extreme)
        color = "#4ADE80" if risk_f < 2.0 else "#FBBF24" if risk_f < 4.5 else "#F87171"
        risk_label = "STEADY" if risk_f < 2.0 else "ACTIVE" if risk_f < 4.5 else "HIGH ALPHA"
        
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 12px; border-left: 10px solid {color};">
                <p style="color: #DBEAFE; font-size: 26px; margin: 0;"><b>Buy {shares} Shares</b></p>
                <p style="color: #93C5FD; font-size: 18px; margin: 5px 0;">Stop Loss: <b>${t_stop:.2f}</b></p>
                <hr style="border: 0.5px solid #3B82F6; margin: 15px 0;">
                <p style="color: #BFDBFE; font-size: 14px; margin: 0;">Risk Factor: <b>{risk_f:.2f}%</b></p>
                <p style="color: {color}; font-size: 14px; margin: 0;"><b>{risk_label} Profile</b> (Gap: ${stop_gap:.2f})</p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # Cleaned Intel Tab
        st.subheader("Ownership & Insider Recon")
        try:
            holders = ticker_obj.major_holders
            if not holders.empty:
                c1, c2 = st.columns(2)
                c1.metric("Institutional", f"{holders.iloc[1, 0]:.1%}" if isinstance(holders.iloc[1, 0], float) else str(holders.iloc[1, 0]))
                c2.metric("Insider", f"{holders.iloc[0, 0]:.1%}" if isinstance(holders.iloc[0, 0], float) else str(holders.iloc[0, 0]))
        except: st.info("Ownership data restricted today.")
        
        st.divider()
        try:
            trades = ticker_obj.insider_transactions
            if not trades.empty:
                st.dataframe(trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(8), hide_index=True, use_container_width=True)
            else: st.info("No recent Form 4 filings.")
        except: st.warning("SEC Database Offline")

else:
    st.error("📡 Sync Issue: Markets Offline?")
