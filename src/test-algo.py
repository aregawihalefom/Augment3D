import cv2
import numpy as np
import importlib
from Algorithm import mainAlgorithm

if __name__ == '__main__':

    filename = '../assets/models/computer_grid.png'
    dim = (600, 600)
    img = cv2.resize(cv2.imread(filename), dim)

    # prepare main algorithm
    tool = mainAlgorithm(img, desc="Main algorithm")

    blue_channel = tool.based_on_green_channel()
    # display results
    cv2.imshow('Original Image', img)
    cv2.imshow('From edge corner points', blue_channel)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
