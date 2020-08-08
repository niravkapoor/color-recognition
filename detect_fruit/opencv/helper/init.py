import cv2
import math
from .common_color import CommonColor
import sys
from .detect_color import DetectColor

class InitDetect:
    def start(self, path, name, savePath):
        try:
            # center = (w / 2, h / 2)
            # cl = CommonColor()
            dt = DetectColor()
            # Read the image from the path
            resize_img = cv2.imread(path)
            
            resize_img = cv2.resize(resize_img, (559, 494))
            # get height and width of the image
            (h, w) = resize_img.shape[:2]
            print('height', h, w)
            y1 = math.floor(h/2) - 150
            y2 = math.floor(h/2) + 100
            x1 = math.floor(w/2) - 100
            x2 = math.floor(w/2) + 200
            print('coordinates', y1, y2, x1, x2)
            crop_img = resize_img[y1:y2, x1:x2]

            color = dt.find(crop_img, name, savePath)
            print('color on image', color)
            return color
        except Exception as ex:
            print('Exception in InitDetect', str(ex))