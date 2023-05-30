import cv2
import numpy as np
import glob
import os

CHECKERBOARD = (6, 9)
subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_FIX_SKEW
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
_img_shape = None
objpoints = []  # 3D point in real-world space
imgpoints_left = []  # 2D points in left camera image plane
imgpoints_right = []  # 2D points in right camera image plane

left_images = glob.glob('images/Left/img*.png')
right_images = glob.glob('images/Right/img*.png')

for left_img_path, right_img_path in zip(left_images, right_images):
    left_img = cv2.imread(left_img_path)
    right_img = cv2.imread(right_img_path)

    if _img_shape is None:
        _img_shape = left_img.shape[:2]
    else:
        assert _img_shape == left_img.shape[:2], "All images must share the same size."

    gray_left = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

    ret_left, corners_left = cv2.findChessboardCorners(gray_left, CHECKERBOARD, None)
    ret_right, corners_right = cv2.findChessboardCorners(gray_right, CHECKERBOARD, None)

    if ret_left and ret_right:
        objpoints.append(objp)
        cv2.cornerSubPix(gray_left, corners_left, (3, 3), (-1, -1), subpix_criteria)
        cv2.cornerSubPix(gray_right, corners_right, (3, 3), (-1, -1), subpix_criteria)
        imgpoints_left.append(corners_left)
        imgpoints_right.append(corners_right)

N_OK = len(objpoints)
K_left = np.zeros((3, 3))
D_left = np.zeros((4, 1))
K_right = np.zeros((3, 3))
D_right = np.zeros((4, 1))
rvecs_left = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]
tvecs_left = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]
rvecs_right = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]
tvecs_right = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]

rms_left, _, _, _, _ = cv2.fisheye.calibrate(
    objpoints,
    imgpoints_left,
    gray_left.shape[::-1],
    K_left,
    D_left,
    rvecs_left,
    tvecs_left,
    calibration_flags,
    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6),
)

rms_right, _, _, _, _ = cv2.fisheye.calibrate(
    objpoints,
    imgpoints_right,
    gray_right.shape[::-1],
    K_right,
    D_right,
    rvecs_right,
    tvecs_right,
    calibration_flags,
    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6),
)

print("Found " + str(N_OK) + " valid images for calibration")
print("Left Camera:")
print("DIM=" + str(_img_shape[::-1]))
print("K=np.array(" + str(K_left.tolist()) + ")")
print("D=np.array(" + str(D_left.tolist()) + ")")
print("RMS error: ", rms_left)

print("\nRight Camera:")
print("DIM=" + str(_img_shape[::-1]))
print("K=np.array(" + str(K_right.tolist()) + ")")
print("D=np.array(" + str(D_right.tolist()) + ")")
print("RMS error: ", rms_right)

# Save the undistorted images
undistorted_folder = "undistorted/"
if not os.path.exists(undistorted_folder):
    os.makedirs(undistorted_folder)

for i in range(N_OK):
    undistorted_left = cv2.fisheye.undistortImage(
        left_img.astype(np.uint8),
        K_left,
        D_left,
        Knew=K_left,
        new_size=_img_shape[::-1],
    )

    undistorted_right = cv2.fisheye.undistortImage(
        right_img.astype(np.uint8),
        K_right,
        D_right,
        Knew=K_right,
        new_size=_img_shape[::-1],
    )

    cv2.imwrite(undistorted_folder + f"undistorted_left_{i}.png", undistorted_left)
    cv2.imwrite(undistorted_folder + f"undistorted_right_{i}.png", undistorted_right)

print('Undistorted images saved to', undistorted_folder)
