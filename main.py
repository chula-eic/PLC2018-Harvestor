## main.py version 0.2.0

import logging
import numpy as np
import json

test = False

if test:
    import test_arm as arm
    import test_modbus as modbus
    import test_vision as vision
else:
    import arm
    import PLC
    import vision


print("CONFIGUE")
basket = {}

with open("mainConfig.json", "r") as config_file:
    config = json.load(config_file)
    x_yellow = config['x_yellow']
    y_yellow = config['y_yellow']
    x_brown = config['x_brown']
    y_brown = config['y_brown']
    x_min = config['x_min']
    x_max = config['x_max']
    x_long = config['x_long']
    x_short = config['x_short']
    x_error = config['x_error']
    y_min = config['y_min']
    y_max = config['y_max']
    y_long = config['y_long']
    y_short = config['y_short']
    y_error = config['y_error']

print("RESET POSITION TO 0, 0, 0")
# modbus.reset()

print("HARVEST")

x_camera = x_min
dir_x = 1
loop_end = False

for y_camera in range(y_min, y_max + y_interval, y_interval):

    if y_camera >= y_max:

        y_camera = y_max
        loop_end = True
        
    while True:

        ## save x, y point
        x_save = x_camera
        y_save = y_camera
        
        while True:

            mangos = vision.find_mangos()
            if len(mangos) > 0:

                ## find nearest mango
                nearest_mango = mangos[0]
                nearest_distant_square = nearest_mango[0]**2 + nearest_mango[1]**2
                for mango in mangos:
                    distant_square = mango[0]**2 + mango[1]**2
                    if distant_square <= nearest_distant_square:
                        nearest_mango = mango
                        nearest_distant_square = distant_square

                x_mango = nearest_mango[0]
                y_mango = nearest_mango[1]

                print("FOUND MANGO", color, "AT", x_mango, y_mango)

                if abs(x_mango) > x_error or abs(y_mango) > y_error:

                    ## visual servo 
                    x_camera += x_mango
                    y_camera += y_mango
                    modbus.drive(x_camera, y_camera)

                else:

                    color = vision.get_color()

                    if color == vision.yellow:

                        arm.grab()
                        modbus.drive(x_yellow, y_yellow)
                        arm.release()

                    elif color == vision.brown:

                        arm.grab()
                        modbus.drive(x_brown, y_brown)
                        arm.release()

                    else:

                        pass

                    modbus.drive(x_save, y_save)

            else:

                ## mango not found
                break

        ## return to saved point
        x_camera = x_save
        y_camera = y_save

        if x_camera + x_interval*dir_x < x_min:
            dir_x = 1
            break
        elif x_camera + x_interval*dir_x > x_max:
            dir_x = -1
            break
        else:
            x_camera += x_interval*dir_x

    if loop_end: break

print("RESULT : COLOR( " + str(vision.yellow)+ " )" + str(basket[vision.yellow]))
print("RESULT : COLOR( " + str(vision.brown)+ " )" + str(basket[vision.brown]))

