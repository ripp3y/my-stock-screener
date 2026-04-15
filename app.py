import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [LIBRARY: DATA-CACHING-IRON] ---
@st.cache_data(ttl=300)
def fetch_broad_market(ticker_string):
    tickers = ticker_string.split(',')
    return yf.download(tickers, period="5d", interval="60m", group_by='ticker', progress=False)

# --- BACKBONE: BROAD SPECTRUM SECTORS ---
RADAR_LIST = {
    "TECH": ["SNDK", "NVDA", "MRVL", "CIEN", "AMD"],
    "ENGY": ["AUGO", "XLE"],
    "BIO": ["IBB", "VRTX"],
    "GROW": ["PLTR", "SNOW"]
}

st.set_page_config(page_title="Radar v3.28", layout="wide")

# --- [MODULE: CLEAN-HEADER-v1] ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem; }
    [data-testid="stHeader"] { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar v3.28")
st.caption(f"Pulse: {datetime.now().strftime('%H:%M:%S')}")

all_tickers = [t for sub in RADAR_LIST.values() for t in sub]
master_df = fetch_broad_market(",".join(all_tickers))

tab_scout, tab_recon = st.tabs(["🔍 BROAD SCOUT", "📊 RECON"])

with tab_scout:
    # --- [MODULE: INTERACTIVE-GRID-v2] ---
    results = []
    for sector, tickers in RADAR_LIST.items():
        for t in tickers:
            try:
                t_df = master_df[t].dropna()
                curr_p = t_df['Close'].iloc[-1]
                
                # Scoring (v3.22 Proven Backbone)
                score = 0
                score += 1 if curr_p > t_df['Close'].iloc[0] else 0 
                score += 1 if t_df['Volume'].iloc[-1] > t_df['Volume'].mean() else 0 
                delta = t_df['Close'].diff()
                rsi = 100 - (100 / (1 + (delta.where(delta > 0, 0).mean() / (delta.where(delta < 0, 0).abs().mean() + 1e-9))))
                score += 1 if rsi < 65 else 0 
                score += 2 if sector == "TECH" else 1 

                results.append({
                    "Tkr": t,
                    "Sec": sector,
                    "Price": round(curr_p, 2),
                    "Vel": f"{score}/5",
                    "Status": "🚀LEAD" if score >= 4 else "🧱ACUM" 
                })
            except: continue
    
    # Render the dynamic grid. TAP HEADERS TO SORT.
    st.dataframe(
        pd.DataFrame(results),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Price": st.column_config.NumberColumn(format="$%.2f"),
            "Tkr": st.column_config.TextColumn(width="small"),
            "Sec": st.column_config.TextColumn(width="small"),
            "Vel": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="medium")
        }
    )

with tab_recon:
    sel = st.selectbox("Target", all_tickers)
    # [MODULE: CHART-SYNTAX-SHIELD] logic follows...
