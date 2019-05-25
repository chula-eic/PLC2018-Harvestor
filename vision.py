import subprocess
from subprocess import Popen
import os, sys, time
import config

'change working dir to darknet to prepare to launch'
os.chdir(
    "../darknet"
)
cmd = './darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights'
#cmd = 'ls'
config.process =   None
def status():
    
    if config.process == None:
        return False
    if p.poll() == None:
        return True
    return False
def read_stdout():
    
    if config.process == None:
        return None
    return process.stdout.read(100000).decode('utf-8')
def start():
    
    if status() == True:
        return
    config.process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
def find_mangos():
    
    if status() == False:
        return
    out = read_stdout()
    return out
def terminate_process():
    
    if(status() == True):
        process.terminate()
        return True
    return False
def clear_buffer():
    config.process.stdout.flush()
#test
if __name__ == '__main__':
    start()
    while(True):
        print(find_mangos())
        time.sleep(1)
        clear_buffer()