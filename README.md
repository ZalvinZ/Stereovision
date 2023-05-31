# Stereovision
creating a stereovision system

Cuurent Issue:
Trying to get the rectify.py code working.
The code takes the undistorted_camer1 and undistorted_camera2.png images and goes through rectification when the images are realigned by featuring matching. The error that I get is as following: TypeError: Expected Ptr<cv::UMat> for argument '%s
The image input does not go into the stereocalibrator function.

A successful retified image will align both images pixel-to-pixel.

A successful disparity mapping will look like this:
![image](https://github.com/ZalvinZ/Stereovision/assets/26739762/01dafc81-90fd-41b7-888d-eaf1ef70ec91)

