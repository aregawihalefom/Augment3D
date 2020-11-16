import numpy as np
import cv2


class mainAlgorithm:
    """

    """

    def __init__(self, img, desc=None):
        self.desc = desc
        self.input_image = img
        self.out_image = None

    def start_the_process(self):
        pass

    def based_on_green_channel(self):
        blue_channel = self.input_image[:, :, 1]

        low_threshold = 50
        high_threshold = 200

        edges = cv2.Canny(np.uint8(blue_channel), low_threshold, high_threshold)
        kernel = np.ones((4, 4), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)

        return dilated_edges

    def based_on_horizontal_vertical(self):
        raise NotImplementedError

    def based_on_distance_between(self):
        raise NotImplementedError

    def based_on_rectangluar(self):
        raise NotImplementedError

    def final_kalman_filter(self):
        raise NotImplementedError

    def final_corners(self):
        raise NotImplementedError
