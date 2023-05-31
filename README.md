# Stereovision
creating a stereovision system

Dependencies:
Python 3.5.3 or above
OpenCV 4.1.1 (pre-compiled, 'pip' from Python Wheels)
StereoVision lib 1.0.3 (https://github.com/erget/StereoVision)

Cuurent Issue:
Trying to get the rectify.py code working.
The code takes the undistorted_camer1 and undistorted_camera2.png images and goes through rectification when the images are realigned by featuring matching. The error that I get is as following: TypeError: Expected Ptr<cv::UMat> for argument '%s
The image input does not go into the stereocalibrator function.

A successful retified image will align both images pixel-to-pixel.

![image](https://github.com/ZalvinZ/Stereovision/assets/26739762/6550ac54-8d2c-474b-b0c3-72b75a0b7f8a)


A successful disparity mapping will look like this:

![image](https://github.com/ZalvinZ/Stereovision/assets/26739762/01dafc81-90fd-41b7-888d-eaf1ef70ec91)

