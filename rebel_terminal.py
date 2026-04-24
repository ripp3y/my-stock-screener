import streamlit as st
import pandas as pd
import requests  # <--- This was the missing bolt!

# --- [1. CONFIG] ---
st.set_page_config(page_title="PRO v11.13")
API_KEY = "3HIAJ4MY3OPVFXCF" 

# --- [2. THE ENGINE] ---
def get_pro_data(ticker):
    try:
        # Direct URL to the AlphaVantage Pro Server
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}&datatype=csv'
        response = requests.get(url)
        # Convert the response text into a table
        from io import StringIO
        return pd.read_csv(StringIO(response.text))
    except Exception as e:
        st.error(f"Engine Sputter: {e}")
        return None

# --- [3. INTERFACE] ---
st.title("📟 PRO v11.13")
st.caption("AlphaVantage Active | Galax Hub")

if st.button("CRANK ENGINE"):
    with st.spinner("Firing..."):
        data = get_pro_data("NVTS")
        
        if data is not None and not data.empty and 'price' in data.columns:
            st.success("✅ SPARK!")
            
            price = data['price'].iloc[0]
            change = data['change_percent'].iloc[0]
            
            st.metric("NVTS", f"${float(price):.2f}", f"{change}")
            st.balloons()
        else:
            st.error("No data returned. Wait 60 seconds (API limit) and try again.")
