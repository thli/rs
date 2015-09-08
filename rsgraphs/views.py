# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.template import Context
import logging
from plotly import tools
import plotly.plotly as py
from plotly.graph_objs import *
from rsgraphs.utils import *


import urllib
import requests
from bs4 import BeautifulSoup
import time
import datetime
import numpy as numpy

logger = logging.getLogger(__name__)

def index(request):
    context = {}
    return render_to_response('index.html', context_instance=Context(context))

def redirect_to_index(request):
    return redirect('rsgraphs/index')

def graph(request, item_name):
    context = {}

    url = build_url(item_name)
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, "html.parser")

    raw_data = soup.find_all('span', class_='st0')	
    string_data = map(stringify, raw_data)
    (dates,prices,volumes,EMA_9,MACD,HISTOGRAM) = build_data(string_data)

    # ## define plotly data
    # price_trace = Scatter(x=dates, y=prices, name='daily price',xaxis='x3',yaxis='y3',xsrc='thli:54:0876c4',ysrc='thli:54:fa5a05')
    # volume_trace = Bar(x=dates,y=volumes, name='volume',xaxis='x2',yaxis='y2',xsrc='thli:54:910217',ysrc='thli:54:bdbd9d')
    # macd_trace = Scatter(x=dates, y=MACD, name='macd',xsrc='thli:54:1d76c3',ysrc='thli:54:a9a9a2')
    # ema_trace = Scatter(x=dates, y=EMA_9, name='9-day EMA',xsrc='thli:54:1d76c3',ysrc='thli:54:2a9b5d')
    # histogram_trace = Bar(x=dates, y=HISTOGRAM, name='macd histogram',xsrc='thli:54:1d76c3',ysrc='thli:54:cfa3d1')

    # data = Data([price_trace,volume_trace,macd_trace,ema_trace,histogram_trace])

    # # define plotly layout
    # layout = Layout(
    #     autosize=True,
    #     xaxis=XAxis(domain=[0,1],type='linear',autorange=True),
    #     yaxis=YAxis(domain=[0,0.4],type='linear',autorange=True),
    #     xaxis2=XAxis(domain=[0,1],type='linear',autorange=True,anchor='y2'),
    #     yaxis2=YAxis(domain=[0.4,0.48],type='linear',autorange=True),
    #     xaxis3=XAxis(domain=[0,1],type='linear',autorange=True,anchor='y3'),
    #     yaxis3=YAxis(domain=[.5,1],type='linear',autorange=True)
    # )

    # define plotly data
    price_trace = Scatter(x=dates, y=prices, name='daily price',yaxis='y3')
    volume_trace = Bar(x=dates,y=volumes, name='volume',yaxis='y2')
    macd_trace = Scatter(x=dates, y=MACD, name='macd')
    ema_trace = Scatter(x=dates, y=EMA_9, name='9-day EMA')
    histogram_trace = Bar(x=dates, y=HISTOGRAM, name='macd histogram')

    data = Data([price_trace,volume_trace,macd_trace,ema_trace,histogram_trace])

    # define plotly layout
    layout = Layout(
        autosize=True,
        yaxis=YAxis(domain=[0,0.4]),
        yaxis2=YAxis(domain=[0.4,0.48]),
        yaxis3=YAxis(domain=[.5,1])
    )

    fig = Figure(data=data,layout=layout)

    unique_url = py.plot(fig, filename = item_name, auto_open = False)
    context['url'] = unique_url
    context['item_name'] = item_name

    return render_to_response('graph.html', context_instance=Context(context))