import json
import numpy as np
import cv2
from time import time
import logging


def read_video(cap, mtx, dist, newcameramtx, stereo):
    ret, frame = cap.read()
    (h, w, c) = frame.shape
    cv2.imshow("Raw Image", frame)

    left_dst = cv2.undistort(frame[:, :int(w/2), :], mtx, dist, newcameramtx)
    right_dst = cv2.undistort(frame[:, int(w/2):, :], mtx, dist, newcameramtx)
    cv2.imshow("Left", left_dst)
    cv2.imshow("Right", right_dst)

    return frame

#capture via webcam 0
logging.basicConfig(level=logging.DEBUG)
logging.debug("START DEBUGGING")
try:
    cap = cv2.VideoCapture(1)
    logging.debug("SUCCESFULLY ACTIVATE WEBCAM")
except:
    logging.error("ERROR CANNOT ACTIVATE WEBCAM")
    exit(0)


with open("calibration.json", "r") as fp:
    logging.debug("READ CALIBRATION JSON")
    calibration = json.load(fp)
    mtx = np.array(calibration["mtx"])
    dist = np.array(calibration["dist"])
    newcameramtx = np.array(calibration["newcameramtx"])
    
logging.debug("WIDTH = %s", str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
logging.debug("HEIGHT = %s", str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = cap.get(cv2.CAP_PROP_FPS)
delta_time = 100/fps
logging.debug("START VIDEO CAPTURE WITH %d MILLISECONDS INTERVAL", int(delta_time))

stereo = cv2.StereoBM()

logging.debug("START START CAPTURING")
wait = -1
while cap.isOpened() and wait == -1:

    frame = read_video(cap, mtx, dist, newcameramtx, stereo)
    wait = cv2.waitKey(int(delta_time))

logging.debug("END CAPTURING")