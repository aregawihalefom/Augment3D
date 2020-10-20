# Augment3D

In this repository, Projection 3D Objects on top of reference images using augmented reality techniques is demonstrated.

## How it works
In General, This works based on feature extraction and feature description using SIFT features. The workflow is describe as

 1. Feature reach image(i.e to make feature extraction easier) is used as a reference image.
 2. Using Opencv, Video of the reference image is captured(Consistently)
 3. Both the reference image and current video frame , `SIFT` features and descriptors are extracted.
 4. Based Lowe's(author of SIFT) ratio test good matching points are extracted.
 5. A homography is calculated using RANSAC Algorithm.
 6. projection matrix is calculated from the homography and some orthonormal vector Properties to project the 3D object into
 reference image

 ## Dependencies

 ```pip3 install opencv-python numpy pyqt5```
 Incase if you get this error:<br /> <br /> 
 'QObject::moveToThread: Current thread (0x55fded9ab880) is not the object's thread (0x55fdedb9aee0). Cannot move to target thread (0x55fded9ab880)'
 <br /> <br /> you need to install opencv version which matches with your installed pyqt version<br /> 
  in our case ```opencv-python==4.3.0.36``` and ```pyqt5==5.15.1```  works fine. <br /> 

## Usage

*  First reference image should be provided either by coping to `assets/images` folder with '1.jpg' filename
   then run the program in your command line using `python run_program.py`

* Alternatively the reference image could provided as command line argument as `python run_program.py --input_path [path-to-the-image]/1.jpg`


## some results

![alt text](https://github.com/aregawihalefom/Augment3D/blob/master/assets/results/new-other-augmented.gif)


# To-do
