## main.py version 0.1.3

import logging
import sys, getopt

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

    logging.warning('MANGOS NOT FOUND')

def pixel_to_pulse(pixel):
    return pixel / pixel_per_pulse

def find_mangos(mangos, x_camera, y_camera):

    go_to(x_camera, y_camera)
    rel_mangos = vision.find_mangos()

    for rel_mango in rel_mangos:

        x_rel = pixel_to_pulse(rel_mango[0])
        y_rel = pixel_to_pulse(rel_mango[1])
        c = rel_mango[2]
        mango = [x_camera + x_rel, y_camera + y_rel, c]
        mangos.add(mango)

def scan():

    logging.info("SCAN FOR MANGOS")
    mangos = set()

    reset_xy()
    x_camera = min_pulse_x
    y_camera = min_pulse_y
    dx = 1
    dy = 1

    while (x_camera <= max_pulse_x) or (y_camera <= max_pulse_y):

        find_mangos(mangos, x_camera, y_camera)
        
        if x_camera >= max_pulse_x:
            dx =-1
        elif x_camera <= min_pulse_x:
            dx = 1
        else:
            dx = dx

        if y_camera >= max_pulse_y:
            dy =-1
        elif y_camera <= min_pulse_y:
            dy = 1
        else:
            dy = dy

        x_camera += pulse_step_x*dx
        y_camera += pulse_step_y*dy

    if len(mangos) <= 0: 
        error_mango_not_found()
    else: 
        pass

    return (mangos, len(mangos))

def reset_xy():

    logging.info('RESET X, Y')
    modbus.reset_xy()

def wait_for_ready():

    logging.info('WAIT FOR PLC TO BE READY')
    while modbus.is_busy() != True:
        pass

def go_to(x, y):

    wait_for_ready()
    logging.info("GO TO " + str([x, y]))
    modbus.drive(x, y)

def grab():
    arm.grab()

def collect(basket, c):

    wait_for_ready()
    logging.info("COLLECT " + str(c))
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

    logging.info("RESULT : COLOR( " + str(vision.yellow)+ " )" + str(basket[vision.yellow]))
    logging.info("RESULT : COLOR( " + str(vision.brown)+ " )" + str(basket[vision.brown]))

def set_logging_level():

    argv = sys.argv[1:]
    level = ""
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["logging="])
    except getopt.GetoptError:
        print('main.py -i <logging level>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <level>')
            sys.exit()
        elif opt in ("-i", "--logging"):
            level = arg
    try:
        logging.basicConfig(level=eval("logging." + level))
    except:
        logging.basicConfig(level=logging.WARNING)


if __name__ == '__main__':

    set_logging_level()

    logging.info("START HAVESTING")
    mangos, n_mango = scan()

    logging.info("RESET BASKET")
    basket[vision.yellow] = 0
    basket[vision.brown] = 0

    reset_xy()
    if n_mango > 0:
        for mango in mangos:
            x, y = mango[0:2]
            c = mango[2]

            logging.info("TO COLLECT MANGO ( " + str(c) +") at" + str([x, y]))

            go_to(x, y)
            grab()
            collect(basket, c)
            reset_xy()
        logging.info("FINISH HAVESTING")
        display_result(basket)
    else:
        pass