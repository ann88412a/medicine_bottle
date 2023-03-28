import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Separator, Progressbar
import time, json, statistics, os, cv2
import urllib.request
from PIL import Image, ImageTk
from threading import Thread
from .syringe_scale import syringe_scale
from .webcam_video_stream import medical_webcam_stream
from .light_control import light_control
from . import DAN

# print(os.getcwd())

class medical_GUI:
    def __init__(self, cfg_file_path="./config_files/syringe_scale_default.cfg"):
        self.DEBUG = True
        ## Load config file
        with open(cfg_file_path, 'r') as __f:
            self.__cfg = json.load(__f)
            __f.close()
        ## instantiated the other func class
        self.syringe_scale = syringe_scale(self.__cfg)
        self.light = light_control(self.__cfg["arduino_serial_com_port"], self.__cfg["arduino_serial_baud_rates"])
        self.webcam_stream = medical_webcam_stream()
        ## start the IoTtalk DAI loop
        dm_loop = Thread(target=self.dummy_device_loop, name="medical_iottalk")
        dm_loop.setDaemon(True)
        dm_loop.start()
        ## create the window
        self.window = tk.Tk()
        self.window.title('Medical Talk')
        if self.DEBUG:
            self.window.geometry("1024x600")
        else:
            self.window.attributes("-fullscreen", True)
            self.window.attributes("-topmost", True)
        self.window.update()
        self.window.bind('<Escape>', lambda _: self.quit())  # press "Esc" key to close
        self.window.bind('<ButtonPress-1>', self.sys_options_long_press_event)  # long press to quit (3s)
        self.window.bind('<ButtonRelease-1>', self.sys_options_long_press_event)
        self.__screen_width = self.window.winfo_width()
        self.__screen_height = self.window.winfo_height()
        self.__font_ratio = self.__screen_width / 1024
        if self.DEBUG:
            print("Screen size(w*h): {} * {}".format(self.__screen_width, self.__screen_height))

    def run(self):
        ## run check all state before start
        self.start_up_check()
        ## run GUI
        self.window.mainloop()
        ## release cam after done
        self.webcam_stream.cap.release()

    def quit(self):
        if(messagebox.askyesno("Close app", "Quit?")):
            self.window.destroy()

    def sys_options_long_press_event(self, event=None):
        if event is None:
            self.sys_options()
            self.__id_of_sys_options_long_press_after_event = None
        elif event.type == tk.EventType.ButtonPress:
            self.__id_of_sys_options_long_press_after_event = self.window.after(3000, self.sys_options_long_press_event)
        elif self.__id_of_sys_options_long_press_after_event:
            self.window.after_cancel(self.__id_of_sys_options_long_press_after_event)
            self.__id_of_sys_options_long_press_after_event = None

    def sys_shutdown(self):
        if(messagebox.askyesno("Power off", "Power off?")):
            self.window.destroy()
            os.system('systemctl poweroff')

    def sys_reboot(self):
        if(messagebox.askyesno("Reboot", "Reboot?")):
            self.window.destroy()
            os.system('systemctl reboot')

    def sys_options(self):
        self.clean()
        tk.Button(self.window, text='poweroff', font=('', int(40 * self.__font_ratio), 'bold'), command=lambda: [self.sys_shutdown()]).place(relx=0.025, rely=0.2, relwidth=0.3, relheight=0.3)
        tk.Button(self.window, text='reboot', font=('', int(40 * self.__font_ratio), 'bold'), command=lambda: [self.sys_reboot()]).place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.3)
        tk.Button(self.window, text='結束APP', font=('', int(40 * self.__font_ratio), 'bold'), command=lambda: [self.quit()]).place(relx=0.675, rely=0.2, relwidth=0.3, relheight=0.3)
        tk.Button(self.window, text='取消', font=('', int(40 * self.__font_ratio), 'bold'), command=lambda: [self.check_network(self.__cfg["ServerURL"]), self.wait_page()]).place(relx=0.8, rely=0.8, relwidth=0.2, relheight=0.2)

    def clean(self):
        for child in list(self.window.children.values()):
            child.destroy()
        for widget in self.window.winfo_children():
            widget.configure(state='disabled')  # read only
            widget.destroy()

    def text_translate(self, text, language='zh-tw'):
        return text

    def wait_page(self):
        self.clean()
        self.light.light_off()
        tk.Label(self.window, text=self.text_translate("針劑藥物辨識系統\n\n等待中..."),
                 font=('', int(80 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    def start_up_check(self):
        try:
            assert self.check_network(URL=self.__cfg["ServerURL"], show_GUI=False), "Failed to connect to the IoTtalk server!"
            assert self.light.check_light_state(), "Failed with the light control serial error!"
            assert self.webcam_stream.check_cam_ready(), "Failed with the webcam streaming error!"
            self.wait_page()  # first step
            # self.scan_scale()
        except AssertionError as error:
            self.window.destroy()
            print("#############################")
            print(error)
            print("#############################")

        except BaseException as e:
            self.window.destroy()
            print("#############################")
            print("Failed with an unknown error!")
            print("Error msg:", e)
            print("#############################")





    ## Barcode Mode
    def get_barcode(self):  # 輸入欄位
        self.clean()
        tk.Label(self.window, text=self.text_translate("請掃描條碼"),
                 font=('', int(80*self.__font_ratio), 'bold')).place(relx=0.0, rely=0.25, relwidth=1.0, relheight=0.2)
        self.barcode_entry = tk.Entry(self.window, font=('', int(60*self.__font_ratio), 'bold'))
        self.barcode_entry.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.15)
        self.barcode_entry.focus_set()
        self.barcode_entry.bind('<Return>', self.check_barcode)

    def check_barcode(self, event):
        string = self.barcode_entry.get()
        if not string:  # check the string isn't empty
            self.get_barcode()
        else:
            self.clean()
            DAN.push('barcode_result_nano', self.barcode_control_info[0], self.barcode_control_info[1], string)
            tk.Label(self.window, text="條碼編號： ", anchor="w",
                     font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.2)
            tk.Label(self.window, text="{}".format(string), anchor="w",
                     font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.4)
            tk.Label(self.window, text=self.text_translate("上傳中..."), anchor="e",
                     font=('', int(60 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.8, relwidth=1.0, relheight=0.2)
            self.window.after(3000, lambda: self.wait_page())





    ## Syringe Scale Mode
    def scan_scale(self):
        if self.DEBUG:
            self.syringe_scale_control_info = ["aaa", "bbb", "5 ml", "True"]
        self.clean()
        self.__scale_val_hist_list = []
        self.frame_show = tk.Label(self.window)
        self.frame_show.place(relx=0.0, rely=0.0, relwidth=0.3, relheight=1.0)

        tk.Label(self.window, text=self.text_translate("請將針具放置於固定平台"),
                 font=('', int(28 * self.__font_ratio), 'bold')).place(relx=0.31, rely=0.0, relwidth=0.69, relheight=0.1)

        self.__syringe_hint_imagetk = ImageTk.PhotoImage(Image.open('./GUI/images/HW_V2_with_syringe.png').resize(
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
        Separator(self.window, orient=tk.VERTICAL).place(relx=0.3, rely=0.0, relheight=1.0)
        Separator(self.window, orient=tk.VERTICAL).place(relx=0.649, rely=0.8, relheight=0.2)
        self.show_webcam_stream()

    def show_webcam_stream(self):
        frame = self.webcam_stream.syringe_image_list.read()
        self.scale_frame, self.scale_value = self.syringe_scale.get_scale(frame[0], frame[1], syringe_type=self.syringe_scale_control_info[-2])

        img_ratio = 0.98 * min(self.__screen_height/self.scale_frame.shape[0], 0.3*self.__screen_width/self.scale_frame.shape[1])
        cv2image = cv2.cvtColor(cv2.resize(self.scale_frame, None, fx=img_ratio, fy=img_ratio), cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.frame_show.imgtk = imgtk
        self.frame_show.configure(image=imgtk)
        self.frame_show_val.config(text=self.text_translate("辨識數值： {}".format(self.scale_value)))
        self.frame_show.after(50, self.show_webcam_stream)
        self.scan_scale_auto_finish(self.scale_value)
        print(time.time())

    def scan_scale_auto_finish(self, scale_value):  # push data while scale value stable
        # print(time.time())
        if scale_value is not None:
            self.__scale_val_hist_list.append(scale_value)
            self.scale_running_bar['value'] = len(self.__scale_val_hist_list)*90/30
            if(len(self.__scale_val_hist_list) > 30):
                __mean = statistics.mean(self.__scale_val_hist_list)
                __median = statistics.median(self.__scale_val_hist_list)
                if __median > __mean:
                    self.scale_running_bar['value'] = 100 * (__mean+1) / (__median+1)
                else:
                    self.scale_running_bar['value'] = 100 * (__median+1) / (__mean+1)

                if(float(__median) == float(scale_value) and float(__mean) == float(__median)): ## finished and push
                    self.clean()
                    # cv2.imwrite("{}/{}_{}_{}_{}_{}.jpg".format(self.__cfg["syringe_scale_img_save_path"], time.strftime("%Y%d%m%H%M%S", time.localtime()),
                    #                                self.syringe_scale_control_info[0], self.syringe_scale_control_info[1],
                    #                                self.syringe_scale_control_info[2].replace(" ", ""), scale_value), self.cur_frame)
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

    def check_network(self, URL="https://www.google.com.tw/", show_GUI=True):
        self.clean()
        # retry_time_count = time.time()
        try:
            urllib.request.urlopen(URL, timeout=1)
            if not show_GUI:
                return True
        except urllib.request.URLError as err:
            if show_GUI:
                flg = tk.Label(self.window, text="")
                tk.Label(self.window, text=self.text_translate("系統已離線..."), font=('', int(80 * self.__font_ratio), 'bold')).place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
                tk.Button(self.window, text=self.text_translate("retry"), font=('', int(40 * self.__font_ratio), 'bold'),
                          command=flg.pack).place(relx=0.8, rely=0.8, relwidth=0.2, relheight=0.2)
                self.window.wait_visibility(flg)
                self.check_network(URL)
            else:
                return False

    def dummy_device_loop(self):
        ServerURL = self.__cfg["ServerURL"]
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
                        self.light.light_on(255)
                        self.syringe_scale_control_info = syringe_scale_control
                        self.scan_scale()
                    else:
                        self.wait_page()

            except Exception as e:
                self.check_network(ServerURL)
                print(e)
                if str(e).find('mac_addr not found:') != -1:
                    print('Reg_addr is not found. Try to re-register...')
                    DAN.device_registration_with_retry(ServerURL, Reg_addr)
                else:
                    print('Connection failed due to unknow reasons.')
                    time.sleep(1)
            time.sleep(0.2)



