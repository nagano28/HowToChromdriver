#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 00:13:21 2018

@author: nagano
"""

from urllib.parse import parse_qsl
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests import get as GET

#'='の後を書き換える、例でUEC
html = GET("https://www.google.co.jp/search?q=UEC").text
bs = BeautifulSoup(html, 'lxml')

for el in bs.select("h3.r a"):
    title = el.get_text()
    url = dict(parse_qsl(urlparse(el.get("href")).query))["q"]
    print(title)
    print("  ", url)
