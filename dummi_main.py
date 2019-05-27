import numpy 

def mango(x_max,y_max):
    y=0
    x=0
    while True :
        drive(x, y)
        z = get_mangos()
        n = len(z)
        if n != 0 :
            for i in range(0,n):
                xi = z[i][0]+(z[i][2]//2)
                yi = z[i][1]+(z[i][3]//2)
                drive(xi,yi)
                grab()
                collect(z[i][4])
        if x != x_max : x = x+1
        else: 
            x=0
            if y != y_max : y = y+1 
            else : 
                break 

