import math

import arm
import main
import modbus
import vision

screen_width = 600
screen_height = 200

def ptp(mango5):
    x_mango = mango5[0]+(mango5[2]//2) - screen_width/2
    y_mango = mango5[1]+(mango5[3]//2) - screen_height/2
    return [x_mango, y_mango, mango5[4]]

def distant2(mango3):
    return mango3[0]**2 + mango3[1]**2

def find_nearest(mango_list):
    if len(mango_list) != 0:
        nearest_mango = ptp(mango_list[0])
        for mango in mango_list:
            mango = ptp(mango)
            if distant2(mango) < distant2(nearest_mango):
                nearest_mango = mango
        return nearest_mango
    else:
        return None

def get_mango(x, y, x_error, y_error, alpha, beta):

    x_start = x
    y_start = y

    mango_list = vision.get_mangos()
    n = len(mango_list)

    while n != 0 :

        ## get nearest mango
        mango = find_nearest(mango_list)
        x_mango = mango[0]
        y_mango = mango[1]
        c = mango[2]

        ## adjust visual servo
        while x_mango >= x_error and y_mango >= y_error:
            x += alpha * x_mango
            y += beta * y_mango
            modbus.drive(x, y)

        arm.grab()
        arm.collect(c)

        ## return to x_start, y_start
        x = x_start
        y = y_start
        modbus.drive(x, y)
        mango_list = vision.get_mangos()
        n = len(mango_list)
       

def main_event(config):
    x, y, x_max, y_max, x_interval, y_interval, x_error, y_error, alpha, beta = config
    while True :
        modbus.drive(x, y)
        get_mango(x, y, x_error, y_error, alpha, beta)
        if x != x_max : x = x + x_interval
        else: 
            x=0
            if y != y_max : y = y + y_interval
            else : 
                break 
