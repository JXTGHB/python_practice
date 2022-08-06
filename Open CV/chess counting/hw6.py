import cv2
import matplotlib.pyplot as plt
import numpy as np
cont = list()
j = 0
A = []
for i in range(2,5):
    ImgData = 'IMG_570'+str(i)+'.JPG'
    img = cv2.imread(ImgData)
    #print(img.shape)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    canny = cv2.Canny(blurred, 30, 150)

    ret, binary = cv2.threshold(canny,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(0,0,255),20)
    count = 0
    j += 1
    for cont in contours:
        ares = cv2.contourArea(cont)
        if ares<18 and ares>15:
            count += 1

    print("Total Chess :",count)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(
    #    img,
    #    'Detected Chess: ' + str(count),
    #    (10, 350),
    #    font,
    #    10,
    #    (0, 0xFF, 0xFF),
    #    10,
    #    cv2.FONT_HERSHEY_SIMPLEX,
    #    )
    #cv2.imshow('answer',img)
    cv2.imwrite('./outputIMG_570'+str(i)+'.JPG', img)

