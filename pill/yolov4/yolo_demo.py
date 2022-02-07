
import numpy as np
import os

command = '/home/fritingo/Documents/yolo/darknet/darknet detector test /home/fritingo/Documents/yolo/darknet/pill/obj.data /home/fritingo/Documents/yolo/darknet/pill/yolo_pill.cfg /home/fritingo/Documents/yolo/darknet/pill/yolo_pill_final.weights /home/fritingo/Documents/pill_data/1-2-4/5.png'
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