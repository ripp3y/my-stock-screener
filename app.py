import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [LIBRARY: DATA-CACHING-IRON] ---
@st.cache_data(ttl=300)
def fetch_stones(ticker_string):
    tickers = ticker_string.split(',')
    return yf.download(tickers, period="5d", interval="60m", group_by='ticker', progress=False)

# --- BACKBONE: STEPPING STONES + INTEL ---
RADAR_DATA = {
    "STX": {"type": "ENGINE", "intel": "AI Storage Surge | 52-Week High | Target $600+"},
    "MRVL": {"type": "ENGINE", "intel": "Data Center +29% YTD | AI Custom Silicon Lead"},
    "SNDK": {"type": "ENGINE", "intel": "Nasdaq-100 Entry Complete | Supply Shortage Play"},
    "LASR": {"type": "ACTIVE", "intel": "Strong Buy | Earnings +132% YoY | Bull Run"},
    "AXTI": {"type": "WATCH", "intel": "⚠️ Offering priced at $64.25 | Wait for floor"},
    "MSFT": {"type": "WATCH", "intel": "Earnings 4/29 | Azure Growth 39% | Stable"},
    "ATRO": {"type": "WATCH", "intel": "Aerospace Electrification | Pivot Bottom $62"}
}

st.set_page_config(page_title="Radar v3.35", layout="wide")

# --- MOBILE UI SHIELD (Optimized for Small Screens) ---
st.markdown("""
    <style>
    .block-container { padding: 0.4rem 0.4rem; }
    [data-testid="stHeader"] { visibility: hidden; }
    .stButton > button { width: 100%; height: 35px; border-radius: 4px; }
    .intel-text { font-size: 11px; color: #94A3B8; margin-top: -10px; padding-bottom: 10px; }
    th { font-size: 11px !important; }
    td { font-size: 14px !important; font-weight: 600; padding-top: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar v3.35 [INTEL]")
st.caption(f"Stone Hop: ACTIVE | {datetime.now().strftime('%H:%M:%S')}")

all_tickers = list(RADAR_DATA.keys())
master_df = fetch_stones(",".join(all_tickers))

tab_scout, tab_recon = st.tabs(["🔍 SCOUT", "📊 RECON"])

with tab_scout:
    # --- [MODULE: MOBILE-PILOT-SORT] ---
    c1, c2, c3 = st.columns(3)
    sort_vel = c1.button("🔥 VEL")
    sort_pri = c2.button("💰 PRICE")
    sort_tkr = c3.button("🏷️ TKR")

    results = []
    for t, info in RADAR_DATA.items():
        try:
            t_df = master_df[t].dropna()
            curr_p = t_df['Close'].iloc[-1]
            prev_p = t_df['Close'].iloc[0]
            
            # Velocity Logic
            score = 0
            score += 1 if curr_p > prev_p else 0 
            score += 1 if t_df['Volume'].iloc[-1] > t_df['Volume'].mean() else 0 
            score += 1 if info["type"] == "ENGINE" else 0

            results.append({
                "Tkr": t,
                "Price_val": curr_p,
                "Price": f"${curr_p:.2f}",
                "Vel_val": score,
                "Vel": f"{score}/5",
                "Intel": info["intel"]
            })
        except: continue
    
    df_display = pd.DataFrame(results)
    if sort_pri: df_display = df_display.sort_values(by="Price_val", ascending=False)
    elif sort_tkr: df_display = df_display.sort_values(by="Tkr")
    else: df_display = df_display.sort_values(by="Vel_val", ascending=False)

    # Render with Intel-Flow
    for _, row in df_display.iterrows():
        st.write(f"**{row['Tkr']}** | {row['Price']} | `{row['Vel']}`")
        st.markdown(f"<div class='intel-text'>{row['Intel']}</div>", unsafe_allow_html=True)
        st.divider()

with tab_recon:
    sel = st.selectbox("Stone Select", all_tickers)
    st.info(f"Targeting: {RADAR_DATA[sel]['intel']}")
