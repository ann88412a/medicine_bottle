from glob import glob
import tkinter as tk
from tkinter import CENTER, ttk
import time
from tkinter import font
from ctypes import *
import random
import os
import cv2
import time

from scipy import r_
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue

#===============YOLO==================

def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default=0,
                        help="video source. If empty, uses webcam 0 stream")
    parser.add_argument("--out_filename", type=str, default="",
                        help="inference video name. Not saved if empty")
    parser.add_argument("--weights", default='/home/medical/medicine_bottle/pill/yolov4/tensorRT/yolov4_tiny_pill.weights',
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default='/home/medical/medicine_bottle/pill/yolov4/tensorRT/yolov4_tiny_pill.cfg',
                        help="path to config file")
    parser.add_argument("--data_file", default='/home/medical/medicine_bottle/pill/yolov4/jetson_obj.data',
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.25,
                        help="remove detections with confidence below this value")
    return parser.parse_args()

def str2int(video_path):
    try:
        return int(video_path)
    except ValueError:
        return video_path

def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame)
        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()

def inference(darknet_image_queue, detections_queue, fps_queue):
    global start_detect
    
    start_detect = True

    global inference_detection
    while cap.isOpened():
       
        test = ['Sennoside','Apresoline','Repaglinide','Cataflam']
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=args.thresh)
        detections_queue.put(detections)
        fps = int(1/(time.time() - prev_time))
        fps_queue.put(fps)
        # print("FPS: {}".format(fps))
        # darknet.print_detections(detections, args.ext_output)
        
        # sort_test = sorted(test)
        # print(test,'sdjfl',sort_test)
        detection_sort = sorted([i[0] for i in detections])
        inference_detection = detection_sort
        print('detection :',detection_sort)

    
       
        darknet.free_image(darknet_image)
    cap.release()

def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video

def convert2relative(bbox):
    """
    YOLO format use relative coordinates for annotation
    """
    x, y, w, h  = bbox
    _height     = darknet_height
    _width      = darknet_width
    return x/_width, y/_height, w/_width, h/_height

def convert2original(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_x       = int(x * image_w)
    orig_y       = int(y * image_h)
    orig_width   = int(w * image_w)
    orig_height  = int(h * image_h)

    bbox_converted = (orig_x, orig_y, orig_width, orig_height)

    return bbox_converted

def drawing(frame_queue, detections_queue, fps_queue):
    random.seed(3)  # deterministic bbox colors
    video = set_saved_video(cap, args.out_filename, (video_width, video_height))
    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        detections_adjusted = []
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = convert2original(frame, bbox)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, class_colors)
            # if not args.dont_show:
            #     cv2.imshow('Inference', image)
            if args.out_filename is not None:
                video.write(image)
            if cv2.waitKey(fps) == 27:
                break
    cap.release()
    video.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    start_detect = False
    inference_detection = []
    vote_list = []
    vote = False
    result = []
# def open_yolo():    
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)

    args = parser()
    
    network, class_names, class_colors = darknet.load_network(
            args.config_file,
            args.data_file,
            args.weights,
            batch_size=1
        )
    darknet_width = darknet.network_width(network)
    darknet_height = darknet.network_height(network)
    input_path = str2int(args.input)
    cap = cv2.VideoCapture(input_path)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    Thread(target=video_capture, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue, detections_queue, fps_queue)).start()
    Thread(target=drawing, args=(frame_queue, detections_queue, fps_queue)).start()




#==============GUI===============  

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
         
        global start_detect
        
        def ready():
            if start_detect:
                label.config(text ="開機完成")
                label.grid(row = 0, column = 0)
                button1 = tk.Button(self, text ="開始",command = lambda : controller.show_frame(Page1), font = LARGEFONT)
                button1.grid(row = 1, column = 0,sticky=tk.E)
                
            else:
                label.config(text ="開機中"+str(time.time()))
                label.after(1,ready)
        # label of frame Layout 2
        label = ttk.Label(self, text ="開機中", font = LARGEFONT)
        ready()
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 0,sticky=tk.E)
        
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        
        def clear_vote():
            global vote_list
            global vote
            vote_list.clear()
            vote = True
          

        label = ttk.Label(self, text ="請先放入藥丸再按開始辨識", font = LARGEFONT)
        label.grid(row = 0, column = 0)
  
        # button to show frame 2 with text
        # layout2
        button1 = tk.Button(self, text ="開始辨識",
                            command = lambda : [clear_vote(),controller.show_frame(Page2)],font = LARGEFONT)
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 0)
  
     
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # vote_list.append(inference_detection)
        def reset():
            global vote
            vote = False
        def ready():
            global vote_list
            global inference_detection
            global vote
            
            print('--------------------------')
            print('--------------------------')
            print('--------------------------')
            print(vote_list)

            if len(vote_list) >9:
                label.config(text = "辨識完成")
                count_list = []
                count_list.clear()
                for i in range(len(vote_list)):
                    global result
                    if vote_list.count(vote_list[i]) > len(vote_list)/2:
                        
                        result = vote_list[i]
                       
                        break
                    else:
                        count_list = count_list.append(vote_list.count(vote_list[i]))
                        if len(vote_list) == len(count_list):
                            result = vote_list[count_list.index(max(count_list))]

                label.grid(row = 0, column = 0)
                button1 = tk.Button(self, text ="確認結果",command = lambda : [controller.show_frame(Page3),reset()], font = LARGEFONT)
                button1.grid(row = 1, column = 0,sticky=tk.E)
                
            else:
                label.config(text = "辨識中")
                print('i am here',vote)
                if vote == True:
                    vote_list.append(inference_detection)
                print(len(vote_list),vote_list)
                label.after(200,ready)
        label = ttk.Label(self, text ="辨識中", font = LARGEFONT)
        label.grid(row = 0, column = 0,sticky=tk.E)
        ready()
        

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global result
       
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

        def show_ans():
            print('--------------------------')
            print('--------------------------')
            print('--------------------------')
            print(result)

        def init():
            global start_detect
            global inference_detection
            global vote_list
            global vote
            global result

            start_detect = False
            inference_detection =[]
            vote_list = []
            vote = False
            result = []
        
        button1 = tk.Button(self, text ="確認",
                            command = lambda : [controller.show_frame(Page1),show_ans(),init()],font=LARGEFONT)
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
     
  
# Driver Code
app = tkinterApp()
app.geometry("1080x960")
app.title('藥丸辨識')
app.mainloop()

