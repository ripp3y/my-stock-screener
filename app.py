import streamlit as st
import pandas as pd
import yfinance as yf

# --- ENGINE ---
def color_shares(val, type_val):
    """Colors share counts based on buy/sell action."""
    color = '#4ADE80' if 'Buy' in str(type_val) else '#F87171'
    return f'color: {color}; font-weight: bold;'

# ... (Previous imports and data fetching logic remains same) ...

with t3:
    # 1. TOP-LEVEL OWNERSHIP PERCENTAGES
    st.subheader("Ownership Mix")
    try:
        # Fetching major holders and converting to a clean display
        holders = ticker_obj.major_holders
        if holders is not None:
            # We want to extract the % values specifically
            # Typically yfinance returns: [Value, Description]
            inst_own = holders.iloc[1, 0] # % Held by Institutions
            insid_own = holders.iloc[0, 0] # % Held by Insiders
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Institutional", f"{inst_own:.1%}" if isinstance(inst_own, float) else inst_own)
            c2.metric("Insider", f"{insid_own:.1%}" if isinstance(insid_own, float) else insid_own)
            c3.metric("Float", "Public", help="Remaining shares available to retail.")
    except:
        st.info("Ownership percentages loading...")

    st.divider()

    # 2. SIMPLIFIED INSIDER ACTIVITY (FORM 4)
    st.subheader("Insider Intel (Form 4)")
    try:
        trades = ticker_obj.insider_transactions
        if trades is not None and not trades.empty:
            # 1. Clean the data
            df_trades = trades[['Start Date', 'Insider', 'Transaction', 'Shares']].copy()
            df_trades['Shares'] = df_trades['Shares'].apply(lambda x: f"{x:,}") # Add commas
            
            # 2. Display with conditional logic
            # We show the Transaction type and the Shares as the main focus
            st.dataframe(
                df_trades.head(15),
                column_config={
                    "Start Date": "Date",
                    "Transaction": st.column_config.TextColumn("Action"),
                    "Shares": st.column_config.TextColumn("Units")
                },
                hide_index=True,
                use_container_width=True
            )
            
            st.caption("🟢 Green = Potential Conviction Buy | 🔴 Red = Executive Distribution")
        else:
            st.write("No major moves reported recently.")
    except:
        st.warning("SEC Form 4 feed currently offline.")

    # 3. TOP INSTITUTIONS (The Anchors)
    with st.expander("View Top 5 Institutional Anchors"):
        try:
            inst = ticker_obj.institutional_holders.head(5)
            st.table(inst[['Holder', 'Shares']])
        except:
            st.write("Data unavailable.")
