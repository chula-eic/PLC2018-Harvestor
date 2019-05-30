import PLC
PLC.setup()
while(1):
    mode =  int(input())
    if mode == -1:
        break
    if mode == 0:
        print(PLC.get_XY())
    elif mode == 1:
        PLC.setup()
    elif mode == 2:
        PLC.long_x_positive()
    elif mode == 3:
        PLC.long_x_negative()
    elif mode == 4:
        PLC.short_x_positive()
    elif mode == 5:
        PLC.short_x_negative()
    elif mode == 6:
        PLC.long_y_positive()
    elif mode == 7:
        PLC.long_y_negative()
    elif mode == 8:
        PLC.short_y_positive()
    elif mode == 9:
        PLC.short_y_negative()

