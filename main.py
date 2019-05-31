## main.py version 0.2.0

import logging
import numpy as np
import json
import cv2

import arm
import PLC
import vision


print("CONFIGUE")
basket = {}

with open("mainConfig.json", "r") as config_file:
    config = json.load(config_file)
    x_yellow = config['x_yellow']
    y_yellow = config['y_yellow']
    x_brown = config['x_brown']
    y_brown = config['y_brown']
    x_min = config['x_min']
    x_max = config['x_max']
    x_long = config['x_long']
    x_short = config['x_short']
    x_error = config['x_error']
    y_min = config['y_min']
    y_max = config['y_max']
    y_long = config['y_long']
    y_short = config['y_short']
    y_error = config['y_error']

print("SETUP ARM")
arm.setup()

print("SETUP PLC")
PLC.setup()

print("SETUP VISION")
net = vision.load()
vcap = cv2.VideoCapture(1)

def get_frames(vcap):

    ret, images = vcap.read()
    h, w, c = frame.shape
    l_image = frame[:, :int(w/2), :]
    r_image = frame[:, int(w/2):, :]
    return [l_image, r_image]

def go_to(x, y, x_end, y_end):

    x_step = int((x - x_end) / x_long)
    x_sign = int(x_step/abs(x_step))
    y_step = int((y - y_end) / y_long)
    y_sign = int(y_step/abs(y_step))
    for i in range(abs(x_step)):

        if x_sign > 0:

            PLC.long_x_positive()
            x_end += x_long

        elif x_sign < 0:

            PLC.long_x_negative()
            x_end -= x_long

        else:

            print("ERROR : X_SIGN IS 0")
            break

    for i in range(abs(y_step)):

        if y_sign > 0:

            PLC.long_y_positive()
            y_end += y_long

        elif y_sign < 0:

            PLC.long_y_negative()
            y_end -= y_short

        else:

            print("ERROR : y_SIGN IS 0")
            return False

    x_step = int((x - x_end) / x_short)
    x_sign = int(x_step/abs(x_step))
    y_step = int((y - y_end) / y_short)
    y_sign = int(y_step/abs(y_step))
    for i in range(abs(x_step)):

        if x_sign > 0:

            PLC.short_x_positive()
            x_end += x_short

        elif x_sign < 0:

            PLC.short_x_negative()
            x_end -= x_short

        else:

            print("ERROR : X_SIGN IS 0")
            break

    for i in range(abs(y_step)):

        if y_sign > 0:

            PLC.short_y_positive()
            y_end += y_short

        elif y_sign < 0:

            PLC.short_y_negative()
            y_end -= y_short

        else:

            print("ERROR : y_SIGN IS 0")
            return False

    print("X_ERROR =", x_end - x, "Y_ERROR =", y_end - y)
    return True

print("HARVEST")

x_end = x_min
dir_x = 1
loop_end = False

x_end = x_min
y_end = y_min
for x_end in range(x_min, x_max, x_short):
    
    x_save = x_end
    lframe, rframe = get_frames(vcap)
    raw_mangos = vision.detect(rframe, net)
    
    go_to(x_end + x_short, y_end, x_end, y_end)

print("RESULT : COLOR( " + str(vision.yellow)+ " )" + str(basket[vision.yellow]))
print("RESULT : COLOR( " + str(vision.brown)+ " )" + str(basket[vision.brown]))

