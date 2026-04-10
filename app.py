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
        # --- RISK SCOUT (15% High Alpha Cap) ---
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        acc = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 15.0, 3.0, help="High alpha ceiling active.")
        
        risk_amt = acc * (risk_pct / 100)
        shares = int(risk_amt / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        risk_factor = (atr / cp) * 100
        
        if risk_factor < 2.0: color, status = "#4ADE80", "LOW RISK"
        elif risk_factor < 4.0: color, status = "#FBBF24", "HIGH RISK"
        else: color, status = "#F87171", "EXTREME RISK"
        
        st.markdown(f"### {sel} Status: ACCUMULATING", help="VPT logic check.")
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 10px solid {color};">
                <p style="color: #DBEAFE; font-size: 20px; margin: 0;"><b>Risk Factor:</b> {risk_factor:.2f}% | <b>Shares:</b> {shares}</p>
                <p style="color: {color}; font-size: 16px; margin: 5px 0; font-weight: bold;">CONDITION: {status}</p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # --- SIMPLIFIED INTEL ---
        st.subheader("Ownership %")
        try:
            holders = ticker_obj.major_holders
            c1, c2 = st.columns(2)
            inst_val = holders.iloc[1, 0]
            ins_val = holders.iloc[0, 0]
            c1.metric("Institutional", f"{inst_val:.1%}" if isinstance(inst_val, float) else inst_val)
            c2.metric("Insider", f"{ins_val:.1%}" if isinstance(ins_val, float) else ins_val)
        except:
            st.info("Ownership data loading...")

        st.divider()
        st.subheader("Insider Action")
        try:
            trades = ticker_obj.insider_transactions
            if trades is not None and not trades.empty:
                df_trades = trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(12).copy()
                
                # Apply Green/Red row colors
                def color_rows(row):
                    color = '#4ADE80' if 'Buy' in str(row.Transaction) else '#F87171'
                    return [f'color: {color}'] * len(row)

                st.dataframe(
                    df_trades.style.apply(color_rows, axis=1),
                    column_config={
                        "Start Date": "Date",
                        "Shares": st.column_config.NumberColumn("Units", format="%d")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.write("No major moves reported.")
        except:
            st.warning("SEC Feed offline.")

else:
    st.error("📡 Sync Issue.")
