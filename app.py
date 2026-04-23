import streamlit as st
import pandas as pd
import yfinance as yf
import sys

# --- [1. GLOBAL SAFETY] ---
if 'st' not in globals():
    import streamlit as st

# --- [2. TERMINAL CONFIG] ---
st.set_page_config(page_title="Radar v8.80", layout="wide")

# --- [3. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Standardizing on 3mo/1d for 60-day stability
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception:
        return None

# --- [4. UI STYLING] ---
def highlight_rows(row):
    if any(t in str(row['Mission Status']) for t in ["⚡", "🔥", "🚀"]):
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- [5. HEADER] ---
st.title("📟 Strategic Terminal v8.80")
st.caption(f"Engine: Python {sys.version.split()[0]} | View: 60-Day Core")

# --- [6. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🔥 VOLUME HEAT", "🚀 BREAKOUTS"])

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
                # Calculation for 60-day performance
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

        st.divider()
        st.subheader("🔍 60-Day Technical Deep-Dive")
        target = st.selectbox("Select Ticker to Inspect:", portfolio)
        if target in data:
            st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: VOLUME HEAT (ALPHA)] ---
with tab_alpha:
    st.subheader("🔥 Relative Volume (RVOL) Scanner")
    alpha_list = ["ALAB", "CRUS", "AMSC", "VRT", "SMCI", "NVTS"]
    a_data = get_clean_data(alpha_list)
    
    if a_data is not None:
        vol_results = []
        for a in alpha_list:
            try:
                # RVOL Logic: Current Volume vs 20-Day Avg Volume
                # (Simplified for daily data: Today's Vol / Avg Vol)
                recent_vol = a_data[a]['Volume'].iloc[-1]
                avg_vol = a_data[a]['Volume'].tail(20).mean()
                rvol = recent_vol / avg_vol
                
                intensity = "Normal"
                if rvol > 2.0: intensity = "🚨 MASSIVE SPIKE"
                elif rvol > 1.5: intensity = "🔥 High Inflow"
                
                vol_results.append({
                    "Ticker": a,
                    "Vol Ratio": f"{rvol:.2fx}",
                    "Intensity": intensity,
                    "Price": f"${a_data[a]['Close'].iloc[-1]:.2f}"
                })
            except: continue
        st.table(pd.DataFrame(vol_results))
        st.caption("Strategy: Monitoring RVOL for Institutional Exhaustion or Ignition.")

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("🚀 60-Day Velocity Monitor")
    if data is not None:
        for lead in ["NVTS", "FIX"]:
            st.write(f"**{lead} Momentum Trend**")
            st.area_chart(data[lead]['Close'].tail(60), height=250, color="#00FF00")

st.divider()
st.caption("v8.80 Core Saved. Focusing on NVTS $19.50 Pivot.")
