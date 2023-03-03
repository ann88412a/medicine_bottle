import tkinter as tk
from tkinter.ttk import Separator, Progressbar
from iottalk_lib import DAN
from threading import Thread
import time, json, statistics, serial
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
# import sys
# sys.path.append('../../')
from syringe_scale import syringe_scale

class medical_GUI:
    def __init__(self, cap, cfg_file_path="./default.cfg"):
        # Load config file
        with open(cfg_file_path, 'r') as __f:
            self.__cfg = json.load(__f)
            __f.close()
        # Setup the serial with arduino light
        self.light = serial.Serial(self.__cfg["arduino_serial_com_port"], self.__cfg["arduino_serial_baud_rates"])  # 初始化序列通訊埠
        self.light.close()
        self.light.open()
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

        self.syringe_scale = syringe_scale(self.__cfg)
        self.wait_page()  # first step

    def run(self):
        self.window.mainloop()

    def quit(self):
        self.window.destroy()
        # self.select_mode()

    def clean(self):
        for child in list(self.window.children.values()):
            child.destroy()
        for widget in self.window.winfo_children():
            widget.configure(state='disabled')  # read only
            widget.destroy()
        self.window.bind('<Escape>', lambda _: self.quit())  # press "Esc" key to close

    def text_translate(self, text, language='zh-tw'):
        return text

    def wait_page(self):
        self.clean()
        self.light.write('0\r\n'.encode())
        tk.Label(self.window, text=self.text_translate("針劑藥物辨識系統\n\n等待中..."),
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
            tk.Label(self.window, text="條碼編號：\n{}\n\n上傳中...".format(string),
                     font=('', int(80*self.__font_ratio), 'bold')).place(relx=0.0, rely=0.1, relwidth=1.0, relheight=0.9)
            DAN.push('barcode_result_nano', self.barcode_control_info[0], self.barcode_control_info[1], string)
            # tk.Label(self.window, text="上傳中...",
            #          font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.6, relwidth=1.0, relheight=0.15)
            self.window.after(3000, lambda: self.wait_page())





    ## Syringe Scale Mode
    def scan_scale(self):
        # self.syringe_scale_control_info = ["aaa", "bbb", "5 ml", "True"]
        self.clean()
        # self.__scale_val = 0
        self.__scale_val_hist_list = []
        self.frame_show = tk.Label(self.window)
        self.frame_show.place(relx=0.0, rely=0.0, relwidth=0.3, relheight=1.0)

        tk.Label(self.window, text=self.text_translate("請將針具放置於固定平台"),
                 font=('', int(28 * self.__font_ratio), 'bold')).place(relx=0.31, rely=0.0, relwidth=0.69, relheight=0.1)

        self.__syringe_hint_imagetk = ImageTk.PhotoImage(Image.open('./images/HW_V2_with_syringe.png').resize(
            (int(self.__screen_width * 0.69), int(self.__screen_height * 0.69))))
        tk.Label(self.window, image=self.__syringe_hint_imagetk).place(relx=0.31, rely=0.1, relwidth=0.69, relheight=0.69)

        tk.Label(self.window, text=self.text_translate("針具樣式： {}".format(self.syringe_scale_control_info[-2])), anchor="w",
                 font=('', int(28 * self.__font_ratio), 'bold')).place(relx=0.31, rely=0.8, relwidth=0.34, relheight=0.1)
        self.frame_show_val = tk.Label(self.window, text=self.text_translate("辨識數值："), anchor="w",
                 font=('', int(28 * self.__font_ratio), 'bold'))
        self.frame_show_val.place(relx=0.31, rely=0.9, relwidth=0.34, relheight=0.1)
        tk.Label(self.window, text=self.text_translate("辨識進度："), anchor="w",
                 font=('', int(28 * self.__font_ratio), 'bold')).place(relx=0.66, rely=0.8, relwidth=0.34, relheight=0.1)
        self.scale_running_bar = Progressbar(self.window, mode="determinate", orient='horizontal')
        self.scale_running_bar.place(relx=0.66, rely=0.91, relwidth=0.33, relheight=0.08)
        self.scale_running_bar['value'] = 0
        Separator(self.window, orient=tk.HORIZONTAL).place(relx=0.3, rely=0.8, relwidth=0.7)  # HORIZONTAL建立水平分隔线，VERTICAL建立垂直分隔线
        Separator(self.window, orient=tk.VERTICAL).place(relx=0.3, rely=0.0, relheight=1.0)  # HORIZONTAL建立水平分隔线，VERTICAL建立垂直分隔线
        Separator(self.window, orient=tk.VERTICAL).place(relx=0.649, rely=0.8, relheight=0.2)  # HORIZONTAL建立水平分隔线，VERTICAL建立垂直分隔线
        self.show_webcam_stream()

    def show_webcam_stream(self):
        self.scale_frame, self.scale_value = self.syringe_scale.get_scale(self.last_frame, self.cur_frame, syringe_type=self.syringe_scale_control_info[-2])

        img_ratio = 0.98 * min(self.__screen_height/self.scale_frame.shape[0], 0.3*self.__screen_width/self.scale_frame.shape[1])
        cv2image = cv2.cvtColor(cv2.resize(self.scale_frame, None, fx=img_ratio, fy=img_ratio), cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.frame_show.imgtk = imgtk
        self.frame_show.configure(image=imgtk)
        self.frame_show_val.config(text=self.text_translate("辨識數值： {}".format(self.scale_value)))
        self.frame_show.after(30, self.show_webcam_stream)
        self.scan_scale_auto_finish(self.scale_value)

    def scan_scale_auto_finish(self, scale_value):  # push data while scale value stable
        # print(time.time())
        if scale_value is not None:
            self.__scale_val_hist_list.append(scale_value)
            self.scale_running_bar['value'] = len(self.__scale_val_hist_list)*0.8
            if(len(self.__scale_val_hist_list) > 100):
                __mean = statistics.mean(self.__scale_val_hist_list)
                __median = statistics.median(self.__scale_val_hist_list)
                if __mean/__median > 1:
                    self.scale_running_bar['value'] = 80 + __median/__mean*20
                else:
                    self.scale_running_bar['value'] = 80 + __mean/__median*20
                if(abs(__median - scale_value) < 0.001 and abs(__mean - __median) < 0.001): ## finished and push
                    self.clean()
                    # cv2.imwrite("{}/{}_{}_{}_{}_{}.jpg".format(self.__cfg["syringe_scale_img_save_path"], time.strftime("%Y%d%m%H%M%S", time.localtime()),
                    #                                self.syringe_scale_control_info[0], self.syringe_scale_control_info[1],
                    #                                self.syringe_scale_control_info[2].replace(" ", ""), scale_value), self.cur_frame)
                    # self.light.write('0'.encode())
                    DAN.push('syringe_scale_result_nano', self.syringe_scale_control_info[0],
                             self.syringe_scale_control_info[1], self.syringe_scale_control_info[2], scale_value)
                    tk.Label(self.window, text=self.text_translate("針筒樣式: {}".format(self.syringe_scale_control_info[-2])), anchor="w",
                             font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.2)
                    tk.Label(self.window, text=self.text_translate("辨識結果: {}".format(scale_value)), anchor="w",
                             font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.2)
                    tk.Label(self.window, text=self.text_translate("上傳中..."), anchor="e",
                             font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.8, relwidth=1.0, relheight=0.2)
                    self.window.after(3000, lambda: self.wait_page())
                    # self.wait_page()
                else:
                    if max(self.__scale_val_hist_list) - __median > min(self.__scale_val_hist_list) - __median:
                        pop_num = max(self.__scale_val_hist_list)
                    else:
                        pop_num = min(self.__scale_val_hist_list)
                    self.__scale_val_hist_list.pop(self.__scale_val_hist_list.index(pop_num))




    def dummy_device_loop(self):
        ServerURL = self.__cfg["ServerURL"]  # with non-secure connection
        Reg_addr = self.__cfg["Reg_addr"]  # if None, Reg_addr = MAC address
        DAN.profile['dm_name'] = "medical_bottle_nano_V2"
        DAN.profile['df_list'] = ['barcode_control_nano', 'syringe_control_nano', 'barcode_result_nano', 'syringe_scale_result_nano', ]
        DAN.profile['d_name'] = self.__cfg["d_name"]
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

                syringe_scale_control = DAN.pull('syringe_control_nano')  # Pull data from an output device feature "Dummy_Control"
                if syringe_scale_control != None:  ## syringe_scale_control_nano -> [UserName, RandId, SyringeType, True]
                    if syringe_scale_control[-1]:
                        self.light.write('255\r\n'.encode())
                        self.syringe_scale_control_info = syringe_scale_control
                        self.scan_scale()
                    else:
                        self.wait_page()

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


