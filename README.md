# Stereovision
creating a stereovision system

**Dependencies:**

numpy

Python 3.5.3 or above

OpenCV 4.1.1 (pre-compiled, 'pip' from Python Wheels)

StereoVision lib 1.0.3 (https://github.com/erget/StereoVision)

**Current Issue:**

Trying to get the rectify.py and/or rectification1.py code working.

The rectification1.py codee takes the undistorted_camer1 and undistorted_camera2.png images and goes through rectification where the images are realigned by featuring matching. The error that I get is as following: TypeError: Expected Ptr<cv::UMat> for argument '%s . The parameters of the intrinsic and extrinsic cameras are already identified and placed in the code. 

Similarily, in rectify.py the the code calibrates as well as rectiy the images. It takes in the undistorted images from left (undistorted_left) and right (undistorted_right) images, calibrates the camera and undistorts the images, then rectifies the last pair of images. the calibration parameters and rectification parameters are saved in a file called calib_result. The error I am getting is as follows: TypeError: Expected Ptr<cv::UMat> for argument '%s.

A successful retified image will align both images pixel-to-pixel.

![image](https://github.com/ZalvinZ/Stereovision/assets/26739762/6550ac54-8d2c-474b-b0c3-72b75a0b7f8a)


A successful disparity mapping will look like this:

![image](https://github.com/ZalvinZ/Stereovision/assets/26739762/01dafc81-90fd-41b7-888d-eaf1ef70ec91)

