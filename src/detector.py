import cv2
import numpy as np

filename = '../assets/images/cheekboard.png'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.04)

num = np.int0(dst)
# result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst > 0.04 * dst.max()] = [0, 0, 255]

# === END METHOD 1 ==

# METHOD 2


# find the edges
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)
draw = gray.copy()
color = (255, 0, 0)
font = cv2.FONT_HERSHEY_SIMPLEX

# painiting the detected corners
for corner in corners:
    x,y = corner.ravel()
    cv2.putText(img, '*', (x,y), font, 1, color, 2, cv2.LINE_AA)

# This is general
vis = np.concatenate((img, draw), axis=1)
# This is the case
cv2.imshow('two', vis)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
