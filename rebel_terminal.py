import streamlit as st
import pandas as pd
import requests

# --- [1. CONFIG] ---
st.set_page_config(page_title="PRO TERMINAL v11.12", layout="wide")
# Your Master Key is now live
API_KEY = "3HIAJ4MY3OPVFXCF" 

# --- [2. THE PRO ENGINE] ---
def get_pro_data(ticker):
    """Bypasses Yahoo entirely. Uses AlphaVantage CSV stream."""
    try:
        # Using the 'GLOBAL_QUOTE' function for a fast, single-price check
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}&datatype=csv'
        df = pd.read_csv(url)
        if not df.empty:
            return df
        return None
    except Exception as e:
        st.error(f"Fuel Line Clog: {e}")
        return None

# --- [3. HEADER] ---
st.title("📟 PRO TERMINAL v11.12")
st.caption("Engine: AlphaVantage Direct | Status: Master Key Active | Hub: Galax")

# --- [4. THE TEST FIRE] ---
st.write("Checking the new fuel source...")

if st.button("CRANK THE BIG BLOCK"):
    with st.spinner("Pumping Data from Pro Server..."):
        # We test with NVTS first
        data = get_pro_data("NVTS")
        
        if data is not None and 'price' in data.columns:
            st.success("✅ CONNECTION ESTABLISHED")
            
            # AlphaVantage Quote returns specific column names
            price = data['price'].iloc[0]
            change = data['change_percent'].iloc[0]
            volume = data['volume'].iloc[0]
            
            c1, c2, c3 = st.columns(3)
            c1.metric("NVTS Price", f"${float(price):.2f}")
            c2.metric("Day Change", f"{change}")
            c3.metric("Volume", f"{int(volume):,}")
            
            st.balloons() # Just to celebrate the firewall break!
        else:
            st.error("Engine sputtered. The API Key is correct, but the server might be throttled. Wait 60 seconds and try again.")

# --- [5. LOGS] ---
st.divider()
st.info("Note: The Free Pro-Key allows 5 'cranks' per minute. Don't spam the button!")

