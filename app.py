import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- CONFIG & DATA ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY"]
    try:
        return yf.download(syms, period="1y", group_by='ticker').ffill()
    except:
        return None

# --- ENGINE ---
all_data = fetch_scout_data(list(team_intel.keys()))

if all_data is not None:
    stats = []
    spy_df = all_data["SPY"]
    
    for t in team_intel.keys():
        try:
            df = all_data[t].dropna()
            p = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            # RS Rank: Relative Strength vs SPY
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": p, "rs": rs, "daily": ((p-prev)/prev)*100})
        except: continue

    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # Dashboard Leaderboard
    cols = st.columns(2)
    for i, s in enumerate(sorted_stats):
        with cols[i % 2]:
            st.metric(f"{s['ticker']} (RS: {s['rs']*100:+.1f}%)", f"${s['price']:.2f}", f"{s['daily']:+.2f}%")

    st.divider()

    # --- ANALYSIS HUB ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    ticker_obj = yf.Ticker(sel)
    df_sel = all_data[sel].dropna()
    
    t1, t2, t3 = st.tabs(["📊 Technicals", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        # PRO-VIEW HORIZONTAL CHART
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
        # ROBUST RISK LOGIC
        cp = df_sel['Close'].iloc[-1]
        hi_lo = df_sel['High'] - df_sel['Low']
        # Simplified ATR calculation to avoid syntax errors on mobile
        tr_calc = pd.concat([hi_lo, (df_sel['High']-df_sel['Close'].shift()).abs()], axis=1).max(axis=1)
        atr_14 = tr_calc.rolling(14).mean().iloc[-1]
        t_stop = cp - (atr_14 * 2.5)
        
        st.metric("ATR Volatility", f"${atr_14:.2f}")
        st.metric("Volatility Stop", f"${t_stop:.2f}", delta=f"${cp - t_stop:.2f} Buffer")

    with t3:
        # INSIDER ROSTER
        try:
            insider_data = ticker_obj.insider_transactions
            if insider_data is not None and not insider_data.empty:
                st.dataframe(insider_data[['Start Date', 'Insider', 'Transaction', 'Shares']].head(10), hide_index=True)
            else:
                st.info("No recent insider activity reported.")
        except:
            st.error("Live feed sync failed.")

else:
    st.error("📡 Market Data Sync Issue.")
