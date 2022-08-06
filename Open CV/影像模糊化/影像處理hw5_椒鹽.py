import cv2 
import numpy as np
img=cv2.imread('yuang.jpg')
cv2.imshow('original',img)
#saltImage=saltpepper(img,0.02)
n=0.02
m=int((img.shape[0]*img.shape[1])*n)
for a in range(m):
    
    i=int(np.random.random()*img.shape[1])
    j=int(np.random.random()*img.shape[0])
    if img.ndim==2:
        img[j,i]=255
    elif img.ndim==3:
        img[j,i,0]=255
        img[j,i,1]=255
        img[j,i,2]=255
for b in range(m):
    i=int(np.random.random()*img.shape[1])
    j=int(np.random.random()*img.shape[0])
    if img.ndim==2:
        img[j,i]=0
    elif img.ndim==3:
        img[j,i,0]=0
        img[j,i,1]=0
        img[j,i,2]=0
cv2.imshow('saltImage',img)
cv2.imwrite('salt.jpg',img)
img_median = cv2.medianBlur(img, 5)
cv2.imshow('median',img_median)
cv2.waitKey(0)
cv2.destroyAllWindows()
