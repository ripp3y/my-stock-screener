import streamlit as st
import pandas as pd
import yfinance as yf

# --- [1. CONFIG MUST BE FIRST] ---
st.set_page_config(page_title="Radar v6.50", layout="wide")

# --- [2. DATA LOADERS] ---
@st.cache_data(ttl=3600)
def get_live_metrics(tickers):
    if not tickers: return None
    return yf.download(tickers, period="5d", interval="1h", group_by='ticker', progress=False)

# --- [3. UI HEADER] ---
st.title("📡 Radar v6.50: Interactive Terminal")

# --- [4. TABS] ---
tab_recon, tab_alpha, tab_breakout = st.tabs(["📊 RECON", "🌪️ ALPHA", "🚀 BREAKOUTS"])

# --- [TAB 1: RECON] ---
with tab_recon:
    st.subheader("Tactical Portfolio (Click Ticker for Chart)")
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_live_metrics(portfolio)
    
    recon_list = []
    for t in portfolio:
        try:
            curr = data[t]['Close'].iloc[-1]
            prev = data[t]['Close'].iloc[-8]
            move = ((curr - prev) / prev) * 100
            # GENERATING THE CLICKABLE LINK
            chart_link = f"https://finance.yahoo.com/quote/{t}/chart"
            
            recon_list.append({
                "Ticker": chart_link, # We pass the URL here
                "Symbol": t,
                "Price": f"${curr:.2f}",
                "24h Move": f"{move:+.2f}%",
                "20% Target": f"${curr*1.2:.2f}"
            })
        except: continue
    
    df_recon = pd.DataFrame(recon_list)
    # CONFIGURING THE LINK COLUMN
    st.dataframe(
        df_recon,
        column_config={
            "Ticker": st.column_config.LinkColumn("Chart Link", display_text=r"^https://finance\.yahoo\.com/quote/(.*)/chart$")
        },
        hide_index=True,
        use_container_width=True
    )

# --- [TAB 2: ALPHA] ---
with tab_alpha:
    st.subheader("Market Scanner (Click Ticker to Verify)")
    # Adding clickable links to the Alpha watchlist
    alpha_picks = ["ALAB", "CRUS", "FLR", "AMSC"]
    alpha_data = get_live_metrics(alpha_picks)
    
    alpha_list = []
    for p in alpha_picks:
        try:
            curr = alpha_data[p]['Close'].iloc[-1]
            link = f"https://finance.yahoo.com/quote/{p}/chart"
            alpha_list.append({"Ticker": link, "Price": f"${curr:.2f}", "Status": "🔥 SCANNING"})
        except: continue
    
    st.dataframe(
        pd.DataFrame(alpha_list),
        column_config={"Ticker": st.column_config.LinkColumn("Verify Chart")},
        hide_index=True
    )

# --- [TAB 3: BREAKOUTS] ---
with tab_breakout:
    st.subheader("High-Velocity Leads")
    # Using simple link buttons for the high-priority gems
    st.link_button("🚀 View NVTS Advanced Chart", "https://finance.yahoo.com/quote/NVTS/chart")
    st.link_button("🚀 View FIX Advanced Chart", "https://finance.yahoo.com/quote/FIX/chart")
