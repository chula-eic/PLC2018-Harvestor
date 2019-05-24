## main.py version 0.1.4

import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np

test = True

if test:
    import test_arm as arm
    import test_modbus as modbus
    import test_vision as vision
else:
    import arm
    import modbus
    import vision

basket = {}
x_yellow = 1000
y_yellow = 0
x_brown = 2000
y_brown = 0

travel_x = [0]
travel_y = [0]

grab_x = []
grab_y = []

x_min= 0
x_max = 10000
y_min = 0
y_max = 10000
x_interval = 1000
y_interval = 1000

pixel_per_pulse = 10

def test_print(msg):
    if test: print(msg)

def error_mango_not_found():

    test_print('MANGOS NOT FOUND')

def pixel_to_pulse(pixel):
    return pixel / pixel_per_pulse

def find_mangos(mangos, x_camera, y_camera):

    go_to(x_camera, y_camera)
    rel_mangos = vision.find_mangos()

    for rel_mango in rel_mangos:

        x_rel = pixel_to_pulse(rel_mango[0])
        y_rel = pixel_to_pulse(rel_mango[1])
        c = rel_mango[2]
        mango = (x_camera + x_rel, y_camera + y_rel, c)
        test_print("FIND MANGO AT " + str(mango[0]) + " , " + str(mango[1]) + " WITH COLOR " + str(c))
        mangos.add(mango)

def scan():

    test_print("SCAN FOR MANGOS")
    mangos = set()

    reset()
    x_camera = x_min
    dir_x = 1
    loop_end = False

    for y_camera in range(y_min, y_max + y_interval, y_interval):

        if y_camera >= y_max: 
            y_camera = y_max
            loop_end = True
        while True:
            find_mangos(mangos, x_camera, y_camera)
            if x_camera + x_interval*dir_x < x_min:
                dir_x = 1
                test_print("CHANGE DIRECTION X TO " + str(dir_x))
                break
            elif x_camera + x_interval*dir_x > x_max:
                dir_x = -1
                test_print("CHANGE DIRECTION X TO " + str(dir_x))
                break
            else:
                x_camera += x_interval*dir_x

        if loop_end: break


    if len(mangos) <= 0: 
        error_mango_not_found()
    else: 
        pass

    return (mangos, len(mangos))

def reset():

    test_print('RESET X, Y')
    travel_x.append(0)
    travel_y.append(0)
    modbus.reset()

def wait_for_ready():

    test_print('WAIT FOR PLC TO BE READY')
    while modbus.is_busy():
        pass

def go_to(x, y):

    wait_for_ready()
    test_print("GO TO " + str([x, y]))
    modbus.drive(x, y)

def grab():
    arm.grab()

def collect(basket, c):

    wait_for_ready()
    test_print("COLLECT " + str(c))
    x = 0; y = 0

    if c == vision.yellow:
        x = x_yellow
        y = y_yellow
    elif c == vision.brown:
        x = x_brown
        y = y_brown
    
    go_to(x, y)
    travel_x.append(x)
    travel_y.append(y)
    basket[c] += 1

def display_result(basket):

    test_print("RESULT : COLOR( " + str(vision.yellow)+ " )" + str(basket[vision.yellow]))
    test_print("RESULT : COLOR( " + str(vision.brown)+ " )" + str(basket[vision.brown]))


if __name__ == '__main__':

    is_debugging = True or test

    if is_debugging:
        logging.basicConfig(level=test_print)
    else:
        logging.basicConfig(level=test_print)

    test_print("SET DEBUGGING = %s" + str(is_debugging))

    if test: test_print("START TESTING")
    test_print("START HAVESTING")
    mangos, n_mango = scan()

    test_print("RESET BASKET")
    basket[vision.yellow] = 0
    basket[vision.brown] = 0

    reset()
    if n_mango > 0:
        X = []
        Y = []
        C = []
        for mango in mangos:
            x, y = mango[0:2]
            c = mango[2]
            X.append(x)
            Y.append(y)
            C.append('y' if c == vision.yellow else 'r')

            test_print("TO COLLECT MANGO ( " + str(c) +") at" + str([x, y]))

            go_to(x, y)
            travel_x.append(x)
            travel_y.append(y)
            grab()
            grab_x.append(x)
            grab_y.append(y)
            collect(basket, c)
            reset()
        test_print("FINISH HAVESTING")
        display_result(basket)
        if test:
            plt.scatter(X, Y, c=C)
            plt.plot(travel_x, travel_y, alpha=0.5)
            plt.show()
    else:
        pass