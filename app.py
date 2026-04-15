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

st.set_page_config(page_title="Radar v3.29", layout="wide")

# --- COMPACT STYLING ---
st.markdown("""
    <style>
    .stButton > button { width: 100%; font-size: 10px; padding: 2px; }
    th { font-size: 10px !important; }
    td { font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar v3.29")
st.caption(f"Pulse: {datetime.now().strftime('%H:%M:%S')}")

all_tickers = [t for sub in RADAR_LIST.values() for t in sub]
master_df = fetch_broad_market(",".join(all_tickers))

tab_scout, tab_recon = st.tabs(["🔍 BROAD SCOUT", "📊 RECON"])

with tab_scout:
    # --- [MODULE: MOBILE-PILOT-SORT] ---
    st.write("Sort Priority:")
    c1, c2, c3 = st.columns(3)
    sort_vel = c1.button("🔥 VEL")
    sort_pri = c2.button("💰 PRIC")
    sort_tkr = c3.button("🏷️ TKR")

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
                    "Price_val": curr_p,
                    "Price": f"${curr_p:.2f}",
                    "Vel_val": score,
                    "Vel": f"{score}/5",
                    "Status": "🚀LEAD" if score >= 4 else "🧱ACUM" 
                })
            except: continue
    
    df_display = pd.DataFrame(results)
    
    # Sort Handling
    if sort_pri:
        df_display = df_display.sort_values(by="Price_val", ascending=False)
    elif sort_tkr:
        df_display = df_display.sort_values(by="Tkr")
    else:
        # Default to Velocity (Our primary 100% YoY goal)
        df_display = df_display.sort_values(by="Vel_val", ascending=False)

    # Clean up and display [MODULE: STATIC-TABLE-STABLE]
    final_table = df_display[["Tkr", "Sec", "Price", "Vel", "Status"]]
    st.table(final_table)

with tab_recon:
    sel = st.selectbox("Target Recon", all_tickers)
