from easymodbus.modbusClient import ModbusClient
import time

client = ModbusClient('192.168.3.250', 502)
client.connect

def read_XY():
    a = client.read_holdingregisters(0,1)
    L.append(a)
    b = client.read_holdingregisters(1,1)
    L.append(b)
    return a+b

def is_busy():
    s = client.read_coils(0,1)
    if s[0]: return True
    return False
def drive(x,y):
    pass
