import logging
import cv2
import numpy as np
import json
import vision

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

logging.debug("SETUP DARKNET")
net = vision.load()

try:
    cap = cv2.VideoCapture(1)
    logging.debug("SUCCESFULLY ACTIVATE WEBCAM")
except:
    logging.error("ERROR CANNOT ACTIVATE WEBCAM")
    exit(0)
    
logging.debug("WIDTH = %s", str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
logging.debug("HEIGHT = %s", str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

calibrate_file = open("calibration/calibration.json", "r")
calib = json.load(calibrate_file)
calibrate_file.close()
mtx = np.array(calib['mtx'])
dist = np.array(calib['dist'])
newcameramtx = np.array(calib['newcameramtx'])

n = 5

logging.debug("START START CAPTURING " + str(n*2) + " IMAGES FOR EACH COLOR")
wait = -1

for c_str in ["y", "b", "g"]:

    if c_str == "y" : logging.debug("START START CAPTURING YELLOW MANGOS")
    elif c_str == "b" : logging.debug("START START CAPTURING BROWN MANGOS")
    elif c_str == "g" : logging.debug("START START CAPTURING GREEN MANGOS")
    else: break

    i = 0
    while i < n:

        left_raw, right_raw = read_video(cap)
        left_dst = cv2.undistort(left_raw, mtx, dist, None, newcameramtx)
        right_dst = cv2.undistort(right_raw, mtx, dist, None, newcameramtx)
        cv2.imshow('left', left_dst)
        cv2.imshow('right', right_dst)
        left_mango = vision.detect(left_dst, net)
        right_mango = vision.detect(right_dst, net)
        if left_mango != None and right_mango != None:
            left_i = 2*i
            right_i = 2*i + 1
            left_path = "mango_color/" + c_str + str(left_i) + ".png"
            cv2.imwrite(left_path, left_dst)
            logging.debug("WRITE AT " + left_path)
            right_path ="mango_color/" + c_str + str(right_i) + ".png" 
            cv2.imwrite(right_path, right_dst)
            logging.debug("WRITE AT " + right_path)
            i += 1
        cv2.waitKey(100)

    if c_str != "g": input("PRESS ENTER TO CONTINUE")


logging.debug("END CAPTURING")