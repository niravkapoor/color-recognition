from .colorlabeler import ColorLabeler
import argparse
import imutils
import cv2
import sys

class DetectColor:

	def find(self, image, imgName, savePath):
		resized = imutils.resize(image, width=300)
		# blur the resized image slightly, then convert it to both
		# grayscale and the L*a*b* color spaces
		blurred = cv2.GaussianBlur(resized, (5, 5), 0)
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		# find contours in the thresholded image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		# initialize the shape detector and color labeler
		# sd = ShapeDetector()
		cl = ColorLabeler()

		# loop over the contours
		for c in cnts:
			# detect the shape of the contour and label the color
			# shape = sd.detect(c)
			color = cl.label(lab, c, image)
			return color