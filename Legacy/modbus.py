from easymodbus.modbusClient import ModbusClient
import time
#make sure X5 swith on PLC is on before execute any modbus command
#else the PLC will not listen properly
#X0, X1, X2 and X3 is manual movement
#X4 is manual reset which work the same way as reset()
#X5 is toggle for auto and manual mode
#PLC will only accept modbus command in auto mode
#and will only accept manual commant in mannual mode

client = ModbusClient('192.168.3.250', 502)
client.connect


#reset x and y coordinate
def reset():
    client.write_single_coil(0, 1)
    while read_XY != [0, 0]:
        pass
    client.write_single_coil(0, 0)

#read x and y coordinate from PLC
#will return a list [x,y]
def read_XY():
    a = client.read_holdingregisters(0,1)
    b = client.read_holdingregisters(10,1)
    return a+b

#PLC will not accept any command whan it's busy
def is_busy():
    s = client.read_coils(20,1)
    if s[0]: return True
    return False

#drive(int x coordinate, int y coordinate)
#x must be between 0 and 10000
#y must be between 0 and 6000
def drive(x,y):
    if is_busy(): return False
    client.write_single_register(0, x)
    client.write_single_register(10, y)
    client.write_single_coil(10, 1)
    while not is_busy():
        pass
    client.write_single_coil(10, 0)
    return True

if __name__ == "__main__":
    reset()
    while(1):
        if drive(1000, 1000):
            break
    while(1):
        if drive(0, 0):
            break
