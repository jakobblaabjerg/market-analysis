import altair as alt
import plotly.express as px
import streamlit as st

from src.utils import load_data_from_yf, transform_data, compute_indicators, filter_data
from src.visualizations import candlestick_plot
from src.enums import Ticker

st.set_page_config(
    page_title="Market Analysis",
    layout="wide",
    initial_sidebar_state="expanded")

alt.theme.enable("dark")



with st.sidebar:
    selected_ticker = st.selectbox(
        'Select a ticker',
        list(Ticker),
        format_func=lambda ticker: ticker.name  # show the enum name
    )


    # Resolution selectbox example
    selected_resolution = st.selectbox(
        'Select resolution',
        options=['d', 'm', 'y'],
        format_func=lambda x: {'d': 'Daily', 'm': 'Monthly', 'y': 'Yearly'}[x]
    )


    selected_n_days = st.slider(
        'Select number of days',
        min_value=20,
        max_value=365*3,
        value=365,  # default 1 year
        step=1
    )

data = load_data_from_yf(ticker=selected_ticker.value, last_n_days=1400)
data = transform_data(data, selected_resolution)
data = compute_indicators(data)
data = filter_data(data, selected_n_days, selected_resolution)
candlestick_plot(data, ticker=selected_ticker.value, indicators=["SMA_200", "EMA_8"])