
import numpy as np
import os
import time

start = time.time()
# command = '/home/fritingo/Documents/yolo/darknet/darknet detector test /home/fritingo/Documents/yolo/darknet/pill/obj.data /home/fritingo/Documents/yolo/darknet/pill/yolo_pill.cfg /home/fritingo/Documents/yolo/darknet/pill/yolo_pill_final.weights /home/fritingo/Documents/pill_data/1-2-4/5.png'
command = '/home/medical/darknet/darknet detector test /home/medical/medicine_bottle/pill/yolov4/jetson_obj.data /home/medical/medicine_bottle/pill/yolov4/yolo_pill.cfg /home/medical/medicine_bottle/pill/yolov4/yolo_pill_final.weights /home/medical/pill_data/1-3-4/4.png  -dont_show'

r = os.popen(command) #Execute command
info = r.readlines()  #read command output
i = 0


pills = np.array([])
for line in info:  #handle output line by line
    line = line.strip('\r\n')
    i = i+1
    # if i > 10:
    print(i,line)
        # pills = np.append(pills,line)
os.popen('q')
print(pills)
