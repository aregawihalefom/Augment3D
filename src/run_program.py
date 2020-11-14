import argparse

import cv2
import numpy as np
import math
import os
import argparse
from src.objLoader import *

MIN_MATCHES = 10


class AR:
    """" Extract detail information  for the AR implementation"""

    def __init__(self, input_image, scale):

        self.scale = scale  # scale for the 3D object size
        self.reference_image = input_image  # reference image
        self.H = None  # Homography

        # matrix of camera parameters (made up but works quite well for me)
        self.A = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])

        # 3D object to be displayed
        self.object3D = OBJ('../assets/models/eyeball.obj', swapyz=True)

        # feature extractor and descriptor
        self.sift = cv2.xfeatures2d.SIFT_create()

        # start the process
        self.kp_model, self.des_model, self.model_image = self.intialize_refence_image()

        # initialize model
        self.intialize_refence_image()

        # Perform the main application task ( grab_video , extract features , descriptors and create homograpy)
        # then project object
        self.start_main_task()

    def intialize_refence_image(self):

        # Read the model image
        img1 = cv2.resize(cv2.imread(self.reference_image, 0), (400, 600))  # query Image

        # Initiate SIFT detector
        # find the keypoints and descriptors with SIFT
        kp1, des1 = self.sift.detectAndCompute(img1, None)

        return kp1, des1, img1

    def start_main_task(self):

        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

        count = 0

        while True:
            # get the image
            ret, frame = cap.read()
            if not ret:
                print("Unable to capture video")
                return
            # if count:
            #     img1 = frame
            #     # detect and describe features in the feature
            kp_f, des_f = self.sift.detectAndCompute(frame, None)

            # matching points between the model and the current frame
            good_matches, all_matches = self.compute_matching_points(kp_f, des_f)

            if len(all_matches) > MIN_MATCHES:
                # determine homography
                self.H = self.calculate_homography(good_matches, kp_f)

                # create boundary around the frame
                bounded_image = self.draw_boundary(frame)

                # show the 3D OBJECT
                if self.H is not None:
                    try:
                        # obtain 3D projection matrix from H matrix and camera parameters
                        projection = self.projection_matrix()
                        # project cube or model
                        frame = self.show_3d(bounded_image, self.object3D, projection, self.model_image, False)
                    except Exception as e:
                        print(e)
                else:
                    print("Homography was not created")

                # finally show the final result
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) == 27 or 0xFF == ord('q'):
                    break
            else:
                print("No enough points")
                exit()

    def draw_boundary(self, frame):
        h, w = self.model_image.shape[0], self.model_image.shape[1]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, self.H)
        frame = cv2.polylines(frame, [np.int32(dst)], True, (255, 225, 0), 3, cv2.LINE_AA)

        return frame

    def compute_matching_points(self, kp_f, des_f):

        # match descriptor with model
        # FLANN MATCHER

        FLANN_INDEX_KDTREE = 0

        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(self.des_model, des_f, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        return good, matches

    def calculate_homography(self, good, kp_f):

        # make the points into array.. for RANSAC
        src_pts = np.float32([self.kp_model[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_f[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # find H
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h, w = self.model_image.shape[0], self.model_image.shape[1]
        pts = np.float32([[0, 10], [0, h - 60], [w - 1, h - 60], [w - 1, 10]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, H)

        # homography
        return H

    # create projection matrix
    def projection_matrix(self):
        """
          From the camera calibration matrix and the estimated H
          compute the 3D projection matrix
          """
        # Compute rotation along the x and y axis as well as the translation
        H = self.H * (-1)
        rot_and_transl = np.dot(np.linalg.inv(self.A), H)
        col_1 = rot_and_transl[:, 0]
        col_2 = rot_and_transl[:, 1]
        col_3 = rot_and_transl[:, 2]

        # normalise vectors
        l = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
        rot_1 = col_1 / l
        rot_2 = col_2 / l
        translation = col_3 / l

        # compute the orthonormal basis
        c = rot_1 + rot_2
        p = np.cross(rot_1, rot_2)
        d = np.cross(c, p)
        rot_1 = np.dot(c / np.linalg.norm(c, 2) + d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
        rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
        rot_3 = np.cross(rot_1, rot_2)
        # finally, compute the 3D projection matrix from the model to the current frame
        projection = np.stack((rot_1, rot_2, rot_3, translation)).T
        return np.dot(self.A, projection)

    def show_3d(self, img, obj, projection, model, color=False):
        """
        Render a loaded obj model into the current video frame
        """
        vertices = obj.vertices
        scale_matrix = np.eye(3) * self.scale
        h, w = model.shape

        for face in obj.faces:
            face_vertices = face[0]
            points = np.array([vertices[vertex - 1] for vertex in face_vertices])
            points = np.dot(points, scale_matrix)
            # render model in the middle of the reference surface. To do so,
            # model points must be displaced
            points = np.array([[p[0] + w / 2, p[1] + h / 2, p[2]] for p in points])
            dst = cv2.perspectiveTransform(points.reshape(-1, 1, 3), projection)
            imgpts = np.int32(dst)
            if color is False:
                cv2.fillConvexPoly(img, imgpts, (137, 27, 211))
            else:
                color = self.hex_to_rgb(face[-1])
                color = color[::-1]  # reverse
                cv2.fillConvexPoly(img, imgpts, color)

        return img

    def hex_to_rgb(hex_color):
        """
           Helper function to convert hex strings to RGB
           """
        hex_color = hex_color.lstrip('#')
        h_len = len(hex_color)
        return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This program projects 3D object on top of reference image in a "
                                                 "video sequence")
    parser.add_argument("--input_dir",
                        type=str,
                        help="path to reference image.")
    parser.add_argument("--scale",
                        type=int,
                        help="Scale of the 3d object to be viewed , Recommended  values between 0.2 - 0.5")
    # Execute the parser to create Namespace object containing the above
    # Properties
    args = parser.parse_args()
    input_path = args.input_dir
    scale = args.scale

    if input_path is None:
        input_path = "assets/images/1.jpg"
    if not scale:
        scale = 0.3

    ar = AR(input_path, scale)
