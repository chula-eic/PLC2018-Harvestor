from easymodbus.modbusClient import ModbusClient
import time

client = ModbusClient('192.168.3.250', 502)
client.connect

def reset():
    client.write_single_coil(0, 1)
    while read_XY != [0, 0]:
        pass
    client.write_single_coil(0, 0)

def read_XY():
    a = client.read_holdingregisters(0,1)
    b = client.read_holdingregisters(10,1)
    return a+b

def is_busy():
    s = client.read_coils(20,1)
    if s[0]: return True
    return False

def drive(x,y):
    if is_busy(): return False
    client.write_single_register(0, x)
    client.write_single_register(10, y)
    client.write_single_coil(10, 1)
    while not is_busy():
        pass
    client.write_single_coil(10, 0)
    return True
