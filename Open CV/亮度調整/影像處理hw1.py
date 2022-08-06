import cv2
import numpy as np

#img= cv2.imread('gray.jpg') #灰階圖片
img= cv2.imread('frog.jpg')
change=int(input("輸入你想改變的值:"))
row=img.shape[0]
col=img.shape[1]
ch=img.shape[2]
#color=int(img[100,100,0])
if(ch==3):
    for i in range(row):
        for j in range(col):
            for n in range(ch): 
                color=int(img[i,j,n])
                if color+change>255:
                    img.itemset((i,j,n), 255)
                elif color+change<0:
                    img.itemset((i,j,n), 0)
                else:
                    img.itemset((i,j,n), color+change)
elif(ch==1):
    for i in range(row):
        for j in range(col): 
                color=int(img[i,j])
                if color+change>255:
                    img.itemset((i,j), 255)
                elif color+change<0:
                    img.itemset((i,j), 0)
                else:
                    img.itemset((i,j), color+change)
    
cv2.imshow('My Image', img)
cv2.imwrite('output.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(img[100,100,0])
