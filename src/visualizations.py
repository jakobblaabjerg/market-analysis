import plotly.graph_objects as go
import streamlit as st

def candlestick_plot(data, ticker, indicators):

    dates_str = data['Date'].dt.strftime('%Y-%m-%d').tolist()
    tick_step = 10
    tickvals = dates_str[::tick_step]
    ticktext = dates_str[::tick_step]

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=dates_str,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ))

    # Add indicators
    for ind in indicators:
        fig.add_trace(go.Scatter(
            x=dates_str,
            y=data[ind],
            mode='lines',
            name=ind
        ))


    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        xaxis=dict(
            type='category',
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext,
            tickangle=45,  # Rotate labels for readability
            tickfont=dict(size=10)
        ),
        height=600,
        dragmode="zoom"
    )

    st.plotly_chart(fig, use_container_width=True)