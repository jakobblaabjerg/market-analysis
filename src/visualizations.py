import plotly.graph_objects as go
import streamlit as st
import numpy as np

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


def return_distribution_plot(data, ticker):
    returns = data['Return'].dropna()
    mean = returns.mean()
    std = returns.std()

    hist = go.Histogram(
        x=returns,
        nbinsx=50,
        marker_color='skyblue',
        opacity=0.75,
        name='Returns'
    )

    lines = []
    for i in range(-3, 4):
        line_color = 'red'
        line_style = 'solid' if i == 0 else 'dash'
        lines.append(
            go.Scatter(
                x=[mean + i * std, mean + i * std],
                y=[0, max(np.histogram(returns, bins=50)[0])],
                mode='lines',
                line=dict(color=line_color, dash=line_style, width=1.5),
                showlegend=False
            )
        )

    fig = go.Figure(data=[hist] + lines)

    fig.update_layout(
        xaxis_title='Return',
        yaxis_title='Frequency',
        bargap=0.05,
        template='plotly_white'
    )

    st.plotly_chart(fig)


    # ratio between 
    # sharp ratio 