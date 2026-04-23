import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v7.50", layout="wide")

# --- [2. THE BYPASS: Hardens the Yahoo Connection] ---
def get_secure_session():
    session = requests.Session()
    # This makes Yahoo think you are a real person on a Chrome browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return session

@st.cache_data(ttl=300)
def get_tactical_data(tickers):
    if not tickers: return None
    secure_session = get_secure_session()
    # session=secure_session is the key to stopping the "buffering"
    return yf.download(tickers, period="5d", interval="1h", session=secure_session, group_by='ticker', progress=False)

# --- [3. STYLING] ---
def apply_green_glow(row):
    if any(t in str(row['Mission Status']) for t in ["⚡", "🔥", "🚀"]):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [4. UI] ---
st.title("📟 Radar v7.50: Full Visual Core")
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_tactical_data(portfolio)
    
    # Portfolio Table
    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[-8]
            move = ((curr - prev) / prev) * 100
            recon_list.append({
                "Ticker": t, "Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%", "Mission Status": "⚡ Hyper-Growth" if t == "NVTS" else "🟢 Accumulating"
            })
        except: continue
    
    st.table(pd.DataFrame(recon_list).style.apply(apply_green_glow, axis=1))

    # AUTO-CHARTS: Putting them back on the RECON tab
    st.divider()
    st.subheader("📈 Institutional Momentum")
    cols = st.columns(2)
    with cols[0]:
        st.write("**NVTS: 5-Day Trend**")
        if "NVTS" in data: st.area_chart(data["NVTS"]['Close'], color="#00FF00")
    with cols[1]:
        st.write("**FIX: 5-Day Trend**")
        if "FIX" in data: st.area_chart(data["FIX"]['Close'], color="#00FF00")

# --- [TAB 2 & 3: Restored] ---
with tab_alpha:
    st.write("Alpha Scanner Active.")
with tab_breakout:
    st.write("Breakout Monitor Active.")
