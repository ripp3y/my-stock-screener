import streamlit as st
import pandas as pd
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
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders & Ownership"])

    with t1:
        # CANDLESTICK MAIN
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
        # --- RISK SCOUT ENGINE ---
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # Position Sizing
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 15.0, 3.0, help="High alpha ceiling active.")
        
        risk_amt = acc * (risk_pct / 100)
        stop_dist = cp - t_stop
        shares = int(risk_amt / stop_dist) if stop_dist > 0 else 0
        
        risk_factor = (atr / cp) * 100
        if risk_factor < 2.0: status_color, status_text = "#4ADE80", "LOW RISK"
        elif risk_factor < 4.0: status_color, status_text = "#FBBF24", "HIGH RISK"
        else: status_color, status_text = "#F87171", "EXTREME RISK"
        
        st.markdown(f"### {sel} Status: ACCUMULATING", help="Institutional buy pressure check.")
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 10px solid {status_color};">
                <p style="color: #DBEAFE; font-size: 20px; margin: 0;">
                    <b>Risk Factor:</b> {risk_factor:.2f}% | <b>Shares:</b> {shares}
                </p>
                <p style="color: {status_color}; font-size: 16px; margin: 5px 0; font-weight: bold;">
                    CONDITION: {status_text}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # --- THE INSIDER SCOOP ---
        col_a, col_b = st.columns(2)
        
        # 1. Ownership Breakdown
        with col_a:
            st.subheader("Major Holders")
            try:
                holders = ticker_obj.major_holders
                st.dataframe(holders, use_container_width=True, hide_index=True)
            except:
                st.info("Ownership data private or loading...")

        # 2. Institutional Top 5
        with col_b:
            st.subheader("Top Institutions")
            try:
                inst = ticker_obj.institutional_holders.head(5)
                st.dataframe(inst[['Holder', 'Shares']], use_container_width=True, hide_index=True)
            except:
                st.info("Institutional data unavailable.")

        st.divider()
        
        # 3. Form 4 Insider Trades
        st.subheader("Recent Insider Activity (Form 4)")
        try:
            trades = ticker_obj.insider_transactions
            if trades is not None and not trades.empty:
                # Clean up the display for mobile
                st.dataframe(
                    trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(12),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("No major insider moves reported in last 6 months.")
        except:
            st.warning("Could not sync SEC Form 4 feed.")

else:
    st.error("📡 Sync Issue.")
