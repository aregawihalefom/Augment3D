import cv2
import numpy as np
import importlib
from LineDetector import LineDetector

if __name__ == '__main__':

    # read the image using opencv
    filename = '../assets/models/with_bordeaux_background.png'
    dim = (600, 600)
    img = cv2.resize(cv2.imread(filename), dim)
    copy_image = img

    # create line detector onbject
    detector = LineDetector(copy_image, "Line detector")

    # define
    edges, lines = detector.apply_line_detection()

    # display results
    cv2.imshow('Original Image', lines)
    cv2.imshow('From edge corner points', edges)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
