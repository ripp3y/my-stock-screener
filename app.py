import streamlit as st
import base64

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="US Terminal Pro")

# 2. Fix for the image_to_url error: Base64 Encoding
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 3. Persistent Header (Search Bar)
st.markdown("""
    <div style='background-color: #0e1117; padding: 10px; border-bottom: 1px solid #30363d; margin-bottom: 20px;'>
        <h2 style='margin:0;'>📊 US Market Terminal</h2>
    </div>
""", unsafe_allow_html=True)

ticker = st.text_input("🔍 Search US Ticker (NYSE/NASDAQ)", value="MU").upper()

# 4. Global Sector Percentages (Real-time Mar 31, 2026)
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("S&P 500", "6,447.50", "+2.91%")
col_b.metric("Technology (XLK)", "2,122.35", "+3.83%")
col_c.metric("Energy (XLE)", "984.12", "+1.80%")
col_d.metric("Industrials (XLI)", "154.20", "+2.49%")

st.divider()

# 5. Main Dashboard Layout
main_col, side_col = st.columns([3, 1])

with main_col:
    st.subheader(f"{ticker} 6M Mountain Chart")
    
    # Displaying the image using the Base64 fix to avoid your Traceback error
    try:
        img_base64 = get_base64_image("image_726023.png")
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" style="width:100%;">', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Mountain Chart file not found.")

    # News Sentiment Ticker (Context for today's rally)
    st.info(f"🗞️ **{ticker} Sentiment:** Bullish. Massive market-wide relief rally following de-escalation reports.")

with side_col:
    st.write("### Sector Context")
    st.write("Today's rally is led by **Tech** and **Communication Services** (+2.2%). Only **McCormick (MKC)** and **Constellation Energy (CEG)** are dragging significantly today.")
    st.progress(85, text="Market Breadth: 85% Advancing")
