import pandas as pd 
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

@st.cache_data
def load_data_from_yf(ticker: str, last_n_days: int) -> pd.DataFrame:

    start = datetime.datetime.today() - datetime.timedelta(days=last_n_days)
    return yf.download(tickers=ticker, start=start, auto_adjust=True)



def transform_data(data: pd.DataFrame, resolution: str = "d"):
    
    
    if resolution.lower() not in ["d", "m", "y"]:
        raise ValueError("resolution can either be daily = 'd', monthly = 'm' or yearly = 'y'")

    data = data.reset_index()
    data.columns = data.columns.get_level_values(0)
    data = data[['Date', 'Open', 'Close', 'High', 'Low', 'Volume']]
    data.columns.name = None

    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data = data.sort_values('Date')


    if resolution.lower() == "m":
        data = data.groupby(['Year', 'Month'])
        data = data.agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'mean'
            }).reset_index()
        data['Date'] = pd.to_datetime(dict(year=data['Year'], month=data['Month'], day=1))

    elif resolution.lower() == "y":
        data = data.groupby(['Year'])
        data = data.agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'mean'
            }).reset_index()
        data['Date'] = pd.to_datetime(dict(year=data['Year'], month=1, day=1))

    data['Change'] = data['Close']-data['Open']
    data['Color'] = np.where(data['Close'] >= data['Open'], 'Green', 'Red')
    data['ShadowUpper'] = np.where(data['Color'] == 'Green', data['High']-data['Close'], data['High']-data['Open'])
    data['ShadowUpperBottom'] = np.where(data['Color'] == 'Green', data['Close'], data['Open'])
    data['ShadowLower'] = np.where(data['Color'] == 'Green', data['Open']-data['Low'], data['Close']-data['Low'])
    data['ShadowLowerBottom'] = data['Low']
    data['Return'] = (data['Close']-data['Open'])/data['Open']

    return data


def candlestick_plot(data, ticker, indicators):

    body_width = 0.6
    shadow_width = 0.1

    plt.figure(figsize=[12,8])
    plt.bar(data.index, data['Change'], body_width, bottom=data['Open'], color=data['Color'])
    plt.bar(data.index, data['ShadowUpper'], shadow_width, bottom=data['ShadowUpperBottom'], color=data['Color'])
    plt.bar(data.index, data['ShadowLower'], shadow_width, bottom=data['ShadowLowerBottom'], color=data['Color'])

    for ind in indicators:
        plt.plot(data.index, data[ind], label=ind)
    
    plt.ylabel('Price')
    plt.xlabel('Time')
    plt.title(f'ticker={ticker}')
    plt.tight_layout()
    plt.show()

    return None


def return_distribution_plot(data, ticker):

    returns = data['Return'].dropna()
    mean = returns.mean()
    std = returns.std()

    plt.figure(figsize=(10, 6))
    plt.hist(returns, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    
    for i in range(-3, 4):
        plt.axvline(mean + i * std, color='red' if i else 'black',
                    linestyle='--' if i else '-', linewidth=1.5)

    plt.title(f'Return Distribution for {ticker}')
    plt.xlabel('Return')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    return None


def compute_candlestick_formations(data):
    pass




def filter_data(data, last_n_days, resolution):

    if resolution == "d":
        return data.tail(last_n_days)
    
    elif resolution == "m":
        return data.tail(int(last_n_days/30))
    
    elif resolution == "y":
        return data.tail(int(last_n_days/365))


def compute_indicators(data: pd.DataFrame, indicator: list = None):

    available_indicators = {
        'SMA_200': lambda data: data['Close'].rolling(window=200).mean(),
        'EMA_8': lambda data: data['Close'].ewm(span=8, adjust=False).mean()
    }

    if indicator is None:
        indicator = list(available_indicators.keys())

    for ind in indicator:
        if ind in available_indicators:
            data[ind] = available_indicators[ind](data)
        else:
            raise ValueError(f"Unknown indicator: {ind}")

    return data






    # data['Body'] = abs(data['Close']-data['Open'])
    # data['Total'] = data['Body'] + data['ShadowLower'] + data['ShadowUpper']
    # data['BodyPct'] = data['Body'] / data['Total']
    # data['ShadowUpperPct'] = data['ShadowUpper'] / data['Total']
    # data['ShadowLowerPct'] = data['ShadowLower'] / data['Total']
    # data['PrevOpen'] = data['Open'].shift(1)
    # data['PrevClose'] = data['Close'].shift(1)
    # data['PrevHigh'] = data['High'].shift(1)
    # data['PrevLow'] = data['Low'].shift(1)
    # data['PrevBody'] = abs(data['PrevClose']-data['PrevOpen'])
    # data['PrevColor'] = data['Color'].shift(1)
    # data['PrevShadowUpper'] = np.where(data['PrevColor'] == 'Green', data['PrevHigh']-data['PrevClose'], data['PrevHigh']-data['PrevOpen'])
    # data['PrevShadowLower'] = np.where(data['PrevColor'] == 'Green', data['PrevOpen']-data['PrevLow'], data['PrevClose']-data['PrevLow'])
    # data['PrevTotal'] = data['PrevBody'] + data['PrevShadowLower'] + data['PrevShadowUpper']
    # data['PrevBodyPct'] = data['PrevBody'] / data['PrevTotal']
    # data['Prev2High'] = data['High'].shift(2)
    # data['Prev2Low'] = data['Low'].shift(2)
    # data['Prev2Open'] = data['Open'].shift(2)
    # data['Prev2Close'] = data['Close'].shift(2)
    # data['Prev2Color'] = data['Color'].shift(2)
    # data['Prev2Body'] = abs(data['Prev2Close']-data['Prev2Open'])
    # data['Prev2ShadowUpper'] = np.where(data['Prev2Color'] == 'Green', data['Prev2High']-data['Prev2Close'], data['Prev2High']-data['Prev2Open'])
    # data['Prev2ShadowLower'] = np.where(data['Prev2Color'] == 'Green', data['Prev2Open']-data['Prev2Low'], data['Prev2Close']-data['Prev2Low'])
    # data['Prev2Total'] = data['Prev2Body'] + data['Prev2ShadowLower'] + data['Prev2ShadowUpper']
    # data['Prev2BodyPct'] = data['Prev2Body'] / data['Prev2Total']
    # data['Prev3High'] = data['High'].shift(3)
    # data['Prev3Low'] = data['Low'].shift(3)
    # data['Prev3Open'] = data['Open'].shift(3)
    # data['Prev3Close'] = data['Close'].shift(3)
    # data['Prev3Color'] = data['Color'].shift(3)
    # data['Prev3Body'] = abs(data['Prev3Close']-data['Prev3Open'])
    # data['Prev3ShadowUpper'] = np.where(data['Prev3Color'] == 'Green', data['Prev3High']-data['Prev3Close'], data['Prev3High']-data['Prev3Open'])
    # data['Prev3ShadowLower'] = np.where(data['Prev3Color'] == 'Green', data['Prev3Open']-data['Prev3Low'], data['Prev3Close']-data['Prev3Low'])
    # data['Prev3Total'] = data['Prev3Body'] + data['Prev3ShadowLower'] + data['Prev3ShadowUpper']
    # data['Prev3BodyPct'] = data['Prev3Body'] / data['Prev3Total']
    # data['Prev4High'] = data['High'].shift(4)
    # data['Prev4Low'] = data['Low'].shift(4)
    # data['Prev4Open'] = data['Open'].shift(4)
    # data['Prev4Close'] = data['Close'].shift(4)
    # data['Prev4Color'] = data['Color'].shift(4)
    # data['Prev4Body'] = abs(data['Prev4Close']-data['Prev4Open'])
    # data['Prev4ShadowUpper'] = np.where(data['Prev4Color'] == 'Green', data['Prev4High']-data['Prev4Close'], data['Prev4High']-data['Prev4Open'])
    # data['Prev4ShadowLower'] = np.where(data['Prev4Color'] == 'Green', data['Prev4Open']-data['Prev4Low'], data['Prev4Close']-data['Prev4Low'])
    # data['Prev4Total'] = data['Prev4Body'] + data['Prev4ShadowLower'] + data['Prev4ShadowUpper']
    # data['Prev4BodyPct'] = data['Prev4Body'] / data['Prev4Total']
    # data['Hammer/HangingMan'] = np.where((data['ShadowLowerPct']>= 2*data['BodyPct']) & (data['BodyPct']>= 0.2), 1, 0)
    # data['InvertedHammer/ShootingStar'] = np.where((data['ShadowUpperPct']>= 2*data['BodyPct']) & (data['BodyPct']>= 0.2), 1, 0)
    # data['BullishEngulfing'] = np.where((data['Color'] == 'Green') & (data['PrevColor'] == 'Red') & (data['Open'] < data['PrevClose']) & (data['Close'] > data['PrevOpen']), 1, 0)
    # data['PiercingLine'] = np.where((data['PrevColor'] == 'Red') & (data['Color'] == 'Green') & (data['ShadowLowerPct']> 0) & (data['Open']< data['PrevClose']) & (data['Close']> (data['PrevOpen']-data['PrevClose'])/2+data['PrevClose']), 1, 0)
    # data['MorningStar'] = np.where((data['Prev2Color']=='Red') & (data['Color'] == 'Green') & (data['Prev2Body'] > data['PrevBody']*2) &  (data['Body']> data['PrevBody']*2) & (data['PrevBodyPct']<0.3), 1 ,0)
    # data['WhiteSoldiers'] = np.where((data['Prev2BodyPct']>0.5) & (data['PrevBodyPct']>0.5) & (data['BodyPct']>0.5) & (data['Prev2Color'] == 'Green') & (data['PrevColor'] == 'Green') & (data['Color'] == 'Green') & (data['PrevOpen'] > data['Prev2Open']) & (data['PrevClose'] > data['Prev2Close']) & (data['Open'] > data['PrevOpen']) & (data['Close'] > data['PrevClose']), 1, 0)
    # data['BearishEngulfing'] = np.where((data['Color'] == 'Red') & (data['PrevColor'] == 'Green') & (data['Open'] > data['PrevClose']) & (data['Close'] < data['PrevOpen']), 1, 0)
    # data['EveningStar'] = np.where((data['Prev2Color']=='Green') & (data['Color'] == 'Red') & (data['Prev2Body'] > data['PrevBody']*2) &  (data['Body']> data['PrevBody']*2) & (data['PrevBodyPct']<0.3), 1 ,0)
    # data['BlackCrows'] = np.where((data['Prev2BodyPct']>0.5) & (data['PrevBodyPct']>0.5) & (data['BodyPct']>0.5) & (data['Prev2Color'] == 'Red') & (data['PrevColor'] == 'Red') & (data['Color'] == 'Red') & (data['PrevOpen'] < data['Prev2Open']) & (data['PrevClose'] < data['Prev2Close']) & (data['Open'] < data['PrevOpen']) & (data['Close'] < data['PrevClose']), 1, 0)
    # data['DarkCloudCover'] = np.where((data['PrevColor'] == 'Green') & (data['Color'] == 'Red') & (data['Open'] > data['PrevClose']) & (data['Close']< (data['PrevClose']-data['PrevOpen'])/2+data['PrevOpen']), 1, 0)
    # data['Doji'] = np.where((data['BodyPct']< 0.03), 1, 0)
    # data['SpinningTop'] = np.where((data['ShadowLowerPct']>0.35) & (data['ShadowUpperPct']>0.35), 1, 0)
    # data['FallingThree'] = np.where((data['Prev4BodyPct']> 0.8) & (data['Prev4Color'] == 'Red') & (data['Prev3Color'] == 'Green') & (data['Prev3Close'] < data['Prev4Open']) & (data['Prev3Close'] < data['Open']) & (data['Prev3Open'] > data['Prev4Close']) & (data['Prev3Open'] > data['Close']) & (data['Prev2Color'] == 'Green') & (data['Prev2Close'] < data['Prev4Open']) & (data['Prev2Close'] < data['Open']) & (data['Prev2Open'] > data['Prev4Close']) & (data['Prev2Open'] > data['Close']) & (data['PrevColor'] == 'Green') & (data['PrevClose'] < data['Prev4Open']) & (data['PrevClose'] < data['Open']) & (data['PrevOpen'] > data['Prev4Close']) & (data['PrevOpen'] > data['Close']) & (data['BodyPct']> 0.8) & (data['Color'] == 'Red'), 1, 0)
    # data['RissingThree'] = np.where((data['Prev4BodyPct']> 0.8) & (data['Prev4Color'] == 'Green') & (data['Prev3Color'] == 'Red') & (data['Prev3Open'] < data['Prev4Close']) & (data['Prev3Open'] < data['Close']) & (data['Prev3Close'] > data['Prev4Open']) & (data['Prev3Close'] > data['Open']) & (data['Prev2Color'] == 'Red') & (data['Prev2Open'] < data['Prev4Close']) & (data['Prev2Open'] < data['Close']) & (data['Prev2Close'] > data['Prev4Open']) & (data['Prev2Close'] > data['Open']) & (data['PrevColor'] == 'Red') & (data['PrevOpen'] < data['Prev4Close']) & (data['PrevOpen'] < data['Close']) & (data['PrevClose'] > data['Prev4Open']) & (data['PrevClose'] > data['Open']) & (data['BodyPct']> 0.8) & (data['Color'] == 'Green'), 1, 0)
    # return data
































# # number of days.

# backwards


# index = {index: "c25", "tickers":['MAERSK-B.CO' , 'AMBU-B.CO', 'BAVA.CO', 'CARL-B.CO', 'COLO-B.CO', 'DANSKE.CO', 'DEMANT.CO', 'DSV.CO', 'GMAB.CO', 'GN.CO', 'ISS.CO', 'JYSK.CO' , 'NKT.CO', 'NOVO-B.CO', 'NSIS-B.CO', 'PNDORA.CO', 'ROCK-B.CO', 'RBREW.CO', 'SYDB.CO', 'TRYG.CO', 'VWS.CO', 'ZEAL.CO' ,'ORSTED.CO'] }