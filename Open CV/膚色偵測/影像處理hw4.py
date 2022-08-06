import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
 

img = cv2.imread('SkinDetection.jpg')
ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
(y,cr,cb)= cv2.split(ycrcb)
 
answer = np.zeros(cr.shape,dtype= np.uint8)
(x,y)= cr.shape
for i in range(0,x):
     for j in range(0,y):
         if (cr[i][j]>135)and(cr[i][j]<180) and (cb[i][j]>85) and (cb[i][j])<135:
             answer[i][j]= 255
         else:
             answer[i][j] = 0
cv2.imshow('original',img)
cv2.imshow('SkinDetection',answer)

 
cv2.waitKey()
