import serial
import config
from time import sleep
config.isCutting,config.isReleasing,config.isGrabbing = False,False,False
config.PORT = 'COM6'
ser = None
def setup():
    global ser
    ser = serial.Serial(config.PORT, 115200, timeout=1)
    st = serial_read()
    while(not st == "SETUP DONE"):
        st=serial_read()
def serial_write(s):
    t = s
    global ser
    if ser is None:
        return "Error"
    ser.write(s.encode('utf-8'))
    return serial_read(t)
def grab():
    print("Grabbing mango")
    if(serial_write("GRAB") == 'SUCCESS'):
        print('Grabbing success')
        return True
    else:
        print("Grabbing error")
        return False
def release():
    print("Releasing mango")
    if(serial_write("RELEASE") == 'SUCCESS'):
        print("Releasing success")
        return True
    else:
        print("Releasing error")
        return False
def cut():
    print("Cutting wire")
    if(serial_write("CUT") == 'SUCCESS'):
        print('Cutting success')
        return True
    else:
        print('Cutting error')
        return False
def forward():
    print('Going Forward')
    if(serial_write("FORWARD") == 'SUCCESS'):
        print('Going forward, success')
        return True
    else:
        print('Going forward, error')
        return False
def backward():
    print('Going Backward')
    if(serial_write("BACKWARD") == 'SUCCESS'):
        print('Going backward, success')
        return True
    else:
        print('Going backward, error')
        return False
def stop():
    print('Stopping')
    if(serial_write("STOP") == 'SUCCESS'):
        print('Stopping success')
        return True
    else:
        print('Stopping error')
        return False

def is_cutting():
    return config.isCutting
def is_releasing():
    return config.isReleasing
def is_grabbing():
    return config.isGrabbing
def status():
    return config.isReady

#PORT = COM3, COM5 , ... somthing something lol
# def serial_read(PORT):
#     ser = serial.Serial(PORT, 38400, timeout=0.1)
#     while True:
#         if ser.isOpen():
#             rl = ser.readline()
#         else:
#             print("Serial is not available")
#             continue
#         try:
#             rl = rl.decode('utf-8')
#         except UnicodeDecodeError:
#             rl = str(rl)
#         if(rl == 'DONE'):
#             return 
def setToReleasing():
    config.isReleasing = True
    config.isCutting,config.isGrabbing,config.isReady = False,False,False
def setToGrabbing():
    config.isGrabbing = True
    config.isCutting,config.isReleasing,config.isReady = False,False,False
def setToCutting():
    config.isCutting = True
    config.isGrabbing,config.isReleasing,config.isReady = False,False,False
def setToDefault():
    config.isCutting,config.isGrabbing,config.isReleasing = False,False,False
    config.isReady = True
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

#if __name__ == '__main__':
#        setup()
#        while(1):
#            forward()
#            sleep(2)
#            stop()
#            sleep(1)
#            backward()
#            sleep(2)
#            stop()
#            sleep(1)
    
