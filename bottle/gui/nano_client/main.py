import tkinter as tk
from iottalk_lib import DAN
from threading import Thread
import time, json
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
sys.path.append('../../')
from syringe_scale import syringe_scale

class medical_GUI:
    def __init__(self, cap):
        # create the window
        self.window = tk.Tk()
        self.window.attributes("-topmost", True)
        self.window.title('IoTtalk')
        self.window.geometry("1024x600")
        # self.window.attributes("-fullscreen", True)
        self.window.update()

        self.__screen_width = self.window.winfo_width()
        self.__screen_height = self.window.winfo_height()
        # print(self.__screen_width, self.__screen_height)
        self.__font_ratio = self.__screen_width/1024
        # print(self.__font_ratio)

        self.cap = cap
        stream = Thread(target=self.webcam_stream, name="medical_webcam_stream")
        stream.setDaemon(True)
        stream.start()
        dm_loop = Thread(target=self.dummy_device_loop, name="medical_iottalk")
        dm_loop.setDaemon(True)
        dm_loop.start()

        self.syringe_scale = syringe_scale()

        self.wait_page()  # first step

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
        # tk.Button(self.window, text=self.text_translate("quit"),
        #           font=('', int(20 * self.__font_ratio), 'bold'),
        #           command=self.quit).place(relx=0.9, rely=0.0, relwidth=0.1, relheight=0.1)

    def text_translate(self, text, language='zh-tw'):
        return text

    def wait_page(self):
        self.clean()
        tk.Label(self.window, text=self.text_translate("針劑藥物辨識系統\n等待指令中..."),
                 font=('', int(80 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    ## Barcode Mode
    def get_barcode(self):  # 輸入欄位
        self.clean()
        tk.Label(self.window, text=self.text_translate("請掃描條碼"),
                 font=('', int(80*self.__font_ratio), 'bold')).place(relx=0.0, rely=0.25, relwidth=1.0, relheight=0.2)
        self.barcode_entry = tk.Entry(self.window, font=('', int(60*self.__font_ratio), 'bold'))
        self.barcode_entry.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.15)
        self.barcode_entry.focus()
        self.barcode_entry.bind('<Return>', self.check_barcode)
    def check_barcode(self, event):
        string = self.barcode_entry.get()
        if not string:  # check the string isn't empty
            self.get_barcode()
        else:
            self.clean()
            tk.Label(self.window, text="條碼編號： "+string,
                     font=('', int(80*self.__font_ratio), 'bold')).place(relx=0.0, rely=0.25, relwidth=1.0, relheight=0.2)
            DAN.push('barcode_result_nano', self.barcode_control_info[0], self.barcode_control_info[1], string)
            tk.Label(self.window, text="上傳中...",
                     font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.6, relwidth=1.0, relheight=0.15)
            self.window.after(3000, lambda: self.wait_page())





    ## Syringe Scale Mode
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
        self.wait_page()

    def show_webcam_stream(self):
        self.frame, scale_value = self.syringe_scale.get_scale(self.last_frame, self.cur_frame, syringe_type="3 ml")

        img_ratio = 1000/self.frame.shape[0]
        cv2image = cv2.cvtColor(cv2.resize(self.frame, None, fx=img_ratio, fy=img_ratio), cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.frame_show.imgtk = imgtk
        self.frame_show.configure(image=imgtk)
        self.frame_show.after(10, self.show_webcam_stream)



    def dummy_device_loop(self):
        ServerURL = 'http://1.iottalk.tw:9999'  # with non-secure connection
        # ServerURL = 'https://DomainName' #with SSL connection
        Reg_addr = "assasassa"  # if None, Reg_addr = MAC address
        DAN.profile['dm_name'] = 'medical_bottle_nano_V2'
        DAN.profile['df_list'] = ['barcode_control_nano', 'syringe_scale_control_nano', 'barcode_result_nano',
                                  'syringe_scale_result_nano', ]
        DAN.profile['d_name'] = 'medical_bottle_nano_ID_01'
        DAN.device_registration_with_retry(ServerURL, Reg_addr)
        # DAN.deregister()  #if you want to deregister this device, uncomment this line
        # exit()            #if you want to deregister this device, uncomment this line
        while True:
            try:
                barcode_control = DAN.pull('barcode_control_nano')  # Pull data from an output device feature "Dummy_Control"
                if barcode_control != None:  ## barcode_control_nano -> [UserName, RandId, True]
                    if barcode_control[-1]:
                        self.barcode_control_info = barcode_control
                        self.get_barcode()
                    else:
                        self.wait_page()

                syringe_scale_control = DAN.pull('syringe_scale_control_nano')  # Pull data from an output device feature "Dummy_Control"
                if syringe_scale_control != None:  ## syringe_scale_control_nano -> [UserName, RandId, SyringeType, True]
                    self.syringe_scale_control_info = syringe_scale_control

            except Exception as e:
                print(e)
                if str(e).find('mac_addr not found:') != -1:
                    print('Reg_addr is not found. Try to re-register...')
                    DAN.device_registration_with_retry(ServerURL, Reg_addr)
                else:
                    print('Connection failed due to unknow reasons.')
                    time.sleep(1)
            time.sleep(0.2)

    def webcam_stream(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        last_ret, self.last_frame = self.cap.read()
        while (True):
            ret, self.cur_frame = self.cap.read()
            # ret, frame = cap.read()
            # height, width, channels = frame.shape
            # print("fps", cap.`get(cv2.CAP_PROP_FPS))
            # print(frame.shape)
            self.last_frame = self.cur_frame



if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    GUI = medical_GUI(cap)
    GUI.run()
    cap.release()


