import cv2
import numpy as np


# add some noise
def add_gaussian_noise(file):
    # Gaussian distribution parameters
    mean = 0
    var = 20
    sigma = var ** 0.5
    noisy_image = np.zeros(file.shape, np.float32)

    gaussian = np.random.normal(mean, sigma, (file.shape[0], file.shape[1]))
    noisy_image[:, :, 0] = file[:, :, 0] + gaussian
    noisy_image[:, :, 1] = file[:, :, 1] + gaussian
    noisy_image[:, :, 2] = file[:, :, 2] + gaussian

    return noisy_image


# get the image
filename = '../assets/images/model.png'
img = cv2.resize(cv2.imread(filename), (1028, 720))
img = add_gaussian_noise(img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# haris corner detector
def good_features(input):

    corners = cv2.goodFeaturesToTrack(input, 30, 0.01, 10)
    corners = np.int0(corners)

    return corners


def edge_detector(input):

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(input, (kernel_size, kernel_size), 0)

    low_threshold = 150
    high_threshold = 200
    edges = cv2.Canny(np.uint8(blur_gray), low_threshold, high_threshold)
    kernel = np.ones((1, 1), np.uint8)
    edges = cv2.erode(edges, kernel, iterations=1)

    return edges


def paint_corenrs(input, corners):

    color = (0, 0, 255)
    # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(input, (x, y), 6, color, -1)
    return input


# haris corner detection
corners = good_features(gray)

# paint corners
painter_corners = paint_corenrs(img, corners)

# edges , find edges
edge = edge_detector(gray)

# show the image
cv2.imshow('Painted Image', painter_corners)
cv2.imshow('Edge Image', edge)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
