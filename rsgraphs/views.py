from django.shortcuts import render, render_to_response, redirect
from django.template import Context
import plotly.plotly as py
from plotly.graph_objs import Scatter

import urllib
import requests
from bs4 import BeautifulSoup
import time
import datetime
import numpy as numpy

def index(request):
	context = {}
	return render_to_response('index.html', context_instance=Context(context))

def redirect_to_index(request):
    return redirect('rsgraphs/index')

def graph(request, item_name):
	context = {}
	
	trace0 = Scatter(x=[1, 2, 3, 4],
	    y=[10, 15, 13, 17]
	)
	trace1 = Scatter(
	    x=[1, 2, 3, 4],
	    y=[16, 5, 11, 9]
	)
	data = [trace0, trace1]

	unique_url = py.plot(data, filename = 'basic-line', auto_open = False)
	context['url'] = unique_url

	return render_to_response('graph.html', context_instance=Context(context))
    # url = build_url(item_name)
    # r = requests.get(url) 
    # soup = BeautifulSoup(r.content, "html.parser")
    # try:
    #     raw_data = soup.find_all('span', class_='st0')
    #     string_data = map(stringify, raw_data)
    #     (dates,prices,volumes,EMA_9,MACD,HISTOGRAM) = build_data(string_data)
    #     data = zip(*[dates,prices,volumes,EMA_9,MACD,HISTOGRAM])
    # except:
    #     print item_name