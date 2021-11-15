import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def Draw_candlestick(data):
    candlestick = go.Figure(data=go.Candlestick(x=data['time'],
                                                high=data['High'],
                                                open=data['Open'],
                                                low=data['Low'],
                                                close=data['Close']))
    candlestick.update_layout(xaxis_rangeslider_visible=False)
    return candlestick


def Draw_price(data):
    fig = px.line(data, x='time', y=['Open', 'Close'])
    return fig


def Draw_trend(data):
    fig = px.line(data, x='time', y=['High', 'Low'])
    return fig


def Draw_Volume(data):
    fig = px.line(data, x='time', y=['Volume'])
    return fig


def Draw_Deliverable_volume(data):
    fig = px.line(data, x='time', y=['Deliverable Volume'])
    return fig


def Draw_Intraday_pie(data):
    labels = ['Intraday Volume', 'Deliverable Volume']
    values = [data['Intraday Volume'].sum(), data['Deliverable Volume'].sum()]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig


def Draw_VWAP(data):
    fig = go.Figure(go.Scatter(x=data['time'],
                               y=data['VWAP']))
    fig.update_layout(title='VWAP over time')
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="VWAP")
    return fig


def Draw_multi_line_plot(data_object, names):
    # draw line charts
    fig = go.Figure()
    for i in range(len(data_object)):
        fig.add_traces(go.Scatter(x=data_object[i]['time'], y=data_object[i]['Close'], name=names[i], mode='lines'))
    return fig


def Draw_deliverables_pie(data_object, names):
    fig = go.Figure()
    deliverables = []  # store mean of deliverable volume
    for i in range(len(data_object)):
        deliverables.append(np.mean(data_object[i]['Deliverable Volume']))

    fig = go.Figure(data=[go.Pie(labels=names, values=deliverables)])
    return fig


def Draw_intraday_pie(data_object, names):
    fig = go.Figure()
    intraday_arr = []  # store mean of intraday volume
    for i in range(len(data_object)):
        intraday_arr.append(np.mean(data_object[i]['Intraday Volume']))
    fig = go.Figure(data=[go.Pie(labels=names, values=intraday_arr)])
    return fig



def Draw_vwap_pie(data_object, names):
    # vwap analysis
    fig = go.Figure()
    vwaps = []
    for i in range(len(data_object)):
        vwaps.append(np.mean(data_object[i]['VWAP']))

    fig = go.Figure(data=[go.Pie(labels=names, values=vwaps)])
    return fig