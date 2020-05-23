from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2
class ColorLabeler:
	def __init__(self):
		# initialize the colors dictionary, containing the color
		# name as the key and the RGB tuple as the value
		colors = OrderedDict({
			"red": (255, 0, 0),
			"annar_red": (240, 148, 144),
			"green": (0, 255, 0),
			"light_blue": (0, 141, 221),
			"yellow": (250,211,71),
			"blue": (0, 0, 255),
			"black_grapes": (29, 28, 36),
			"muskmelon": (157, 101, 21),
			"watermelon": (142, 40, 33),})
		# allocate memory for the L*a*b* image, then initialize
		# the color names list
		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.colorNames = []
		# loop over the colors dictionary
		for (i, (name, rgb)) in enumerate(colors.items()):
			# update the L*a*b* array and the color names list
			self.lab[i] = rgb
			self.colorNames.append(name)
		# convert the L*a*b* array from the RGB color space
		# to L*a*b*
		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)
	
	def unique_count_app(self):
		# a = cv2.imread("anaar.jpeg")
		colors_temp, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
		return colors_temp[count.argmax()]

	def bincount_app(self):
		# a = cv2.imread("anaar.jpeg")
		a2D = a.reshape(-1,a.shape[-1])
		col_range = (256, 256, 256) # generically : a2D.max(0)+1
		a1D = np.ravel_multi_index(a2D.T, col_range)
		return np.unravel_index(np.bincount(a1D).argmax(), col_range)

	def label(self, image, c, upload):
		# construct a mask for the contour, then compute the
		# average L*a*b* value for the masked region
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		mean = cv2.mean(image, mask=mask)[:3]
		# dominant = self.unique_count_app()
		# dominant2 = self.bincount_app()
		# print('dominant', dominant)
		# print('dominant2',dominant2)
		# initialize the minimum distance found thus far
		minDist = (np.inf, None)
		# loop over the known L*a*b* color values
		print('mean', mean)
		for (i, row) in enumerate(self.lab):
			# compute the distance between the current L*a*b*
			# color value and the mean of the image
			d = dist.euclidean(row[0], mean)
			# if the distance is smaller than the current distance,
			# then update the bookkeeping variable
			if d < minDist[0]:
				print(minDist[0], d, self.colorNames[i], mean)
				minDist = (d, i)
		# return the name of the color with the smallest distance
		return self.colorNames[minDist[1]]