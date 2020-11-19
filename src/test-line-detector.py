import cv2
import numpy as np
import importlib
from LineDetector import LineDetector

if __name__ == '__main__':

    # read the image using opencv
    data_input = '../assets/models/computer_grid.png'
    model = '../assets/models/blue-greed.png'
    dim = (900, 900)
    img_in = cv2.resize(cv2.imread(data_input), dim)
    # img_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)

    model_in = cv2.resize(cv2.imread(model), dim)

    # This is intersting
    input_image = img_in.copy()
    model_image = model_in.copy()

    # create line detector onbject
    detector = LineDetector("Line detector")

    # 1. Get only Green
    green_only = detector.get_only_one_color(input_image)
    green_only_copy = green_only.copy()

    # get edge detection first and then lines
    gray_input = cv2.cvtColor(green_only_copy, cv2.COLOR_BGR2GRAY)
    edges = detector.auto_canny(gray_input)


    # 2. Detect Lines
    lines_input, output_image_input = detector.apply_line_detection(green_only_copy)
    gray_input = cv2.cvtColor(output_image_input, cv2.COLOR_BGR2GRAY)

    # detect edges
    edges = detector.auto_canny(gray_input)

    # error the some lines
    dilated_edges = detector.dilate_edges(edges)

    # 4. get corenrs
    corners = detector.fastFeatureDetector(dilated_edges)
    #corners_input = detector.get_final_result(dilated_edges)

    #
    # lines_model, output_image_model = detector.apply_line_detection(model_image)

    # Display results
    cv2.imshow('Original Image', corners)
    #cv2.imshow('Lines Input', corners_input)

    # cv2.imshow('Lines Model', output_image_model)
    # cv2.imshow('Corner', corners)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
