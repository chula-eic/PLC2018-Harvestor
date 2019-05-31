import logging
import cv2
import numpy as np
import json

def read_video(cap):
    ret, frame = cap.read()
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
delta_time = 100/fps

logging.debug("START VIDEO CAPTURE WITH %d MILLISECONDS INTERVAL", int(delta_time))

logging.debug("START START CAPTURING")
wait = -1
while cap.isOpened() and wait == -1:

    left_raw, right_raw = read_video(cap)
    cv2.imshow('left', left_raw)
    cv2.imshow('right', right_raw)
    wait = cv2.waitKey(int(delta_time))

logging.debug("END CAPTURING")
