import numpy as np
import cv2
import math


class LineDetector:
    """
    This class applies different mechanisms to detect lines in an image

    """

    def __init__(self, input_image, desc=None):
        self.desc = desc
        self.input_image = None
        self.output_image = None
        print("Line detector initalized")

    def get_only_one_color(self, input_image):

        hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

        # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
        mask = cv2.inRange(hsv, (30, 10, 0), (80, 255, 255))

        ## slice the green
        imask = mask > 0
        green = np.zeros_like(input_image, np.uint8)
        green[imask] = input_image[imask]

        return green

    def auto_canny(self, image, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        # return the edged image
        return edged

    def apply_line_detection(self, input_image):

        # Input image
        self.input_image = input_image
        self.output_image = input_image

        # apply edge detection
        low_threshold = 50
        high_threshold = 200
        edges = cv2.Canny(np.uint8(self.input_image), low_threshold, high_threshold)
        kernel = np.ones((4, 4), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)

        # now appy hough line detection
        # Perform HoughLinesP tranform.
        # distance resolution in pixels of the Hough grid
        rho = 1

        # angular resolution in radians of the Hough grid
        theta = np.pi / 180

        # minimum number of votes (intersections in Hough grid cell)
        threshold = 15

        # minimum number of pixels making up a line
        min_line_length = 200

        # maximum gap in pixels between connectable line segments
        max_line_gap = 20

        # lines = cv2.HoughLines(dilated_edges, 1, np.pi / 180, 200)

        lines = cv2.HoughLinesP(dilated_edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                Angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                cv2.line(self.output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # cv2.putText(self.output_image, str(counter), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,233,0))

        return lines, self.output_image

    def dilate_edges(self, edges):
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(edges, kernel, iterations=1)
        return dilation

    def get_final_result(self, input_image):

        output = input_image.copy()

        if len(input_image.shape) == 3:
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        corners = cv2.goodFeaturesToTrack(input_image, 100, 0.1, 5)
        corners = np.int0(corners)

        # paint the detected corners
        color = (0, 255, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Painiting the detected corners
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(output, (x, y), 5, color, -1)
        return output

    def fastFeatureDetector(self, img):
        # Initiate FAST object with default values
        fast = cv2.FastFeatureDetector()

        # find and draw the keypoints
        kp = fast.detect(img, None)
        img2 = cv2.drawKeypoints(img, kp, color=(255, 0, 0))

        return img2
