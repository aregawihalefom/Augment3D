import numpy as np
import cv2
import math


class LineDetector:
    """
    This class applies different mechanisms to detect lines in an image

    """

    def __init__(self, input_image, desc=None):
        self.desc = desc
        self.input_image = input_image
        self.output_image = input_image
        print("Line detector initalized")

    def get_only_one_color(self, ):
        return self.input_image

    def apply_line_detection(self):

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

        lines = cv2.HoughLines(dilated_edges, 1, np.pi / 180, 200)

        lines = cv2.HoughLinesP(dilated_edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        
        counter = 0
        for line in lines:
            for x1, y1, x2, y2 in line:

                Angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                print(Angle)

                cv2.line(self.output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(self.output_image, str(counter), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,233,0))
            if counter == 1:
                break

            counter += 1
        return edges, self.output_image

    def apply_post_processing(self):
        raise NotImplementedError

    def get_final_result(self):
        return self.output_image
