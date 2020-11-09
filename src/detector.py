import cv2
import numpy as np

filename = '../assets/images/cheekboard.png'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.04)

# result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)

# copy image for method 1 and two
im1 = img.copy()
im2 = img.copy()

# Threshold for an optimal value, it may vary depending on the image.
im1[dst > 0.04 * dst.max()] = [0, 0, 255]

# === END METHOD 1 ==

# METHOD 2
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)

# paint the detected corners
color = (0, 0, 255)
font = cv2.FONT_HERSHEY_SIMPLEX

# Painiting the detected corners
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(im2, (x, y), 4, color, -1)

# Concatnate
vis = np.concatenate((im1, im2), axis=1)

# Table 1
filename = '../assets/images/table1.png'
table = cv2.imread(filename)
gray = cv2.cvtColor(table, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 150, 200)

# Table 2
filename = '../assets/images/table1.png'
table = cv2.imread(filename)
gray = cv2.cvtColor(table, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)

# paint the detected corners
color = (255, 0, 255)
font = cv2.FONT_HERSHEY_SIMPLEX

# Painiting the detected corners
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(gray, (x, y), 4, color, -1)

# show the image
cv2.imshow('two', gray)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
