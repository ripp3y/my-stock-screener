import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- CONFIG ---
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
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": p, "rs": rs, "daily": ((p-prev)/prev)*100})
        except: continue

    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
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
