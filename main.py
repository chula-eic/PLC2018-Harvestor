## main.py version 0.1.2

import logging

import arm
import modbus
import vision

basket = {}
x_yellow = 0
y_yellow = 0
x_brown = 0
y_brown = 0

min_pulse_x = 0
max_pulse_x = 10000
min_pulse_y = 0
max_pulse_y = 10000
pulse_step_x = 500
pulse_step_y = 200

pixel_per_pulse = 10

def error_mango_not_found():

    logging.debug('ERROR 0x00: MANGOS NOT FOUND')

def pixel_to_pulse(pixel):
    return pixel / pixel_per_pulse

def find_mango():

    logging.debug("scan for mangos")
    mangos = set()

    reset_xy()
    x_camera = min_pulse_x
    y_camera = min_pulse_y

    while (x_camera <= max_pulse_x) and (y_camera <= max_pulse_y):

        go_to(x_camera, y_camera)
        rel_mangos = vision.find_mangos()

        for rel_mango in rel_mangos:

            x_rel = pixel_to_pulse(rel_mango[0])
            y_rel = pixel_to_pulse(rel_mango[1])
            c = rel_mango[2]
            mango = [x_camera + x_rel, y_camera + y_rel, c]
            mangos.add(mango)
        
        x_camera += pulse_step_x
        y_camera += pulse_step_y

    if len(mangos) <= 0: 
        error_mango_not_found()
    else: 
        pass

    return (mangos, len(mangos))

def reset_xy():

    logging.debug('Rreset X, Y')
    modbus.reset_xy()

def wait_for_ready():

    logging.debug('wait for PLC to be ready')
    while modbus.is_busy() != True:
        pass

def go_to(x, y):

    wait_for_ready()
    logging.debug("go to " + str([x, y]))
    modbus.drive(x, y)

def grab():
    arm.grab()

def collect(basket, c):

    wait_for_ready()
    logging.debug("collect " + str(c))
    x = 0; y = 0

    if c == vision.yellow:
        x = x_yellow
        y = y_yellow
    elif c == vision.brown:
        x = x_brown
        y = y_brown
    
    go_to(x, y)
    basket[c] += 1

def display_result(basket):
    logging.debug("result : color( " + str(vision.yellow)+ " )" + str(basket[vision.yellow]))
    logging.debug("result : color( " + str(vision.brown)+ " )" + str(basket[vision.brown]))

if __name__ == '__main__':

    logging.debug("start havesting")
    mangos, n_mango = find_mango()

    logging.debug("reset basket")
    basket[vision.yellow] = 0
    basket[vision.brown] = 0

    reset_xy()
    if n_mango > 0:
        for mango in mangos:
            x, y = mango[0:2]
            c = mango[2]

            logging.debug("to collect mango ( " + str(c) +") at" + str([x, y]))

            go_to(x, y)
            grab()
            collect(basket, c)
            reset_xy()
        logging.debug("finish havesting")
        display_result(basket)
    else:
        pass