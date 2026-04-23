import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import sys

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v9.60", layout="wide")

# --- [2. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v9.60")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                curr = data[t]['Close'].iloc[-1]
                recon_list.append({"Ticker": t, "Price": f"${curr:.2f}", "Status": "🚀 Blue Sky" if t == "NVTS" else "🟢 Steady"})
            except: continue
        st.table(pd.DataFrame(recon_list))
        st.area_chart(data["NVTS"]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(crypto_list)
    if c_data is not None:
        for c in crypto_list:
            st.metric(c, f"${c_data[c]['Close'].iloc[-1]:,2f}")
            st.area_chart(c_data[c]['Close'].tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")

# --- [TAB 3: HEAT MAP - REBUILT FOR MOBILE] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Volume (RVOL)")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        # We build the table using HTML to guarantee the colors show up on mobile
        html_table = """
        <table style="width:100%; border-collapse: collapse; font-family: sans-serif;">
            <tr style="background-color: #333; color: white;">
                <th style="padding: 10px; text-align: left;">Ticker</th>
                <th style="padding: 10px; text-align: center;">RVOL</th>
                <th style="padding: 10px; text-align: right;">Price</th>
            </tr>
        """
        
        for h in h_tickers:
            try:
                rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                price = h_data[h]['Close'].iloc[-1]
                
                # Color logic: Extreme = Lime, High = Dark Green, Normal = None
                bg_color = "#00FF00" if rvol > 2.2 else "#008000" if rvol > 1.5 else "transparent"
                text_color = "black" if rvol > 1.5 else "white"
                
                html_table += f"""
                <tr style="border-bottom: 1px solid #444;">
                    <td style="padding: 10px; font-weight: bold;">{h}</td>
                    <td style="padding: 10px; text-align: center; background-color: {bg_color}; color: {text_color}; font-weight: bold;">{rvol:.2f}x</td>
                    <td style="padding: 10px; text-align: right;">${price:.2f}</td>
                </tr>
                """
            except: continue
            
        html_table += "</table>"
        # Use unsafe_allow_html to force the browser to render the styled table
        st.markdown(html_table, unsafe_allow_html=True)
        st.caption("🚨 Highlights: Lime > 2.2x | Green > 1.5x")
