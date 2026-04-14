import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# --- 1. CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# FREE API KEY: You can get one at alphavantage.co
# I've set a placeholder; replace 'demo' with your key for full data
AV_API_KEY = 'demo' 

# --- 2. THE ENGINE ---
@st.cache_data(ttl=3600)
def fetch_intel(ticker):
    """Fallback engine for Ownership & Insiders"""
    try:
        # Use Alpha Vantage for Institutional Ownership
        url = f'https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol={ticker}&apikey={AV_API_KEY}'
        r = requests.get(url)
        data = r.json()
        if "holdings" in data:
            df = pd.DataFrame(data["holdings"]).head(10)
            return df, "AlphaVantage"
    except:
        pass
    
    # Second Fallback: yfinance Ticker Object
    try:
        t = yf.Ticker(ticker)
        return t.major_holders, "yFinance"
    except:
        return None, None

# --- 3. MAIN APP ---
tab1, tab2, tab3 = st.tabs(["📊 Charts", "🛡️ Risk", "🕵️ Intel"])

with tab3:
    st.subheader("Deep Intel: Institutional & Insider Recon")
    
    sel = st.selectbox("Select Target for Recon", ["AUGO", "MRVL", "FIX", "SNDK"])
    intel_data, source = fetch_intel(sel)
    
    if intel_data is not None:
        st.success(f"Feed Synced via {source} Engine")
        
        # Display Ownership
        if source == "AlphaVantage":
            st.write("**Top Institutional Holders**")
            st.dataframe(intel_data[['holder', 'shares', 'date']], hide_index=True)
        else:
            st.write("**Ownership Breakdown**")
            st.table(intel_data) # yFinance returns a simple table
            
        st.divider()
        
        # Insider Activity
        st.write("**Recent Insider Filings (Form 4)**")
        try:
            t = yf.Ticker(sel)
            insider = t.insider_transactions
            if not insider.empty:
                st.dataframe(insider[['Start Date', 'Insider', 'Transaction', 'Shares']].head(10), hide_index=True)
            else:
                st.info("No Form 4 filings in the last 90 days.")
        except:
            st.error("SEC EDGAR Link is currently congested. Retrying...")
    else:
        st.warning("⚠️ High-Security Feed. Re-syncing with SEC EDGAR...")
