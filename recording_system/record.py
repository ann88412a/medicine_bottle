
import threading
import cv2
import os
import datetime
from numpy import size
import paramiko
from os import listdir
import tkinter as tk


ip = '1xxxx'
port = 22
myusername = 'xxx'
pwd = '0xxx'
location = '/home/frxx/Documents/yang_ming_record/'

transport = paramiko.Transport((ip,port))
transport.connect(username=myusername,password=pwd)
sftp = paramiko.SFTPClient.from_transport(transport)

def upload():
    while 1:
        global uploaded
        clock = datetime.datetime.now()
        clock = clock.strftime('%M')
        # print(clock)
        if int(clock) % 2 == 0 and uploaded == False:
            files = listdir('record_data')
            print(files)
            for item in files:
                sftp.put('record_data/'+item,location+item)
            uploaded = True
        if int(clock) % 2 != 0 :
            uploaded = False






#===============camera====================
cap = cv2.VideoCapture(0)

def show():
    while(True):
        global frame
        ret, frame = cap.read()
        
        
        cv2.imshow('frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('r'):
        #     now = datetime.datetime.now()
        #     now = now.strftime('%d_%H_%M_%S')
        #     print(now)
        #     cv2.imwrite('/home/medical/record_data/'+str(now)+'.png',frame)
        # elif cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def take_picture():
    global frame
    now = datetime.datetime.now()
    now = now.strftime('%d_%H_%M_%S')
    
    cv2.imwrite('/home/medical/record_data/'+str(now)+'.png',frame)


if __name__ == '__main__':
    save = threading.Thread(target = upload)
    view = threading.Thread(target = show)
    

    save.start()
    view.start()

    global frame

    def take_pic():
        tmp = threading.Thread(target = take_picture)    
        tmp.start()   
    #==========GUI===============
    root = tk.Tk()
    root.title('take picture')
    root.geometry('400x400')
    LARGEFONT =("Verdana", 50)

    bt = tk.Button(root,text='拍照',command=lambda:take_pic(),font=LARGEFONT)
    bt.pack()

    root.mainloop()