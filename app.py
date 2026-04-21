import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [LIBRARY: DATA-CACHING-IRON] ---
@st.cache_data(ttl=300)
def fetch_stones(ticker_string):
    tickers = ticker_string.split(',')
    return yf.download(tickers, period="5d", interval="60m", group_by='ticker', progress=False)

# --- BACKBONE: STEPPING STONES (v3.31) ---
RADAR_LIST = {
    "ENGINES": ["STX", "MRVL", "SNDK"],
    "ACTIVE_HOP": ["LASR"],
    "WATCH_LIST": ["AXTI", "MSFT"]
}

st.set_page_config(page_title="Radar v3.31", layout="wide")

# --- MOBILE UI SHIELD ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem; }
    [data-testid="stHeader"] { visibility: hidden; }
    .stButton > button { width: 100%; font-size: 12px; height: 35px; border-radius: 5px; }
    th { font-size: 11px !important; color: #94A3B8; }
    td { font-size: 13px !important; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar v3.31")
st.caption(f"Stone Hop Active | {datetime.now().strftime('%H:%M:%S')}")

all_tickers = [t for sub in RADAR_LIST.values() for t in sub]
master_df = fetch_stones(",".join(all_tickers))

tab_scout, tab_recon = st.tabs(["🔍 SCOUT", "📊 RECON"])

with tab_scout:
    # --- [MODULE: MOBILE-PILOT-SORT] ---
    c1, c2, c3 = st.columns(3)
    sort_vel = c1.button("🔥 VEL")
    sort_pri = c2.button("💰 PRICE")
    sort_tkr = c3.button("🏷️ TKR")

    results = []
    for category, tickers in RADAR_LIST.items():
        for t in tickers:
            try:
                t_df = master_df[t].dropna()
                curr_p = t_df['Close'].iloc[-1]
                prev_p = t_df['Close'].iloc[0]
                
                # [MODULE: SCOUT-5PT-LOGIC]
                score = 0
                score += 1 if curr_p > prev_p else 0 
                score += 1 if t_df['Volume'].iloc[-1] > t_df['Volume'].mean() else 0 
                score += 2 if category == "ENGINES" else 1 

                results.append({
                    "Tkr": t,
                    "Price_val": curr_p,
                    "Price": f"${curr_p:.2f}",
                    "Vel_val": score,
                    "Vel": f"{score}/5",
                    "Status": "🚀LEAD" if score >= 4 else "🧱ACUM" if score >= 2 else "🔎SCAN"
                })
            except: continue
    
    df_display = pd.DataFrame(results)
    
    # Sort Engine
    if sort_pri: df_display = df_display.sort_values(by="Price_val", ascending=False)
    elif sort_tkr: df_display = df_display.sort_values(by="Tkr")
    else: df_display = df_display.sort_values(by="Vel_val", ascending=False)

    st.table(df_display[["Tkr", "Price", "Vel", "Status"]])

with tab_recon:
    sel = st.selectbox("Stone Select", all_tickers)
    st.info(f"Hopping Target: {sel}")
