import serial
import config.py
from time import sleep
config.isBusy = False
config.PORT = 'COM5'
ser = None
def setup():
    global ser
    ser = serial.Serial(config.PORT, 9600, timeout=1)
    st = serial_read()
    while(not st == "SETUP DONE"):
        st=serial_read()
def serial_write(s):
    t = s
    global ser
    ser.write(s.encode('utf-8'))
    return serial_read(t)

def serial_read(cmd=""):
    global ser
    
    while True:
        if ser.isOpen():
            rl = ser.readline()
        else:
            print("Serial is not available")
            continue
        try:
            rl = rl.decode('utf-8')
        except UnicodeDecodeError:
            rl = str(rl)
        if(rl == "DONE"):
            print('Done')
            setToDefault()
            return 'SUCCESS'
        elif(rl == "GOING FORWARD" or rl == "GOING BACKWARD" or rl == "STOPPED"):
           print('DONE')
           return('SUCCESS')
        elif(rl == 'RELEASING'):
            setToReleasing()
        elif(rl == 'CUTTING'):
            setToCutting()
        elif(rl == 'GRABBING'):
            setToGrabbing()
        elif(rl == "SETUP DONE"):
            return rl
        elif(rl == ""):
            pass
        else:
            print('msg recieve='+rl)
            setToDefault()
            return rl

#330 mm for long_x positioning
def long_x_positive():
    print("long_x+ positioning")
    if(serial_write("2") == 'SUCCESS'):
        print('long_x+ success')
        return True
    else:
        print("long_x+ error")
        return False

def long_x_negative():
    print("long_x- positioning")
    if(serial_write("2") == 'SUCCESS'):
        print('long_x- success')
        return True
    else:
        print("long_x- error")
        return False