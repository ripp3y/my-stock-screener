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
    syms = tickers + ["SPY", "QQQ"]
    try:
        # 2y history ensures all rolling indicators have a solid baseline
        return yf.download(syms, period="2y", group_by='ticker').ffill()
    except:
        return None

# --- ENGINE ---
all_data = fetch_terminal_data(list(team_intel.keys()))

if all_data is not None:
    # --- ANALYSIS HUB ---
    sel = st.selectbox("Select Target", list(team_intel.keys()))
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3, t4 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🌐 Correlation", "🕵️ Insiders"])

    with t1:
        # FLAT CHART RATIO
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=5,r=5,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # --- RISK & MEAN REVERSION TOOLS ---
        cp = df_sel['Close'].iloc[-1]
        
        # 1. Z-Score (Mean Reversion)
        ma_20 = df_sel['Close'].rolling(20).mean()
        std_20 = df_sel['Close'].rolling(20).std()
        z_score = (cp - ma_20.iloc[-1]) / std_20.iloc[-1]
        
        # 2. Risk Metrics
        hi_lo = df_sel['High'] - df_sel['Low']
        tr = pd.concat([hi_lo, (df_sel['High']-df_sel['Close'].shift()).abs()], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # 3. Sharpe & RVI
        returns = df_sel['Close'].pct_change().dropna()
        sharpe = (returns.mean() / (returns.std() + 1e-6)) * np.sqrt(252)
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Z-Score", f"{z_score:.2f}", help=">2.0 is overbought, <-2.0 is oversold")
            st.metric("Sharpe Ratio", f"{sharpe:.2f}")
        with c2:
            st.metric("ATR Volatility", f"${atr:.2f}")
            st.metric("Trailing Stop", f"${t_stop:.2f}")

        # Position Sizer
        st.divider()
        acc = st.number_input("Account Size ($)", value=10000)
        risk = st.slider("Risk %", 0.5, 3.0, 1.0)
        shares = int((acc * (risk/100)) / (cp - t_stop)) if (cp - t_stop) > 0 else 0
        
        # BIG BLUE FOOTER
        rf = (atr / cp) * 100
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6;">
                <h3 style="color: white; margin: 0;">{sel} Risk: {"EXTREME" if rf > 5 else "STABLE"}</h3>
                <p style="color: #DBEAFE; margin: 5px 0;">Risk Factor: <b>{rf:.2f}%</b> | Max: <b>{shares} shares</b></p>
                <p style="color: #93C5FD; font-size: 14px; margin: 0;">
                    Z-Score of <b>{z_score:.2f}</b> suggests price is <b>{"Extended" if abs(z_score) > 2 else "Neutral"}</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # CORRELATION HEATMAP
        st.subheader("🌐 20-Day Matrix")
        corr = all_data.xs('Close', axis=1, level=1).pct_change().corr()
        st.dataframe(corr.style.background_gradient(cmap='RdBu_r').format("{:.2f}"))

    with t4:
        # INSIDERS
        try:
            st.dataframe(ticker_obj.insider_transactions.head(10), hide_index=True)
        except:
            st.info("No recent Form 4 data.")
else:
    st.error("📡 Sync Issue.")
