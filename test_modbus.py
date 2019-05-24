import logging
import time

logging.info("CONNECT TO PLC")

def reset():
    logging.info("RESET X, Y TO 0, 0")

def read_XY():
    logging.info("READ X, Y")

def is_busy():
    logging.info("CHECK IF PLC IS BUSY OR NOT")
    return False

def drive(x,y):
    if is_busy(): return False
    logging.info("WRITE REG X = %d  Y = %d", x, y)
    while is_busy():
        pass
    logging.info("DRIVE TO %d, %d", x, y)
    return True
