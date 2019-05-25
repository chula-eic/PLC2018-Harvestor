import serial
import config

config.isCutting,config.isReleasing = False,False

def grab():
    print("Grabbing mango")
def release():
    print("Releasing mango")
def cut():
    print("Cutting wire")
    isCutting = True
def is_cutting():
    return config.isCutting
def is_releasing():
    return config.isReleasing
def status():


#PORT = COM3, COM5 , ... somthing something lol
def serial_listen(PORT):
    ser = serial.Serial(PORT, 38400, timeout=0.1)
    while True:
        if ser.isOpen():
            rl = ser.readline()
        else:
            #print("Serial is not available")
            continue

        try:
            rl = rl.decode('utf-8')
        except UnicodeDecodeError:
            rl = str(rl)
        if(rl == 'CUTTING' or rl == 'RELEASING'):
def serial_write():
    ser = serial.Serial(PORT, 38400, timeout=0.1)
