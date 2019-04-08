#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 00:44:37 2018

@author: nagano
"""
import cv2
import re
import os
import pandas as pd
#import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt

def getlist(path,num):
    files = os.listdir(path)
    re_files = os.listdir(path)
    return files, re_files,path
        
def imread(path,file):
        im_path = os.path.join(path, file)
        img = cv2.imread(im_path,cv2.IMREAD_COLOR)
        return img
    
def prepro(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray,(5,5),0)
    blur2 = cv2.medianBlur(blur1, ksize=5)
    retval, bw = cv2.threshold(blur2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return bw
        
def cut(bw):
    cut_img = bw[0:70,50:300]
    return cut_img

def hands(cut_img):
    n_gaso = 0
    for j in range(len(cut_img)):
        for k in range(len(cut_img[0])):
            if cut_img[j][k] == 0:
                n_gaso+=1
    return n_gaso

def rm_noise(cut_img):
    contours, hierarchy = cv2.findContours(cut_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    detect_count = 0

    y_max = []
    y_min = []
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])    
        # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
        if area < 100 or 5000 < area:
          continue
        # 外接矩形
        if len(contours[i]) > 0:
          rect = contours[i]
          x, y, w, h = cv2.boundingRect(rect)
          #cv2.rectangle(img2, (x-1, y-1), (x + w+1, y + h+1), (0, 255, 0), 2)
          y_min.append(y-1)
          y_max.append(y+h+1)
          # 外接矩形毎に画像を保存
          #cv2.imwrite('aa' + str(detect_count) + '.jpg', img2[y-1:y + h+1, x-1:x + w+1])
          detect_count = detect_count + 1
    y_min.sort()
    y_max.sort()
    
    rm_img = cut_img[y_min[0]:y_max[-1],0:250]
    return rm_img


#####################ここは，filenameから読み取る．
def post_number(save_path):
    name_files = os.listdir(save_path)
    for name in name_files:
        index = re.search('.png', name)      
        if index: #拡張子jpgならば
            print (name[-11:-4]) #str
            #print ('========================================')

#####################ここは，CNNの出力の数字列から郵便番号の検索をかける．
def number_search_csv(number):
    df = pd.read_csv('KEN_ALL_ROME.CSV', names=('A', 'B', 'C', 'D','E','F','G'),encoding='cp932')
    #print (df)
    aa = '1000001' #ここでCNNから帰ってきた文字列を入れる．
    a = list(df.query('A == "%s"'%aa).index)
    #print (a[0])
    b = []
    b.append(df.at[df.index[a[0]], 'B'])
    b.append(df.at[df.index[a[0]], 'C'])
    b.append(df.at[df.index[a[0]], 'D'])
    b = ''.join(b)
    print (b)
    return b

#####################ここは，送り先付近の営業所の検索を行う．
def search(b):
    driver = webdriver.Chrome('./chromedriver')

    # Googleのトップ画面を開く。
    driver.get('https://www.google.co.jp/')
    
    # タイトルに'Google'が含まれていることを確認する。
    assert 'Google' in driver.title
    print (b)
    # 検索語を入力して送信する。
    number=('大学 %s'%b) #str
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
    f = open('a.txt')
    areas = f.read().split('｜')
    print('送り先 : %s'%areas[0])
    f.close()


def main():
    for i in range(1,7):
        try:
               path = ('./segm/%s'%i)
               save_path = ('./save/%s'%i)
               files, re_files ,path = getlist(path,i)
               if i == 1:
                   re_files = [s.replace('東京', 'Tokyo') for s in re_files]
               elif i == 2:
                   re_files = [s.replace('東京', 'Aomori') for s in re_files]
               elif i == 3:
                   re_files = [s.replace('東京', 'Akita') for s in re_files]
               elif i == 5:
                   re_files = [s.replace('東京', 'Tottori') for s in re_files]
                   
               for k in range(len(files)):
                   img = imread(path,files[k])
                   bw = prepro(img)
                   cut_img = cut(bw)
                   p=5
                   if hands(cut_img) > len(cut_img)*len(cut_img[0])/100*p:
                       #print ("no hands")
                       rm_img = rm_noise(cut_img)
                       rm2_img = cv2.resize(rm_img, (250, 50))
                       plt.figure()
                       plt.imshow(rm2_img,cmap = 'gray')
                       cv2.imwrite("./save/%s/%s"%(i,re_files[k]),rm2_img)
                   else:
                       #print ('========================================')
                       #print ("hands")
                       cv2.imwrite("./save/ex/%s"%re_files[k],cut_img)
               post_number(save_path)
               
               #ここからはCNN後の処理
               number = post_number(save_path) #これ入れるなら"post_number(save_path)"除く．
               b = number_search_csv(number)
               search(b)
               
        except FileNotFoundError:
            print ("Not folder : %s"%i)
    plt.show()


if __name__ == "__main__":
    main()
