import serial
import config
config.isCutting,config.isReleasing,config.isGrabbing = False,False,False
config.PORT = 'COM3'
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
def close_in():
    print('Closing in on Mango.')
    'gg ez'
def back_out():
    print('Backing out from the tree')

def is_cutting():
    return config.isCutting
def is_releasing():
    return config.isReleasing
def is_grabbing():
    return config.isGrabbing
def is_closing_in():
    return config.isClosingIn
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
def serial_write(cmd):
    ser = serial.Serial(config.PORT, 38400, timeout=0.1)
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
        elif(rl == 'RELEASING'):
            setToReleasing()
        elif(rl == 'CUTTING'):
            setToCutting()
        elif(rl == 'GRABBING'):
            setToGrabbing()
        else:
            print('Undefined')
            setToDefault()
            return 'ERROR'