
import streamlit as st
import pandas as pd
import requests
import io

# --- [1. CONFIG] ---
st.set_page_config(page_title="TEST STAND v11.9")

# --- [2. THE BARE FUNCTION] ---
def get_data_manual(ticker):
    """
    Direct CSV pull. 
    NO yfinance, NO scipy, NO specialized libraries.
    """
    try:
        # A simple, static URL to test connection
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?interval=1d&events=history&includeAdjustedClose=true"
        
        # We use 'requests' which is a standard web tool
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Turn the raw text into a table
            df = pd.read_csv(io.StringIO(response.text))
            return df
        else:
            st.error(f"Server rejected request for {ticker} (Code: {response.status_code})")
            return None
    except Exception as e:
        st.error(f"Mechanical Failure: {e}")
        return None

# --- [3. INTERFACE] ---
st.title("📟 TEST STAND v11.9")
st.write("Stripped to the core. Checking spark...")

if st.button("FIRE ENGINE"):
    with st.spinner("Cranking..."):
        # Test with the big two
        for symbol in ["NVTS", "BTC-USD"]:
            st.subheader(f"Results: {symbol}")
            data = get_data_manual(symbol)
            
            if data is not None:
                st.success(f"Connection Established for {symbol}")
                curr_price = data['Close'].iloc[-1]
                st.metric("Price", f"${curr_price:.2f}")
                st.line_chart(data['Close'].tail(30))
            else:
                st.warning(f"No data for {symbol}")

st.divider()
st.caption("Zero Dependencies | Logic Only | Hub: Galax")
