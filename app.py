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

st.set_page_config(page_title="Radar v3.26", layout="wide")

# --- COMPACT STYLING [MODULE: COMPACT-UI-GRID] ---
st.markdown("""
    <style>
    th { font-size: 10px !important; color: #94A3B8; }
    td { font-size: 11px !important; white-space: nowrap !important; }
    .stSelectbox label { font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar v3.26")
st.caption(f"Neural Link: ACTIVE | {datetime.now().strftime('%H:%M:%S')}")

all_tickers = [t for sub in RADAR_LIST.values() for t in sub]
master_df = fetch_broad_market(",".join(all_tickers))

tab_scout, tab_recon = st.tabs(["🔍 BROAD SCOUT", "📊 RECON"])

with tab_scout:
    # --- [MODULE: DYNAMIC-SORT-HEADER] ---
    c1, c2 = st.columns([1, 1])
    sort_col = c1.selectbox("Sort By", ["Vel", "Tkr", "Sec", "Price"], index=0)
    sort_order = c2.selectbox("Order", ["Descending", "Ascending"], index=0)

    results = []
    for sector, tickers in RADAR_LIST.items():
        for t in tickers:
            try:
                t_df = master_df[t].dropna()
                curr_p = t_df['Close'].iloc[-1]
                
                # Scoring (v3.22 Logic)
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
                    "Price": curr_p, # Keep as float for sorting
                    "Vel": score,    # Keep as int for sorting
                    "Status": "🚀LEAD" if score >= 4 else "🧱ACUM" 
                })
            except: continue
    
    # Process Sort and Formatting
    df_display = pd.DataFrame(results)
    is_asc = (sort_order == "Ascending")
    df_display = df_display.sort_values(by=sort_col, ascending=is_asc)
    
    # Apply visual formatting after sorting
    df_display['Price'] = df_display['Price'].apply(lambda x: f"${x:.2f}")
    df_display['Vel'] = df_display['Vel'].apply(lambda x: f"{x}/5")

    st.table(df_display)

with tab_recon:
    sel = st.selectbox("Target Recon", all_tickers)
    # [MODULE: CHART-SYNTAX-SHIELD] logic follows...
