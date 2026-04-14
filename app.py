import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIG & REFRESHED WATCHLIST ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# This is your new "Command Center" for the watchlist
# We added MRVL, SNDK, and AUGO
WATCHLIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO"]

@st.cache_data(ttl=600)
def fetch_prices(ticker_list):
    try:
        # We pass a simple LIST here to avoid the Unhashable error
        return yf.download(list(ticker_list), period="2y", group_by='ticker').ffill()
    except Exception:
        return None

# --- 2. THE ENGINE ---
all_data = fetch_prices(WATCHLIST)

if all_data is not None:
    sel = st.selectbox("Select Target", WATCHLIST)
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Intel"])

    with t1:
        # Candle Chart
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # RISK & Z-SCORE (Fixed Syntax)
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # Calculating Z-Score for momentum strength
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
                <p style="color: #93C5FD; font-size: 12px; margin: 0;">15% Alpha Ceiling Applied</p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # INTEL (Ownership & Insiders)
        st.subheader("Ownership Profile")
        try:
            # Using try/except because yfinance feeds can be restricted
            holders = ticker_obj.major_holders
            if holders is not None and not holders.empty:
                c1, c2 = st.columns(2)
                inst = holders.iloc[1, 0]
                ins = holders.iloc[0, 0]
                c1.metric("Institutional", f"{inst:.1%}" if isinstance(inst, float) else str(inst))
                c2.metric("Insider", f"{ins:.1%}" if isinstance(ins, float) else str(ins))
            else:
                st.info("Searching SEC for ownership data...")
        except Exception:
            st.warning("Ownership feed currently restricted.")

        st.divider()
        st.subheader("Insider Moves (Form 4)")
        try:
            trades = ticker_obj.insider_transactions
            if trades is not None and not trades.empty:
                df_trades = trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(12).copy()
                def color_rows(row):
                    c = '#4ADE80' if 'Buy' in str(row.Transaction) else '#F87171'
                    return [f'color: {c}; font-weight: bold;'] * len(row)
                st.dataframe(df_trades.style.apply(color_rows, axis=1), hide_index=True, use_container_width=True)
            else:
                st.info("No reported insider activity.")
        except Exception:
            st.error("Unable to reach SEC database.")

else:
    st.error("📡 Sync Issue: Verify internet connection.")
