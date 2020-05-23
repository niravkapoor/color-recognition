import cv2
import math
from common_color import CommonColor
import sys
from detect_color import DetectColor
path = "img/" + sys.argv[1]
# print ('path', path)

# center = (w / 2, h / 2)
cl = CommonColor()
dt = DetectColor()

resize_img = cv2.imread(path)
resize_img = cv2.resize(resize_img, (559, 494))
(h, w) = resize_img.shape[:2]
print('height', h, w)
y1 = math.floor(h/2) - 150
y2 = math.floor(h/2) + 100
x1 = math.floor(w/2) - 100
x2 = math.floor(w/2) + 200
print('coordinates', y1, y2, x1, x2)
crop_img = resize_img[y1:y2, x1:x2]

cv2.imshow("cropped", crop_img)
cv2.imshow("resized", resize_img)
# it find the maximum color variant in the image, un comment it to find the color
# cl.find(crop_img)
dt.find(crop_img)
cv2.waitKey(0)