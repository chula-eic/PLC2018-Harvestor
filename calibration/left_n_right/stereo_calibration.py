import numpy as np
import cv2 as cv
import glob
import json


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpointsL = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
objpointsR = [] # 3d point in real world space
imgpointsR = [] # 2d points in image plane.
images = glob.glob('left*.png')

count = 0
for fname in images:
    print("read", fname)
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,7), None)
    # If found, add object points, image points (after refining them)

    if ret == True:

        count += 1
        objpointsL.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpointsL.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (9,7), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(100)

    if count >= 50: break
    

print("ret == True  count", count)

images = glob.glob('right*.png')

count = 0
for fname in images:
    print("read", fname)
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,7), None)
    # If found, add object points, image points (after refining them)

    if ret == True:

        count += 1
        objpointsR.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpointsR.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (9,7), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(100)

    if count >= 50: break
    

cv.destroyAllWindows()

print("ret == True  count", count)

cameramtx = cv.UMat(np.array([
    [142.230224609375, 0.0, 194.09322290448472],
    [0.0, 167.86573791503906, 129.81425585354464],
    [0.0, 0.0, 1.0]
    ]))
dist = cv.UMat(np.array([
        [0.02258901665656029, 0.018869741300398365, -0.00013336432819995717, 0.00026830435749782526, -0.05545675195243372]
    ]))

ret, cameramtx1, dist1, cameramtx2, dist2, R, T, E, F = cv.stereoCalibrate(objpointsL, imgpointsL, objpointsR, imgpointsR, (320, 240), cameramtx, dist, cameramtx, dist)

calibration = {
    "cameramtx1": cameramtx1.tolist(),
    "dist1": dist1.tolist(),
    "cameramtx2": cameramtx2.tolist(),
    "dist2": dist2.tolist()
}

with open("../stereoCalibrate.json", "w") as write_file:
    json.dump(calibration, write_file, indent=4)
