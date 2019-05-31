import tkinter as tk



class MainApplication(tk.Frame):
   def __init__(self, master):
       self.master = master
       tk.Frame.__init__(self, self.master)
       self.configure_gui()
       self.create_widgets()

   def configure_gui(self):
       self.master.title('Simple layout')
       self.master.geometry('440x140')
       self.master.resizable(0, 0)

   def create_widgets(self):
       self.create_frames()
       self.create_buttons()

   def create_frames(self):
       self.left_frame = tk.Frame(width=140, height=140, background='red')
       self.left_frame.grid_propagate(0)
       self.left_frame.grid(row=0, column=0)

       self.right_frame = tk.Frame(width=300, height=140, background='gold2')
       self.right_frame.grid_propagate(0)
       self.right_frame.grid(row=0, column=1)   

   def create_buttons(self):
       self.create_left_frame_buttons()
       self.create_right_frame_buttons()       

   def create_left_frame_buttons(self):
       self.button1 = tk.Button(self.left_frame, text='Button1')       
       self.button1.grid(row=0, column=0, padx=30, pady=20)

       self.button2 = tk.Button(self.left_frame, text='Button2')       
       self.button2.grid(row=1, column=0, padx=30, pady=20)       

   def create_right_frame_buttons(self):
       self.button1 = tk.Button(self.right_frame, text='Button3')       
       self.button1.grid(row=0, column=0, padx=20, pady=50)

       self.button2 = tk.Button(self.right_frame, text='Button4')       
       self.button2.grid(row=0, column=1, padx=70)


if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()