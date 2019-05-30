# import subprocess
# from subprocess import Popen
import os, sys, time
import config
from pydarknet import Detector, Image
import cv2
import os
import time
import test_color as tc
def load(filename = 'yolov3.weights'):
    dir=""
    return Detector(bytes(dir+"yolo/yolov3.cfg", encoding="utf-8"), bytes(dir+"yolo/"+filename, encoding="utf-8"), 0, bytes(dir+"yolo/coco.data", encoding="utf-8"))

def detect(frame, net):
    mul = 1
    if mul != 1:
        framez = cv2.resize(frame,(0,0), fx=1/mul, fy=1/mul)
    else:
        framez = frame
    start_time = time.time()
    # Only measure the time taken by YOLO and API Call overhead
    dark_frame = Image(framez)
    results = net.detect(dark_frame)
    del dark_frame
    end_time = time.time()
    # print("Elapsed Time:", 1/(end_time-start_time))
    cropped_image = []
    for cat, score, bounds in results:
        x, y, w, h = bounds
        cv2.rectangle(framez, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
        cropped_image.append(framez[int(x-w/2):int(x+w/2),int(y-h/2):int(y+h/2)])
        color = tc.get_color(cropped_image[-1])
        cv2.putText(framez, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
        results.append(
            (
                cat,score,color, (
                    mul*(bounds[0]-bounds[2]/2),mul*(bounds[1]-bounds[3]/2),mul*(bounds[2]),mul*(bounds[3])
                    )
            )
        )
    cv2.imshow("frame", framez)
    #results = [(cat, score, (mul*(bounds[0]-bounds[2]/2),mul*(bounds[1]-bounds[3]/2),mul*(bounds[2]),mul*(bounds[3]))) for cat, score, bounds in results]
    return results


if __name__ == "__main__":
    pass


# 'change working dir to darknet to prepare to launch'
# os.chdir(
#     "../darknet"
# )
# cmd = './darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights'
# #cmd = 'ls'
# config.process =   None
# def status():
    
#     if config.process == None:
#         return False
#     if config.process.poll() == None:
#         return True
#     return False
# def read_stdout():
    
#     if config.process == None:
#         return None
#     return config.process.stdout.read(100000).decode('utf-8')
# def start():
    
#     if status() == True:
#         return
#     config.process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
# def find_mangos():
    
#     if status() == False:
#         return
#     out = read_stdout()
#     return out
# def terminate_process():
    
#     if(status() == True):
#         process.terminate()
#         return True
#     return False
# def clear_buffer():
#     config.process.stdout.flush()
# #test
# if __name__ == '__main__':
#     start()
#     while(True):
#         print(find_mangos())
#         time.sleep(1)
#         clear_buffer()

