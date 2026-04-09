import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Alpha Scout", layout="wide")

# Optimized team list (PBRA removed to stop download errors)
team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY", "^VIX"]
    try:
        df = yf.download(syms, period="1y", group_by='ticker')
        return df.ffill()
    except:
        return None

# --- ENGINE START ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers)

if all_data is not None:
    stats = []
    spy_df = all_data["SPY"]
    
    for t in tickers:
        try:
            df = all_data[t].dropna()
            if df.empty: continue
            
            p = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            day_pct = ((p - prev) / prev) * 100
            # RS Calculation: Performance vs S&P 500 over last 20 days
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            
            if not pd.isna(p) and p > 0:
                stats.append({"ticker": t, "price": p, "rs": rs, "daily": day_pct})
        except: continue

    # CRITICAL: Sort by RS (Highest Strength at Top)
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    # 2-Column Grid for Mobile Scannability
    rows = [sorted_stats[i:i + 2] for i in range(0, len(sorted_stats), 2)]
    for row in rows:
        cols = st.columns(2)
        for i, s in enumerate(row):
            with cols[i]:
                st.metric(
                    label=f"{s['ticker']} (RS: {s['rs']*100:+.1f}%)", 
                    value=f"${s['price']:.2f}", 
                    delta=f"{s['daily']:+.2f}%"
                )
    
    st.divider()
    # Simple selection for technicals
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    st.info(f"Analyzing {sel}... Charts and Insiders are ready for next module.")

else:
    st.error("📡 Sync Issue: Connection lost.")
