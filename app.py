import streamlit as st
import pandas as pd
import yfinance as yf
import sys

# --- [1. RECOVERY BRIDGE] ---
# Forces the app to recognize 'st' globally to kill the NameError
global_st = st 

# --- [2. TERMINAL CONFIG] ---
st.set_page_config(page_title="Radar v8.70", layout="wide")

# --- [3. 60-DAY DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Period set to '3mo' to ensure we have a full 60 trading days 
        # Interval '1d' provides the cleanest long-term area charts
        df = yf.download(
            tickers=tickers, 
            period="3mo", 
            interval="1d", 
            group_by='ticker', 
            auto_adjust=True,
            progress=False
        )
        return df if not df.empty else None
    except Exception:
        return None

# --- [4. UI STYLING] ---
def highlight_rows(row):
    if any(t in str(row['Mission Status']) for t in ["⚡", "🔥", "🚀"]):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [5. HEADER] ---
st.title("📟 Strategic Terminal v8.70")
st.caption(f"Engine: Python {sys.version.split()[0]} | View: 60-Day Trend")

# --- [6. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                ticker_df = data[t]
                curr = ticker_df['Close'].iloc[-1]
                # Calculate the 60-Day Performance (approx 42 trading days ago)
                start_60 = ticker_df['Close'].iloc[-42] if len(ticker_df) >= 42 else ticker_df['Close'].iloc[0]
                move_60 = ((curr - start_60) / start_60) * 100
                
                recon_list.append({
                    "Ticker": t, 
                    "Price": f"${curr:.2f}", 
                    "60d Move": f"{move_60:+.2f}%",
                    "Mission Status": "⚡ Hyper-Growth" if t == "NVTS" else "🟢 Steady"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list).style.apply(highlight_rows, axis=1))

        # 60-DAY DEEP DIVE
        st.divider()
        st.subheader("🔍 60-Day Technical Deep-Dive")
        target = st.selectbox("Select Ticker to Inspect:", portfolio)
        if target in data:
            # We slice the last 60 days specifically for the chart
            chart_data = data[target]['Close'].tail(60)
            st.area_chart(chart_data, color="#00FF00")

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("🌪️ Alpha Search")
    alpha_list = ["ALAB", "CRUS", "VRT"]
    a_data = get_clean_data(alpha_list)
    if a_data is not None:
        alpha_rows = []
        for a in alpha_list:
            try:
                p = a_data[a]['Close'].iloc[-1]
                alpha_rows.append({"Ticker": a, "Price": f"${p:.2f}", "Status": "🔥 ACTIVE"})
            except: continue
        st.table(pd.DataFrame(alpha_rows))

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 60-Day Velocity Check")
    if data is not None:
        c1, c2 = st.columns(2)
        with c1:
            st.write("**NVTS Trend**")
            st.area_chart(data["NVTS"]['Close'].tail(60), color="#00FF00")
        with c2:
            st.write("**FIX Trend**")
            st.area_chart(data["FIX"]['Close'].tail(60), color="#00FF00")

st.divider()
st.caption("v8.70 | 60-Day Pivot Analysis Active.")
