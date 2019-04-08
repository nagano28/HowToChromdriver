# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import bs4
import re
from time import sleep
import urllib

#5秒ごとに'UEC'に関する検索結果を表示
url="https://www.google.co.jp/search?q=UEC"

get_url_info = requests.get(url)
bs4Obj = bs4.BeautifulSoup(get_url_info.text, 'lxml')

for page_title in bs4Obj.select("h3.r a"):
    print(page_title.get_text())
    raw_page_url = page_title.get("href").replace("/url?q=", "")
    unquote_page_url = urllib.parse.unquote(raw_page_url)
    print(re.sub(r'&sa=.+', "", unquote_page_url))
    sleep(5)
