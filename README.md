# Augment3D

In this repository, Projection of model of 3D Objects on top of reference images using augmented reality techniques is demonstrated.

## How it works
In General, This works based on feature extraction and feature description using SIFT features. The workflow is describe as 
 
 1. Feature reach image(i.e to make feature extraction easier) is used as a reference image.
 2. Using Opencv, Video of the reference image is captured(Consistently)
 3. Both the reference image and current video frame , `SIFT` features and descriptors are extracted.
 4. Based Lowe's(author of SIFT) ratio test good matching points are extracted.
 5. A homography is calculated using RANSAC Algorithm.
 6. projection matrix is calculated from the homography and some orthonormal vector prorties to project the 3D object into 
 reference image