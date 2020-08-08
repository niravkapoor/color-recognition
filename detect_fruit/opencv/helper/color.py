import cv2 
import numpy as np  
  
img1 = cv2.imread('blue_sky.jpeg')
     

# blurred = cv2.GaussianBlur(img1, (5, 5), 0)
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV) 
print(hsv)
print(img1)
lower_red = np.array([110,50,50]) 
upper_red = np.array([202,99,87]) 
  
# Here we are defining range of bluecolor in HSV 
# This creates a mask of blue coloured  
# objects found in the frame. 
mask = cv2.inRange(hsv, lower_red, upper_red) 
print(mask)
# The bitwise and of the frame and mask is done so  
# that only the blue coloured objects are highlighted  
# and stored in res 
res = cv2.bitwise_and(img1,img1, mask= mask) 
cv2.imshow('frame',img1) 
cv2.imshow('mask',mask) 
cv2.imshow('res',res) 
  
cv2.waitKey(0)
cv2.destroyAllWindows()