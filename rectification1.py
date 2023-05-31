import cv2
import numpy as np

def rectify_images(img_left, img_right, mtx_left, dist_left, mtx_right, dist_right, R, T):
    img_shape = img_left.shape[::-1]

    # Convert arrays to cv::UMat
    mtx_left = cv2.UMat(mtx_left)
    dist_left = cv2.UMat(dist_left)
    mtx_right = cv2.UMat(mtx_right)
    dist_right = cv2.UMat(dist_right)
    R = cv2.UMat(R)
    T = cv2.UMat(T)

    # Stereo rectification
    R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(
        mtx_left, dist_left, mtx_right, dist_right, img_shape, R, T
    )

    # Convert rectification matrices to numpy arrays
    R1 = R1.get()
    R2 = R2.get()
    P1 = P1.get()
    P2 = P2.get()

    # Undistort and rectify images
    map1_left, map2_left = cv2.initUndistortRectifyMap(mtx_left, dist_left, R1, P1, img_shape, cv2.CV_16SC2)
    map1_right, map2_right = cv2.initUndistortRectifyMap(mtx_right, dist_right, R2, P2, img_shape, cv2.CV_16SC2)

    # Undistort and rectify the left image
    img_rectified_left = cv2.remap(img_left, map1_left, map2_left, cv2.INTER_LINEAR)

    # Undistort and rectify the right image
    img_rectified_right = cv2.remap(img_right, map1_right, map2_right, cv2.INTER_LINEAR)

    return img_rectified_left, img_rectified_right

# Example usage
img_left = cv2.imread('undistorted_camera1.png')
img_right = cv2.imread('undistorted_camera2.png')

# Camera matrices and distortion coefficients for both cameras
mtx_left = np.array([[387.21452635, 0., 294.98247839],
                     [0., 517.25797702, 229.92321276],
                     [0., 0., 1.]])
dist_left = np.array([0.39662725, 0.1800423, 0.00073226, 0.00461239, -0.03782871, 0.])

mtx_right = np.array([[-0.39662725, 0.1800423, 0.00073226, 0.00461239, -0.03782871, 0.],
                      [0., 517.25797702, 229.92321276],
                      [0., 0., 1.]])
dist_right = np.array([-0.39662725, 0.1800423, 0.00073226, 0.00461239, -0.03782871, 0.])

# Rotation matrix and translation vector
R = np.array([[ 1.00000000e+00, 1.43393689e-13, -6.34281687e-13],
              [-1.43393689e-13, 1.00000000e+00, 1.39703631e-12],
              [ 6.34281687e-13, -1.39703631e-12, 1.00000000e+00]])
T = np.array([1.97125521e-11, -3.56770236e-11, 2.16573332e-12])

# Rectify the images
img_rectified_left, img_rectified_right = rectify_images(img_left, img_right, mtx_left, dist_left, mtx_right, dist_right, R, T)

# Display the rectified images
cv2.imshow('Rectified Left', img_rectified_left)
cv2.imshow('Rectified Right', img_rectified_right)
cv2.waitKey(0)
cv2.destroyAllWindows()
