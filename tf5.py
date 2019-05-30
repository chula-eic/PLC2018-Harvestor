import logging
import cv2
import numpy as np
import json

def read_video(cap):
    ret, frame = cap.read()
    cv2.imshow("Video Capture", frame)
    h, w, c = frame.shape
    left_raw = frame[:, :int(w/2), :]
    right_raw = frame[:, int(w/2):, :]

    return (left_raw, right_raw)

#capture via webcam 0
logging.basicConfig(level=logging.DEBUG)
logging.debug("START DEBUGGING")
try:
    cap = cv2.VideoCapture(1)
    logging.debug("SUCCESFULLY ACTIVATE WEBCAM")
except:
    logging.error("ERROR CANNOT ACTIVATE WEBCAM")
    exit(0)
    
logging.debug("WIDTH = %s", str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
logging.debug("HEIGHT = %s", str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = cap.get(cv2.CAP_PROP_FPS)
delta_time = 100/fps/2

calibrate_file = open("calibration/calibration.json", "r")
calib = json.load(calibrate_file)
calibrate_file.close()
mtx = np.array(calib['mtx'])
dist = np.array(calib['dist'])
newcameramtx = np.array(calib['newcameramtx'])

logging.debug("START VIDEO CAPTURE WITH %d MILLISECONDS INTERVAL", int(delta_time))

logging.debug("START START CAPTURING")
wait = -1
while cap.isOpened() and wait == -1:

    left_raw, right_raw = read_video(cap)
    left_dst = cv2.undistort(left_raw, mtx, dist, None, newcameramtx)
    right_dst = cv2.undistort(right_raw, mtx, dist, None, newcameramtx)
    cv2.imshow('left', left_dst)
    cv2.imshow('right', right_dst)
    wait = cv2.waitKey(int(delta_time))

logging.debug("END CAPTURING")