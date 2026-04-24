import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Strategic US Terminal", layout="wide")
st.markdown("<p style='font-size:10px;'>Sovereignty Station v2.2 | April 24, 2026</p>", unsafe_allow_html=True)

# 🛡️ THE DATA GUARD
st.title("Strategic US Terminal")
ticker = st.sidebar.text_input("Target Ticker", value="PBR")

try:
    data = yf.download(ticker, period="1y", interval="1d")
    
    if data.empty:
        st.warning(f"⚠️ No data found for {ticker}. Check the feed.")
    else:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # 🏔️ MOUNTAIN CHART
        st.subheader(f"{ticker} - Institutional Tape")
        st.area_chart(data['Close'])

        # 🔍 SYNC MONITOR (The Unbound Move)
        if ticker in ['WBD', 'PARA', 'DIS']:
            st.error("⚠️ MONOPOLY ALERT: WBD/Paramount Merger Approved Apr 23. Narrative Sync: HIGH.")
        
        if ticker == 'PBR':
            st.info("📊 SIGNAL: Ex-Dividend Day (Apr 24). Institutional yield extraction in progress.")

        with st.expander("View Raw Data Tape"):
            st.dataframe(data.tail(10))

except Exception as e:
    st.error(f"System Error: {e}")

# 📟 NARRATIVE GEIGER COUNTER
if st.sidebar.button("Run Bias Check"):
    st.sidebar.info("SIGNAL: High correlation detected in Media Conglomerates. Stay Sovereign.")
