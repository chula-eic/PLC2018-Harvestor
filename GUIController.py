import tkinter as tk
import PLC
import arm
#import main
#import main2
#import vision
import os

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class MainApplication(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title('PLC Controller')
        self.master.geometry('500x500')
        self.master.resizable(0, 0)

    def create_widgets(self):
        self.create_frames()
        self.create_buttons()

    def create_frames(self):
        self.left_frame = tk.Frame(width=250, height=500, background='skyblue')
        self.left_frame.grid_propagate(0)
        self.left_frame.grid(row=0, column=0)

        self.right_frame = tk.Frame(width=250, height=500, background='pink')
        self.right_frame.grid_propagate(0)
        self.right_frame.grid(row=0, column=1)

    def create_buttons(self):
        self.create_left_frame_buttons()
        self.create_right_frame_buttons()       
    
    def create_left_frame_buttons(self):

        self.button1 = tk.Button(self.left_frame, text='X+300',activeforeground='green',command=PLC.long_x_positive)       
        self.button1.config( height = 5, width = 10 )
        self.button1.grid(row=0, column=0, padx=5, pady=10)

        self.button2 = tk.Button(self.left_frame, text='X+50',activeforeground='green',command=PLC.short_x_positive)       
        self.button2.config( height = 5, width = 10 )
        self.button2.grid(row=0, column=1, padx=5, pady=10)

        self.button3 = tk.Button(self.left_frame, text='Y+200',activeforeground='green',command=PLC.long_y_positive)    
        self.button3.config( height = 5, width = 10 )   
        self.button3.grid(row=1, column=0, padx=5, pady=10)  

        self.button4 = tk.Button(self.left_frame, text='Y+50',activeforeground='green',command=PLC.short_y_positive)       
        self.button4.config( height = 5, width = 10 )
        self.button4.grid(row=1, column=1, padx=5, pady=10)  
        
        self.button9 = tk.Button(self.left_frame, text='Main\nProgram',activeforeground='yellow',command=run_main)     
        self.button9.config( height = 5, width = 10 )
        self.button9.grid(row=2, column=0, padx=5, pady=10)

        self.button10 = tk.Button(self.left_frame, text='Main2\nProgram',activeforeground='yellow',command=run_main2)       
        self.button10.config( height = 5, width = 10 )
        self.button10.grid(row=2, column=1, padx=5, pady=10)  

        self.stopButton = tk.Button(self.left_frame, text="STOP",activeforeground='red',command=PLC.stop)
        self.stopButton.config( height=5, width=20)
        self.stopButton.grid(row=3, column=0, columnspan=2)

    def create_right_frame_buttons(self):
        self.button5 = tk.Button(self.right_frame, text='X-300',activeforeground='red')
        self.button5.config( height = 5, width = 10) 
        self.button5.grid(row=0, column=0, padx=5, pady=10)

        self.button6 = tk.Button(self.right_frame, text='X-50',activeforeground='red')       
        self.button6.config( height = 5, width = 10 )
        self.button6.grid(row=0, column=1, padx=5, pady=10)

        self.button7 = tk.Button(self.right_frame, text='Y-200',activeforeground='red')       
        self.button7.config( height = 5, width = 10 )
        self.button7.grid(row=1, column=0, padx=5, pady=10)

        self.button8 = tk.Button(self.right_frame, text='Y-50',activeforeground='red')       
        self.button8.config( height = 5, width = 10 )
        self.button8.grid(row=1, column=1, padx=5, pady=10)

        self.button11 = tk.Button(self.right_frame, text='Gripper\ncut',activeforeground='blue')       
        self.button11.config( height = 5, width = 10 )
        self.button11.grid(row=2, column=0, padx=5, pady=10)

        self.button12 = tk.Button(self.right_frame, text='Gripper\nRelease',activeforeground='blue')       
        self.button12.config( height = 5, width = 10 )
        self.button12.grid(row=2, column=1, padx=5, pady=10)
        
        self.button13 = tk.Button(self.right_frame, text='Arm Forward',activeforeground='purple')       
        self.button13.config( height = 5, width = 10 )
        self.button13.grid(row=3, column=0, padx=5, pady=10)

        self.button14 = tk.Button(self.right_frame, text='Arm Backward',activeforeground='purple')       
        self.button14.config( height = 5, width = 10 )
        self.button14.grid(row=3, column=1, padx=5, pady=10)

def run_main():
    os.system('python3 main.py')

def run_main2():
    os.system('python3 main2.py')

if __name__ == '__main__':
    root = tk.Tk()
    main_app =  MainApplication(root)
    root.mainloop()
