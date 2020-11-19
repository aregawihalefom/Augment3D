import numpy as np
import cv2
from tqdm import trange, tqdm
import os
import time


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8, 3), np.float32)
objp[:, :2] = np.mgrid[0:6, 0:8].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# get all captured chessboard images path
path = os.path.abspath('../../assets/images/checkerboard_captured/')
os.chdir(path)
images = os.listdir(path)
images = [os.path.join(path, im_name) for im_name in images]

# iterate through all the images
images_bar = tqdm(images)
for file_name in images_bar:
    img = cv2.imread(file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (4, 6), None)
    images_bar.set_description('detected corners {}'.format(ret))

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        if corners2.any():
            images_bar.set_description("corner found")
        imgpoints.append(corners2)
        time.sleep(5)
        images_bar.set_description('drawing corners on the chessboard')

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (4, 6), corners2, ret)
    #     cv2.imshow('img', img)
    #     cv2.waitKey(500)
    #
    # cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
img = cv2.imread('./new/calib_test.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult.png', dst)
