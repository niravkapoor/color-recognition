import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('orange-1.jpeg',0)          # queryImage
img2 = cv2.imread('apple-1.jpeg',0) # trainImag
#sift = cv2.SIFT()
sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()

kp1, des1 = surf.detectAndCompute(img1,None)
kp2, des2 = surf.detectAndCompute(img2,None)

orb = cv2.ORB_create()
kpOrb, desOrb = orb.detectAndCompute(img1, None)


keypoints_surf, descriptors = surf.detectAndCompute(img1, None)

img = cv2.drawKeypoints(img1, kp1, None)
imgSurf = cv2.drawKeypoints(img1, keypoints_surf, None)
imgOrb = cv2.drawKeypoints(img1, kpOrb, None)
# cv2.imshow("Image", img)
# cv2.imshow("Image 2", imgSurf)
# cv2.imshow("Image Orb", imgOrb)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
count = 0
for m,n in matches:
    if m.distance < 0.75*n.distance:
        print(m.distance, n.distance)
        good.append([m])
        count += 1
        # if count == 5:
            # print(m,n)
            # break

print (len(good))
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=22)

plt.imshow(img3),plt.show()
