## main.py version 0.2.0

import logging
import numpy as np
import json
import cv2

import arm
import PLC
import vision
import color as c
import color_clf as cclf


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

def go_to(x_start, y_start, x_final, y_final):

    x = x_start
    y = y_start
    x_step = int((x_final - x) / x_long)
    x_sign = int(x_step/abs(x_step))
    y_step = int((y_final - y) / y_long)
    y_sign = int(y_step/abs(y_step))
    for i in range(abs(x_step)):

        if x_sign > 0:

            PLC.long_x_positive()
            x += x_long

        elif x_sign < 0:

            PLC.long_x_negative()
            x -= x_long

        else:

            print("ERROR : X_SIGN IS 0")
            break

    for i in range(abs(y_step)):

        if y_sign > 0:

            PLC.long_y_positive()
            y += y_long

        elif y_sign < 0:

            PLC.long_y_negative()
            y -= y_short

        else:

            print("ERROR : y_SIGN IS 0")
            return False

    x_step = int((x_final - x) / x_short)
    x_sign = int(x_step/abs(x_step))
    y_step = int((y_final - y) / y_short)
    y_sign = int(y_step/abs(y_step))
    for i in range(abs(x_step)):

        if x_sign > 0:

            PLC.short_x_positive()
            x += x_short

        elif x_sign < 0:

            PLC.short_x_negative()
            x -= x_short

        else:

            print("ERROR : X_SIGN IS 0")
            break

    for i in range(abs(y_step)):

        if y_sign > 0:

            PLC.short_y_positive()
            y += y_short

        elif y_sign < 0:

            PLC.short_y_negative()
            y -= y_short

        else:

            print("ERROR : y_SIGN IS 0")
            return [x, y]

    print("X_ERROR =", x - x_final, "Y_ERROR =", y - y_final)
    return [x, y]

def approx_position(mango, x, y):
    real_mango_width = 60
    real_mango_height = 150
    mango_width = 0
    mango_heigth = 0
    x_mango = 0
    y_mango = 0
    approx_x = (x + x_mango + mango_width/2) * mango_width / real_mango_width
    approx_y = (y + y_mango + mango_heigth/2) * mango_heigth / real_mango_height
    return [approx_x, approx_y]

def most_left(mangos, x, y):

    most_left_mango = mnagos[0]
    for mango in mangos:
        ml_x, ml_y = approx_position(most_left_mango, x, y)
        x_mango, y_mango = approx_position(mango, x, y)
        if x_mango + x_error > x and x_mango <= ml_x:
            most_left_mango = mango
    return most_left_mango

def get_color(image):
    clf = cclf.load()
    return cclf.get_color(image, clf)

print("HARVEST")

x = x_min
dir_x = 1
loop_end = False

x = x_min
y = y_min
## drive x as primary axis
for x in range(x_min, x_max, x_short):
    
    print('position', x, y)
    lframe, rframe = get_frames(vcap)
    raw_mangos = vision.detect(rframe, net)
    mango = most_left(raw_mangos, x, y)
    x_mango, y_mango = approx_position(mango, x, y)
    if abs(x_mango - x) <= x_error:

        color = get_color(rframe)

        #check mango's color
        if color == c.yellow() or color == c.brown():

            ## save point
            saved_x = x

            ## drive y as secondary axis
            x, y = go_to(x, y, x, y_mango)
            arm.forward()
            arm.grab()
            arm.cut()
            arm.backward()

            ## swith-case mango's color
            if color == c.yellow():

                go_to(x, y, x_yellow, y_yellow)
                x = x_yellow
                y = y_yellow

            elif color == c.brown():

                go_to(x, y, x_brown, y_brown)
                x = x_brown
                y = y_brown

            else:

                print("ERROR : UNEXPECTED ELSE CASE OF MANGO'S COLOR")

            arm.release()

            ## return to saved point
            go_to(x, y, saved_x, y_min)
            x = saved_x
            y = y_min

        else:

            pass

    else:

        pass
    
    go_to(x, y, x + x_short, y)

print("RESULT : COLOR( " + str(vision.yellow)+ " )" + str(basket[vision.yellow]))
print("RESULT : COLOR( " + str(vision.brown)+ " )" + str(basket[vision.brown]))

