import tkinter as tk
from tkinter import CENTER, ttk
import time
from tkinter import font

LARGEFONT =("Verdana", 50)

  
class tkinterApp(tk.Tk):
     
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2,Page3):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# first window frame startpage
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        t0 = time.time()
        def ready():
            if time.time() - t0 >5:
                label.config(text = "開機完成")
                label.grid(row = 0, column = 0)
                button1 = tk.Button(self, text ="開始",command = lambda : controller.show_frame(Page1), font = LARGEFONT)
                button1.grid(row = 1, column = 0,sticky=tk.E)
                
            else:
                label.config(text = "開機中"+str(time.time()))
                label.after(1,ready)
        # label of frame Layout 2
        label = ttk.Label(self, text ="開機中", font = LARGEFONT)
        ready()
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 0,sticky=tk.E)
        
       
    
  
          
  
  
# second window frame page1
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="請先放入藥丸再按開始辨識", font = LARGEFONT)
        label.grid(row = 0, column = 0)
  
        # button to show frame 2 with text
        # layout2
        button1 = tk.Button(self, text ="開始辨識",
                            command = lambda : controller.show_frame(Page2),font = LARGEFONT)
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 0)
  
        # button to show frame 2 with text
        # # layout2
        # button2 = ttk.Button(self, text ="Page 2",
        #                     command = lambda : controller.show_frame(Page2))
     
        # # putting the button in its place by
        # # using grid
        # button2.grid(row = 2, column = 1)
  
  
  
  
# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="辨識中", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        t1 = time.time()
        def ready():
            if time.time() - t1 >5:
                label.config(text = "開機完成")
                label.grid(row = 0, column = 0)
                button1 = tk.Button(self, text ="確認結果",command = lambda : controller.show_frame(Page3), font = LARGEFONT)
                button1.grid(row = 1, column = 0,sticky=tk.E)
                
            else:
                label.config(text = "辨識中"+str(time.time() - t1))
                label.after(1,ready)
        label = ttk.Label(self, text ="辨識中", font = LARGEFONT)
        ready()
        # button to show frame 2 with text
        # layout2
        # button1 = ttk.Button(self, text ="Page 1",
        #                     command = lambda : controller.show_frame(Page1))
     
        # # putting the button in its place by
        # # using grid
        # button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # # button to show frame 3 with text
        # # layout3
        # button2 = ttk.Button(self, text ="Startpage",
        #                     command = lambda : controller.show_frame(StartPage))
     
        # # putting the button in its place by
        # # using grid
        # button2.grid(row = 2, column = 1, padx = 10, pady = 10,sticky='')

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="確認放入藥丸", font = LARGEFONT)
        label.grid(row = 0, column = 0)

        chk1 = tk.Checkbutton(self,text='Sennosid',var=tk.BooleanVar,font=LARGEFONT)
        chk1.grid(row=1,column=0)
        chk2 = tk.Checkbutton(self,text='Apresoline',var=tk.BooleanVar, font=LARGEFONT)
        chk2.grid(row=2,column=0)
        chk3 = tk.Checkbutton(self,text='Repaglinide',var=tk.BooleanVar,font=LARGEFONT)
        chk3.grid(row=3,column=0)
        chk4 = tk.Checkbutton(self,text='Cataflam',var=tk.BooleanVar,font = LARGEFONT)
        chk4.grid(row=4,column=0)



        
        button1 = ttk.Button(self, text ="確認",
                            command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
     
  
# Driver Code
app = tkinterApp()
app.geometry("1080x960")
app.title('藥丸辨識')
app.mainloop()

# from tkinter import *
# from tkinter.ttk import *
 
# # importing strftime function to
# # retrieve system's time
# from time import strftime
 
# # creating tkinter window
# root = Tk()
# root.title('Clock')
 
# # This function is used to
# # display time on the label
# def time1():
#     string = strftime('%H:%M:%S %p')
#     lbl.config(text = string)
#     lbl.after(1000, time1)
#     this_t.config(text = str(time.time()))
#     this_t.after(1000,time1)
# # Styling the label widget so that clock
# # will look more attractive
# lbl = Label(root, font = ('calibri', 40, 'bold'),
#             background = 'purple',
#             foreground = 'white')
# this_t = Label(root, font = ('calibri', 40, 'bold'),
#             background = 'purple',
#             foreground = 'white')
 
# # Placing clock at the centre
# # of the tkinter window
# this_t.pack()
# lbl.pack()
# time1()
 
# mainloop()