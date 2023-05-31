import cv2
import numpy as np
import glob
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration
from stereovision.exceptions import ChessboardNotFoundError

# Chessboard settings
img_width = 320
img_height = 240
chessboard_size = (9, 6)
rows = 6
columns=9
square_size = 2.6  # Size of each square in cm
image_size = (img_width,img_height)

images_left = glob.glob('images/Left/img*.png')
images_right = glob.glob('images/Right/img*.png')
images_left.sort()
images_right.sort()

calibrator = StereoCalibrator(rows, columns, square_size, image_size)

for i in range(len(images_left)):
    img_left = cv2.imread(images_left[i])
    img_right = cv2.imread(images_right[i])
    gray = cv2.cvtColor(np.float32(imgUMat), cv2.COLOR_RGB2GRAY)
    gray = cv2.cvtColor(np.float32(imgUMat), cv2.COLOR_RGB2GRAY)

    try:
        calibrator._get_corners(images_left)
        calibrator._get_corners(images_right)
    except ChessboardNotFoundError as error:
        print(error)
        print ("Pair No  ignored")
    else:
        calibrator.add_corners((images_left, images_right), True)
  
print ('End cycle')


print ('Starting calibration... It can take several minutes!')
calibration = calibrator.calibrate_cameras()
calibration.export('calib_result')
print ('Calibration complete!')
# Lets rectify and show last pair after  calibration
calibration = StereoCalibration(input_folder='calib_result')
rectified_pair = calibration.rectify((images_left, images_right))

cv2.imshow('Left CALIBRATED', rectified_pair[0])
cv2.imshow('Right CALIBRATED', rectified_pair[1])
cv2.imwrite("rectifyed_left.jpg",rectified_pair[0])
cv2.imwrite("rectifyed_right.jpg",rectified_pair[1])
cv2.waitKey(0)

# Release resources
cv2.destroyAllWindows()
