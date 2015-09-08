import urllib
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import datetime
import csv
import multiprocessing
import numpy as np
from multiprocessing import Pool

BASE_URL = 'http://runescape.wikia.com/wiki/Module:Exchange/%s/Data'

def build_url(item_name):
    return BASE_URL % item_name.rstrip()

def unix2date(unix_date):
    date = datetime.datetime.fromtimestamp(unix_date).strftime('%Y-%m-%d')
    return date

def stringify(raw_data):
    return raw_data.string

################  Analytical Functions  ###################
def EMA(prices, days):
    weights = np.exp(np.linspace(-1.,0.,days))
    weights += 1
    weights /= weights.sum()

    a = np.convolve(prices,weights)[:len(prices)]
    a[:days] = a[days]

    return a
###########################################################


# build_data: parses the raw_data scraped from the web and returns
# the following lists of data:
# dates, prices, volumes, MACD line, 9-day EMA signal line

def build_data(raw_data):
    dates = []
    prices = []
    volumes = []

    for datapoint in raw_data:
        m = re.match("'(?P<unix_date>\d+):(?P<price>\d+(\.\d+)?)(:(?P<volume>\d+\.\d+))?'", datapoint)

        unix_date = m.group('unix_date')
        date = str(unix2date(int(unix_date)))
        price = int(m.group('price'))
        volume = m.group('volume')
        if volume is None:
            volume = 0

        dates.append(date)
        prices.append(price)
        volumes.append(volume)

    EMA_12 = EMA(prices, 12)
    EMA_26 = EMA(prices, 26)
    MACD = (EMA_12 - EMA_26).tolist()
    SIGNAL = EMA(MACD, 9).tolist()
    HISTOGRAM = (np.array(MACD) - np.array(SIGNAL)).tolist()

    return (dates,prices,volumes,SIGNAL,MACD,HISTOGRAM)