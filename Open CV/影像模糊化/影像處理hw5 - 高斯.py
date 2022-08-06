import cv2
import numpy as np
def correct(value):
    if value > 255:
        return 255
    elif value < 0:
        return 0
    else:
        return value
img = cv2.imread('yuang.jpg')
cv2.imshow('original',img)
image = img
h, w, c = image.shape
for row in range(h):
    for col in range(w):
        s = np.random.normal(0, 20, 3)#均質，標準差，數量
        blue = image[row, col, 0]  
        green = image[row, col, 1]  
        red = image[row, col, 2]  
        image[row, col, 0] = correct(blue + s[0])
        image[row, col, 1] = correct(green + s[1])
        image[row, col, 2] = correct(red + s[2])

cv2.imwrite('Gauss.jpg',image)
cv2.imshow('Gaussian', image)
img_median = cv2.GaussianBlur(image, (3, 3), 0)
#img_median =cv2.medianBlur(image, 5)
cv2.imshow('clear', img_median)
cv2.waitKey(0)
cv2.destroyAllWindows()
