import streamlit as st
import pandas as pd
import yfinance as yf

# 1. SETUP - Must be first to avoid NameError
st.set_page_config(page_title="Radar v6.20", layout="wide")

# 2. DATA (Using yfinance 0.2.64 as per your requirements)
@st.cache_data(ttl=600)
def pull_tactical_data(tickers):
    return yf.download(tickers, period="2d", interval="1h", group_by='ticker', progress=False)

# 3. HEADER
st.title("📡 Radar v6.20: Strategic Core")

# 4. RECON TAB (Restoring the Green Highlight you liked)
tab1, tab2 = st.tabs(["📊 RECON", "🌪️ ALPHA"])

with tab1:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    raw_data = pull_tactical_data(portfolio)
    
    recon_rows = []
    for t in portfolio:
        try:
            curr = raw_data[t]['Close'].iloc[-1]
            prev = raw_data[t]['Close'].iloc[-5] # ~24h ago in trading hours
            move = ((curr - prev) / prev) * 100
            
            status = "🔥 SPIKING" if move > 3 else "Steady"
            if t == "NVTS": status = "⚡ Hyper-Growth"

            recon_rows.append({
                "Ticker": t,
                "Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "Mission Status": status
            })
        except: continue

    df = pd.DataFrame(recon_rows)
    
    # Restore the "Bright Green" Styling logic
    def color_rows(row):
        if "Hyper-Growth" in row['Mission Status'] or "SPIKING" in row['Mission Status']:
            return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
        return [''] * len(row)

    st.table(df.style.apply(color_rows, axis=1))

    # CHART TRIGGER - Direct link to avoid Streamlit buffering
    st.write("### 📈 Tactical Charts")
    selected_chart = st.selectbox("Select Ticker for Deep Recon:", portfolio)
    st.link_button(f"Open {selected_chart} Live Chart", f"https://finance.yahoo.com/quote/{selected_chart}/chart")

with tab2:
    st.subheader("Alpha Scanner")
    st.write("Searching for volume anomalies...")
    # Add your Alpha Filter logic here
