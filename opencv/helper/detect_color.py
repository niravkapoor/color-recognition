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
		cl = ColorLabeler()
		color = cl.label(lab, image)
		return color