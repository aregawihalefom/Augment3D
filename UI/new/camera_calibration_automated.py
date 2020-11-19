import numpy as np
import cv2
import time
import os


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8, 3), np.float32)
objp[:, :2] = np.mgrid[0:6, 0:8].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
cal_images = []
cap = cv2.VideoCapture(2)

while True:
    # read image from camera
    while(cap.isOpened()):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ret, cap_img = cap.read()
    gray = cv2.cvtColor(cap_img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    print('detecting corner')
    retval, corners = cv2.findChessboardCorners(gray, (4, 6), None)

    # If found, add object points, image points (after refining them)
    if retval:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # if there is any corner detected
        if corners2.any():
            print("corner found")
            imgpoints.append(corners2)
            print('Drawing corner')

            # Draw and display the corners
            chess_dawn_img = cv2.drawChessboardCorners(cap_img, (4, 6), corners2, ret)
            cv2.imshow('img', chess_dawn_img)
            cv2.waitKey(500)
            time.sleep(2)
            cv2.destroyAllWindows()
            time.sleep(5)

            # save the image
            cal_images.append('cal_image_{}.png'.format(time.time_ns()))
            cv2.imwrite(os.path.join('calibration_images', cal_images[-1]), cap_img)

        # if we get enough points calibrate the camera else get more
        try:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
            img = cv2.imread('./new/calib_test.jpg')
            h,  w = img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

            # un-distort and then crop the image
            dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
            x,y,w,h = roi
            dst = dst[y:y+h, x:x+w]

            # show undistorted image
            cv2.imshow('undistorted pattern', dst)
            cv2.waitKey(0)
            cv2.imwrite('calibresult.png', dst)

            break

        # go get more points
        except Exception as e:
            print('number of object points: {} whereas number of image points:{}. they must be equal'.format(len(objpoints), len(imgpoints)))


