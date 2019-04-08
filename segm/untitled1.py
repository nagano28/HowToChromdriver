#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 00:44:37 2018

@author: nagano
"""
import cv2
import numpy as np

path = './'
for x in os.listdir(path): 
    

img = cv2.imread('201808261237000Tokyo00000000G1820021.png',cv2.IMREAD_COLOR)
img2 = img[0:70,50:300]
gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
retval, bw = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
p = 5
nn = 0
for j in range(0,70):
    for k in range(0,250):
        if bw[j][k] == 0:
            nn+=1

if nn > 70*250/100*p:
    image, contours, hierarchy = cv2.findContours(bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    detect_count = 0
    
    # 各輪郭に対する処理
    y_max = []
    y_min = []
    for i in range(0, len(contours)):
    
        # 輪郭の領域を計算
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
    
    img3 = img2[y_min[0]:y_max[-1],0:250]
    cv2.imwrite('./save/2018000000000東京000001820021.png',img3)
    
    cv2.imshow('output', img2)
    cv2.waitKey(0)
    cv2.imshow('output2', img3)
    cv2.waitKey(0)

else:
    print ("No post number ")
  # 外接矩形された画像を表示
#cv2.imshow('output', img2)
#cv2.waitKey(0)

  # 終了処理
#cv2.destroyAllWindows()
