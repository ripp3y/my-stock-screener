import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG & NEW WATCHLIST ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Updated per your shift to MRVL, SNDK, AUGO
team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "GEV": 1050.0, "TPL": 639.0, 
    "STX": 528.0, "MRVL": 131.0, "SNDK": 942.0, "AUGO": 101.0
}

@st.cache_data(ttl=600)
def fetch_terminal_data(tickers):
    try:
        # Pulling 2y history for solid Z-Score/Momentum base
        return yf.download(list(tickers), period="2y", group_by='ticker').ffill()
    except:
        return None

# --- 2. ENGINE ---
all_data = fetch_terminal_data(team_intel.keys())

if all_data is not None:
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Intel"])

    with t1:
        # Charting current price action
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # COMMANDER CORE (Z-Score & Risk)
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # Fixed Z-Score Math
        ma_20 = df_sel['Close'].rolling(20).mean().iloc[-1]
        std_20 = df_sel['Close'].rolling(20).std().iloc[-1]
        z_val = (cp - ma_20) / (std_20 + 1e-6)
        
        # Position Sizing
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 15.0, 3.0)
        risk_amt = acc * (risk_pct / 100)
        shares = int(risk_amt / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        
        risk_factor = (atr / cp) * 100
        color = "#4ADE80" if risk_factor < 2.0 else "#FBBF24" if risk_factor < 4.0 else "#F87171"
        
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 10px solid {color};">
                <p style="color: #DBEAFE; font-size: 20px; margin: 0;"><b>Risk Factor:</b> {risk_factor:.2f}% | <b>Shares:</b> {shares}</p>
                <p style="color: {color}; font-size: 14px; margin: 5px 0;">Z-Score: {z_val:.2f} (Standard Deviations)</p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # ROBUST INTEL TAB
        st.subheader("Ownership Profile")
        try:
            holders = ticker_obj.major_holders
            if not holders.empty:
                c1, c2 = st.columns(2)
                # Cleaning for mobile metrics
                inst = holders.iloc[1, 0]
                ins = holders.iloc[0, 0]
                c1.metric("Institutional", f"{inst:.1%}" if isinstance(inst, float) else str(inst))
                c2.metric("Insider", f"{ins:.1%}" if isinstance(ins, float) else str(ins))
            else:
                st.info("Seeking fresh ownership data...")
        except:
            st.info("Data restricted or loading...")

        st.divider()
        st.subheader("Insider Action")
        try:
            trades = ticker_obj.insider_transactions
            if trades is not None and not trades.empty:
                # Scannable Insider Table
                df_trades = trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(10).copy()
                
                # Green/Red Styling
                def color_logic(row):
                    c = '#4ADE80' if 'Buy' in str(row.Transaction) else '#F87171'
                    return [f'color: {c}; font-weight: bold;'] * len(row)

                st.dataframe(df_trades.style.apply(color_logic, axis=1), hide_index=True, use_container_width=True)
            else:
                st.write("No major insider moves reported.")
        except:
            st.warning("SEC Feed offline.")

else:
    st.error("📡 Sync Issue.")
