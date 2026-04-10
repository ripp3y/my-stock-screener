import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. SETTINGS ---
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
    except Exception:
        return None

# --- 2. THE ENGINE ---
all_data = fetch_terminal_data(list(team_intel.keys()))

if all_data is not None:
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Intel"])

    with t1:
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
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # FIXED SYNTAX: Z-Score Logic
        ma_20 = df_sel['Close'].rolling(20).mean().iloc[-1]
        std_20 = df_sel['Close'].rolling(20).std().iloc[-1]
        z_score = (cp - ma_20) / (std_20 + 1e-6)
        
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 15.0, 3.0)
        
        risk_amt = acc * (risk_pct / 100)
        shares = int(risk_amt / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        risk_factor = (atr / cp) * 100
        
        color = "#4ADE80" if risk_factor < 2.0 else "#FBBF24" if risk_factor < 4.0 else "#F87171"
        
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 10px solid {color};">
                <p style="color: #DBEAFE; font-size: 20px; margin: 0;"><b>Risk Factor:</b> {risk_factor:.2f}% | <b>Shares:</b> {shares}</p>
                <p style="color: {color}; font-size: 14px; margin: 5px 0;">Z-Score: {z_score:.2f} SD from mean</p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # --- ROBUST INTEL TAB ---
        st.subheader("Ownership Profile")
        try:
            # Fallback for empty dataframes
            holders = ticker_obj.major_holders
            if holders is not None and not holders.empty:
                c1, c2 = st.columns(2)
                inst = holders.iloc[1, 0]
                ins = holders.iloc[0, 0]
                c1.metric("Institutional", f"{inst:.1%}" if isinstance(inst, float) else str(inst))
                c2.metric("Insider", f"{ins:.1%}" if isinstance(ins, float) else str(ins))
            else:
                st.info("Direct ownership data unavailable for this ticker.")
        except Exception:
            st.warning("Holders feed currently restricted.")

        st.divider()
        st.subheader("Recent Insider Moves")
        try:
            trades = ticker_obj.insider_transactions
            if trades is not None and not trades.empty:
                df_trades = trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(10).copy()
                
                def color_trades(row):
                    c = '#4ADE80' if 'Buy' in str(row.Transaction) else '#F87171'
                    return [f'color: {c}'] * len(row)

                st.dataframe(df_trades.style.apply(color_trades, axis=1), hide_index=True, use_container_width=True)
            else:
                st.info("No reported insider activity in the last 6 months.")
        except Exception:
            st.error("Unable to reach SEC database.")

else:
    st.error("📡 Connection Lost.")
