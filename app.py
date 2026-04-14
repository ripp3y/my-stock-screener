import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG & WATCHLIST ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "GEV": 1050.0, "TPL": 639.0, 
    "STX": 528.0, "MRVL": 131.0, "SNDK": 942.0, "AUGO": 101.0
}

# FIXED: We only pass a list of strings here, which Streamlit can hash easily
@st.cache_data(ttl=600)
def fetch_prices(tickers):
    try:
        return yf.download(list(tickers), period="2y", group_by='ticker').ffill()
    except:
        return None

# --- 2. THE ENGINE ---
all_data = fetch_prices(team_intel.keys())

if all_data is not None:
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    
    # We create the ticker object HERE, not in the cached function
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
        # RISK SCOUT CORE
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        ma_20 = df_sel['Close'].rolling(20).mean().iloc[-1]
        std_20 = df_sel['Close'].rolling(20).std().iloc[-1]
        z_val = (cp - ma_20) / (std_20 + 1e-6)
        
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 15.0, 3.0)
        risk_amt = acc * (risk_pct / 100)
        shares = int(risk_amt / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        
        risk_f = (atr / cp) * 100
        color = "#4ADE80" if risk_f < 2.0 else "#FBBF24" if risk_f < 4.0 else "#F87171"
        
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 10px solid {color};">
                <p style="color: #DBEAFE; font-size: 20px; margin: 0;"><b>Risk Factor:</b> {risk_f:.2f}% | <b>Shares:</b> {shares}</p>
                <p style="color: {color}; font-size: 14px; margin: 5px 0;">Z-Score: {z_val:.2f} SD</p>
                <p style="color: #93C5FD; font-size: 12px; margin: 0;">15% Max Risk Ceiling Active</p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # ROBUST INTEL
        st.subheader("Ownership Profile")
        try:
            holders = ticker_obj.major_holders
            if holders is not None and not holders.empty:
                c1, c2 = st.columns(2)
                inst = holders.iloc[1, 0]
                ins = holders.iloc[0, 0]
                c1.metric("Institutional", f"{inst:.1%}" if isinstance(inst, float) else str(inst))
                c2.metric("Insider", f"{ins:.1%}" if isinstance(ins, float) else str(ins))
            else:
                st.info("Direct ownership data not found.")
        except:
            st.info("Ownership feed restricted.")

        st.divider()
        st.subheader("Recent Insider Moves")
        try:
            trades = ticker_obj.insider_transactions
            if trades is not None and not trades.empty:
                df_trades = trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(10).copy()
                def color_logic(row):
                    c = '#4ADE80' if 'Buy' in str(row.Transaction) else '#F87171'
                    return [f'color: {c}; font-weight: bold;'] * len(row)
                st.dataframe(df_trades.style.apply(color_logic, axis=1), hide_index=True, use_container_width=True)
            else:
                st.info("No reported moves.")
        except:
            st.warning("SEC Feed offline.")

else:
    st.error("📡 Sync Issue: Check Internet Connection")
