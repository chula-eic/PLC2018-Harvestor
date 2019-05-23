import logging

import modbus
import arm
import vision

basket = {}
x_yellow = 0
y_yellow = 0
x_brown = 0
y_brown = 0

def error_mango_not_found():

    logging.debug('ERROR 0x00: MANGOS NOT FOUND')

def find_mango():

    mangos = vision.find_mangos()

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
        for i in range(0, n_mango):
            x, y = mangos[i][0:2]
            c = mangos[i][2]

            logging.debug("to collect mango ( " + str(c) +") at" + str([x, y]))

            go_to(x, y)
            grab()
            collect(basket, c)
            reset_xy()
        logging.debug("finish havesting")
        display_result(basket)
    else:
        pass