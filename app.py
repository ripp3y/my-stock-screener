# --- Updated Section 3: DIRECTIONAL ANALYSIS & VOLUME ---
if selected_ticker:
    df = data[selected_ticker].dropna()
    rsi_s, ema_9_s, _, _ = get_technical_signals(df)
    
    # 3-Level Layout: 1. Price/EMA (50%), 2. RSI (20%), 3. Volume (30%)
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.04, 
                        row_heights=[0.5, 0.2, 0.3])

    # A. Candlesticks (Direction)
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
    # 9-Day EMA (The Floor)
    fig.add_trace(go.Scatter(x=df.index, y=ema_9_s, line=dict(color='orange', width=2), name="9-EMA"), row=1, col=1)

    # B. RSI (The Purple Momentum Line)
    fig.add_trace(go.Scatter(x=df.index, y=rsi_s, line=dict(color='#A020F0', width=2), name="RSI"), row=2, col=1)
    
    # ADDED: Small Font Label for the Purple Line
    fig.add_annotation(xref="paper", yref="paper", x=0.02, y=0.42,
                       text="<span style='font-size:10px; color:#A020F0;'>PURPLE LINE: RSI (MOMENTUM)</span>",
                       showarrow=False)

    # RSI Overbought/Oversold Thresholds
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="lime", row=2, col=1)

    # C. Volume Bars
    vol_colors = ['#26a69a' if c >= o else '#ef5350' for o, c in zip(df['Open'], df['Close'])]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vol_colors, name="Volume"), row=3, col=1)

    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=850, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
