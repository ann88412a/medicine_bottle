import tkinter as tk
try:
    # fix opencv open webcam slowly bug in WIN10
    import os
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    # call cv2 in WIN10
    from cv2 import cv2
except:
    # call cv2 in jetson nano
    import cv2
from PIL import Image, ImageTk
import sys
sys.path.append('../')
from bottle.syringe_scale import syringe_scale

class medical_GUI:
    def __init__(self, cap):
        # setup the webcam
        self.cap = cap
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        # create the window
        self.window = tk.Tk()
        self.window.attributes("-topmost", True)
        self.window.title('IoTtalk')
        # self.window.geometry("1024x600")
        self.window.attributes("-fullscreen", True)
        self.window.update()

        self.__screen_width = self.window.winfo_width()
        self.__screen_height = self.window.winfo_height()
        # print(self.__screen_width, self.__screen_height)
        self.__font_ratio = self.__screen_width/1024
        # print(self.__font_ratio)

        self.syringe_scale = syringe_scale()

        self.select_mode()  # first step

    def run(self):
        self.window.mainloop()

    def quit(self):
        self.window.destroy()
        # self.select_mode()

    def clean(self):
        for widget in self.window.winfo_children():
            widget.configure(state='disabled')  # read only
            # widget.pack_forget()
            widget.destroy()
        tk.Button(self.window, text=self.text_translate("quit"),
                  font=('', int(20 * self.__font_ratio), 'bold'),
                  command=self.quit).place(relx=0.9, rely=0.0, relwidth=0.1, relheight=0.1)

    def text_translate(self, text, language='zh-tw'):
        return text

    def select_mode(self):
        self.clean()
        tk.Label(self.window, text=self.text_translate("Select Mode"),
                 font=('', int(28 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=0.9, relheight=0.1)
        tk.Button(self.window, text=self.text_translate("pill"), font=('',int(100*self.__font_ratio), 'bold'),
                  command=self.pill_mode, state='disabled').place(relx=0.025, rely=0.4, relwidth=0.4, relheight=0.5)
        tk.Button(self.window, text=self.text_translate("bottle"), font=('', int(100*self.__font_ratio), 'bold'),
                  command=self.bottle_mode).place(relx=0.475, rely=0.4, relwidth=0.4, relheight=0.5)



    ## Pill Mode
    def pill_mode(self):
        # print("pill mode")
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # self.clean()
        pass


    ## Bottle Mode
    def bottle_mode(self):
        # print("bottle mode")
        self.clean()
        self.get_barcode()

    def get_barcode(self):  # 輸入欄位
        self.clean()
        tk.Label(self.window, text=self.text_translate("Please scan the barcode"),
                 font=('', int(30*self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=0.9, relheight=0.1)
        self.barcode_entry = tk.Entry(self.window, font=('',int(10*self.__font_ratio), 'bold'))
        self.barcode_entry.place(relx=0.1, rely=0.1, relwidth=0.7, relheight=0.05)
        self.barcode_entry.focus()
        self.barcode_entry.bind('<Return>', self.check_barcode)

    def check_barcode(self, event):
        string = self.barcode_entry.get()
        if not string:  # check the string isn't empty
            self.get_barcode()
        else:
            self.clean()
            tk.Label(self.window, text=string,
                     font=('', int(40*self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=0.9, relheight=0.1)
            tk.Button(self.window, text=self.text_translate("Redo"), font=('',int(100*self.__font_ratio), 'bold'),
                      command=self.get_barcode).place(relx=0.025, rely=0.4, relwidth=0.4, relheight=0.5)
            tk.Button(self.window, text=self.text_translate("Next"), font=('',int(100*self.__font_ratio), 'bold'),
                      command=self.scan_scale).place(relx=0.475, rely=0.4, relwidth=0.4, relheight=0.5)

    def ask_diluent(self):
        pass
            # 少了稀釋選項
            # diluent


    def scan_scale(self, mode='medicine'):
        self.clean()
        tk.Label(self.window, text=self.text_translate("Place syringe with "+mode+" on white setup"),
                 font=('', int(28 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=0.9, relheight=0.1)
        tk.Button(self.window, text=self.text_translate("done"), font=('', int(20*self.__font_ratio), 'bold'),
                  command=self.__quit_show_webcam_stream).place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1)
        self.frame_show = tk.Label(self.window)
        self.frame_show.place(relx=0.0, rely=0.1)

        self.show_webcam_stream()

    def __quit_show_webcam_stream(self):
        self.clean()
        self.webcam_stream_show = False
        # self.frame_show.destroy()
        self.select_mode()

    def show_webcam_stream(self):
        _, self.frame = self.cap.read()
        # print(self.frame.shape)
        # print(self.frame.shape)
        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_CLOCKWISE)
        # print(self.frame.shape)  # (960, 720, 3)
        self.frame = self.syringe_scale.get_scall_raw(self.frame)
        img_ratio = self.__screen_height/self.frame.shape[0]*0.9*0.995
        cv2image = cv2.cvtColor(cv2.resize(self.frame, None, fx=img_ratio, fy=img_ratio), cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.frame_show.imgtk = imgtk
        self.frame_show.configure(image=imgtk)
        self.frame_show.after(10, self.show_webcam_stream)





if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    GUI = medical_GUI(cap)


    GUI.run()
    cap.release()

