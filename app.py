import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_terminal_data(tickers):
    syms = tickers + ["SPY", "QQQ"] # Added QQQ for tech sector correlation
    try:
        data = yf.download(syms, period="2y", group_by='ticker') # 2y to prevent 'nan' on indicators
        return data.ffill()
    except:
        return None

# --- ENGINE ---
all_data = fetch_terminal_data(list(team_intel.keys()))

if all_data is not None:
    # ... (Leaderboard Logic remains the same)

    # --- ANALYSIS HUB ---
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3, t4 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🌐 Correlation", "🕵️ Insiders"])

    with t1:
        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # --- REFINED RISK SCOUT ---
        cp = df_sel['Close'].iloc[-1]
        
        # Robust ATR
        hi_lo = df_sel['High'] - df_sel['Low']
        tr = pd.concat([hi_lo, (df_sel['High']-df_sel['Close'].shift()).abs()], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # Robust RVI (Fixed 'nan' by adding fillna/minimum period check)
        change = df_sel['Close'].diff()
        std_up = change.where(change > 0).rolling(10).std().fillna(0)
        std_down = change.where(change < 0).rolling(10).std().fillna(0)
        rvi_series = (std_up / (std_up + std_down + 0.001)) * 100 # +0.001 prevents div by zero
        curr_rvi = rvi_series.iloc[-1]
        
        # Sharpe Ratio
        returns = df_sel['Close'].pct_change().dropna()
        sharpe = (returns.mean() / (returns.std() + 0.001)) * np.sqrt(252)
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("ATR Volatility", f"${atr:.2f}")
            st.metric("Volatility Stop", f"${t_stop:.2f}", delta=f"${cp - t_stop:.2f} Buffer")
        with c2:
            st.metric("Sharpe Ratio", f"{sharpe:.2f}")
            st.metric("RVI (Vol Direction)", f"{curr_rvi:.1f}")

        # Position Sizer
        st.divider()
        acc_size = st.number_input("Account Size ($)", value=10000)
        risk_pct = st.slider("Risk Per Trade %", 0.5, 3.0, 1.0)
        risk_amt = acc_size * (risk_pct / 100)
        shares = int(risk_amt / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        
        # BIG BLUE FOOTER
        risk_factor = (atr / cp) * 100
        risk_status = "STABLE" if risk_factor < 3 else "VOLATILE" if risk_factor < 5 else "EXTREME"
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6;">
                <h3 style="color: white; margin: 0;">Risk Analysis: {sel}</h3>
                <p style="color: #DBEAFE; font-size: 18px; margin: 5px 0;">
                    <b>Risk Factor:</b> {risk_factor:.2f}% | <b>Condition:</b> {risk_status}
                </p>
                <p style="color: #93C5FD; font-size: 14px; margin: 0;">
                    Max position: <b>{shares} shares</b>. RVI indicates <b>{"Expanding" if curr_rvi > 50 else "Contracting"}</b> volatility.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # --- NEW VITAL TOOL: SECTOR CORRELATION ---
        st.subheader("🌐 Correlation Matrix (20-Day)")
        corr_df = all_data.xs('Close', axis=1, level=1).pct_change().corr()
        st.dataframe(corr_df.style.background_gradient(cmap='RdBu_r'), use_container_width=True)
        st.info("High correlation (>0.8) means assets move together. Watch for 'Over-Concentration'.")

    with t4:
        # Insider Transactions
        try:
            st.dataframe(ticker_obj.insider_transactions.head(10), hide_index=True)
        except:
            st.warning("No insider data found.")

else:
    st.error("Connection lost.")
