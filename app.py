import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Your core watchlist
team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_terminal_data(tickers):
    syms = tickers + ["SPY"]
    try:
        return yf.download(syms, period="1y", group_by='ticker').ffill()
    except:
        return None

# --- 2. THE ENGINE ---
all_data = fetch_terminal_data(list(team_intel.keys()))

if all_data is not None:
    stats = []
    spy_df = all_data["SPY"]
    
    for t in team_intel.keys():
        try:
            df = all_data[t].dropna()
            p = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            # RS: Relative Strength vs Benchmark
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": p, "rs": rs, "daily": ((p-prev)/prev)*100})
        except: continue

    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # Header Leaderboard
    cols = st.columns(2)
    for i, s in enumerate(sorted_stats):
        with cols[i % 2]:
            st.metric(f"{s['ticker']} (RS: {s['rs']*100:+.1f}%)", f"${s['price']:.2f}", f"{s['daily']:+.2f}%")

    st.divider()

    # --- 3. ANALYSIS HUB ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        # FLAT CHART (Height 300)
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False,
            height=300, margin=dict(l=5, r=5, t=10, b=10),
            yaxis=dict(fixedrange=False, side="right", showgrid=True, gridcolor="#333"),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        # RISK SCOUT TOOLS
        cp = df_sel['Close'].iloc[-1]
        hi_lo = df_sel['High'] - df_sel['Low']
        tr = pd.concat([hi_lo, (df_sel['High']-df_sel['Close'].shift()).abs()], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        
        # Risk Factor Calculation (ATR as % of price)
        risk_factor = (atr / cp) * 100
        risk_status = "STABLE" if risk_factor < 3 else "VOLATILE" if risk_factor < 5 else "EXTREME"
        
        st.metric("ATR Volatility", f"${atr:.2f}", help="Standard daily range.")
        st.metric("Trailing Stop", f"${t_stop:.2f}", delta=f"${cp - t_stop:.2f} Buffer")
        
        # THE BIG BLUE FOOTER
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-top: 20px;">
                <h3 style="color: white; margin: 0;">Risk Analysis: {sel}</h3>
                <p style="color: #DBEAFE; font-size: 18px; margin: 5px 0;">
                    <b>Risk Factor:</b> {risk_factor:.2f}% | <b>Condition:</b> {risk_status}
                </p>
                <p style="color: #93C5FD; font-size: 14px; margin: 0;">
                    Status is based on current ATR relative to price action.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        # INSIDER ROSTER
        try:
            insiders = ticker_obj.insider_transactions
            if insiders is not None and not insiders.empty:
                st.dataframe(insiders[['Start Date', 'Insider', 'Transaction', 'Shares']].head(10), hide_index=True)
            else:
                st.info("No recent Form 4 filings.")
        except:
            st.error("Live feed timeout.")

else:
    st.error("📡 Connection to data stream lost.")
