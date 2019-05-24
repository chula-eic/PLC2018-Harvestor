import subprocess as subp
from subprocess import Popen
import os, sys, time
os.chdir(
    "../darknet"
)
cmd = './darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights'
#cmd = 'ls'
p = None
def status():
    global p
    if p == None: 
        return False
    if p.poll() == None:
        return True
    return False
def read_stdout():
    global p
    if(p == None):
        return None
    return p.stdout.read(100000).decode('utf-8')
def start():
    global p
    if status() == True:
        return
    p = subp.Popen(cmd, shell=True, stderr=subp.STDOUT,stdout=subp.PIPE)
def find_mangos():
    global p
    if status() == False:
        return
    out = read_stdout()
    return out
def terminate_process():
    global p
    if(status() == True):
        p.terminate()
        return True
    return False
def clear_buffer():
    global p
    p.stdout.flush()
#test
if __name__ == '__main__':
    start()
    while(True):
        print(find_mangos())
        time.sleep(1)
        clear_buffer()