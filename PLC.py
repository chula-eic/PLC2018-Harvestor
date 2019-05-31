import serial
import config
from time import sleep
config.x = 0
config.y = 0
config.PORT = '/dev/ttyACM0'
ser = None
def setup():
    global ser
    ser = serial.Serial(config.PORT, 9600, timeout=1)
    st = serial_read()
    print(st)
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
        if(rl == "2" or rl == "3" or rl == "4" or rl == "5" or rl == "6" or rl == "7" or rl == "8" or rl == "9"):
           print('POSITIONING DONE')
           return('SUCCESS')
        elif(rl == "SETUP DONE"):
            return rl
        elif(rl == ""):
            pass
        else:
            print('msg recieve='+rl)
            return rl

def get_XY():
    return [config.x, config.y]

def reset():
    if(serial.writeTimeoutError("0") == "RST"):
        config.x = 0
        config.y = 0

#300 mm for long_x positioning
def long_x_positive():
    print("long_x+ positioning")
    if config.x > 700:
        print("out of range long_x+")
        return false
    if(serial_write("2") == 'SUCCESS'):
        print('long_x+ success')
        config.x += 300
        return True
    else:
        print("long_x+ error")
        return False

def long_x_negative():
    print("long_x- positioning")
    if config.x < 300:
        print("out of range long_x-")
        return False
    if(serial_write("3") == 'SUCCESS'):
        print('long_x- success')
        config.x -= 300
        return True
    else:
        print("long_x- error")
        return False
#50mm for short_x positioning
def short_x_positive():
    print("short_x+ positioning")
    if config.x > 950:
        print("out of range short_x+")
        return False
    if(serial_write("4") == 'SUCCESS'):
        print('short_x+ success')
        config.x += 50
        return True
    else:
        print("short_x+ error")
        return False
def short_x_negative():
    print("short_x- positioning")
    if config.x < 50:
        print("out of range short_x-")
        return False
    if(serial_write("5") == 'SUCCESS'):
        print('short_x- success')
        config.x -= 50
        return True
    else:
        print("short_x- error")
        return False

#200mm for long_y positioning
def long_y_positive():
    print("long_y+ positioning")
    if config.y > 350:
        print("out of range long_y+")
        return False
    if(serial_write("6") == 'SUCCESS'):
        print('long_y+ success')
        config.y += 200
        return True
    else:
        print("long_y+ error")
        return False
def long_y_negative():
    print("long_y- positioning")
    if config.y < 200:
        print("out of range long_y-")
        return False
    if(serial_write("7") == 'SUCCESS'):
        print('long_y- success')
        config.y -= 200
        return True
    else:
        print("long_y- error")
        return False

#50mm for short_y positioning
def short_y_positive():
    print("short_y+ positioning")
    if config.y > 500:
        print("out of range short_y+")
        return False
    if(serial_write("8") == 'SUCCESS'):
        print('short_y+ success')
        config.y += 50
        return True
    else:
        print("short_y+ error")
        return False
def short_y_negative():
    print("short_y- positioning")
    if config.y < 50:
        print("out of range short_y-")
        return False
    if(serial_write("9") == 'SUCCESS'):
        print('short_y- success')
        config.y -= 50
        return True
    else:
        print("short_y- error")
        return False
if __name__ == '__main__':
    setup()
    # for i in range(20):
    #     short_y_positive()
    #     short_y_negative()
    # long_x_positive()
    long_x_negative()
    