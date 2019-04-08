#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 00:29:58 2018

@author: nagano
"""

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
#import numpy as np

#options = Options()
# Chromeのパス（Stableチャネルで--headlessが使えるようになったら不要なはず）
#options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
#options.add_argument('--headless')
# ChromeのWebDriverオブジェクトを作成する。
driver = webdriver.Chrome('./chromedriver')

# Googleのトップ画面を開く。
driver.get('https://www.google.co.jp/')

# タイトルに'Google'が含まれていることを確認する。
assert 'Google' in driver.title

nn = 1820021
# 検索語を入力して送信する。
number=('大学〒%s'%nn) #str
input_element = driver.find_element_by_name('q')
input_element.send_keys('%s'%number)
input_element.send_keys(Keys.RETURN)

time.sleep(2)  # Chromeの場合はAjaxで遷移するので、とりあえず適当に2秒待つ。

# タイトルに'〒ooo-oooo'が含まれていることを確認する。
assert number in driver.title

# 検索結果を表示する。
for a in driver.find_elements_by_css_selector('h3 > a'):
    print(a.text)
    with open("a.txt", "w") as f:
        print(a.text, file=f)
    break
#print(a.get_attribute('href'))
    
driver.quit()  # ブラウザーを終了する。
