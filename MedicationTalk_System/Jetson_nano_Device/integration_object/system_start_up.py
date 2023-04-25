'''
MedicationTalk Edge Device
Deployment: Jetson Nano
說明：處理‘實體’給藥相關功能與 IoTtalk 交互
Features：
1. 藥丸辨識： Yolo 辨識藥丸種類與數量
2. 影像備份： 備份藥丸辨識之原始影像至 Google Drive 以利回顧正確性
3. Barcode 掃碼： 掃 Barcode 條碼並將條碼資訊送至與資料庫查詢資訊
'''

import cv2
from threading import Thread
from queue import Queue

from GUI import DAN
import time
# set Device dummy device
# ServerURL = 'https://1.iottalk.tw' 
# Reg_addr = 'Device_Demo' #if None, Reg_addr = MAC address
# DAN.profile['d_name'] = 'Device_Demo'
# DAN.profile['dm_name'] = 'MedicationTalk_Device'
# DAN.profile['df_list'] = ['Pill_Detect_Result-I', 'Syringe_Result-I', 'Retrieve-I', 'Connect-I', 'Barcode-O', 'Pill_Detect-O', 'Syringe-O', 'Update-O']
# DAN.device_registration_with_retry(ServerURL, Reg_addr)

# this device 
# device = 'Device_Demo'

# set camera 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# get frame thread
def get_frame(cap, frame_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if frame_queue.qsize() < 1:
            frame_queue.put(frame)
        if not ret:
            break

    cap.release()

if __name__ == "__main__":
    # get frame 
    frame_queue = Queue()
    Thread(target=get_frame, args=(cap, frame_queue)).start()
    
    # pill detect
    from GUI.DAI import pill_yolo
    pill_detect = pill_yolo()

    for i in range(50):
        print(frame_queue.qsize())
    frame = frame_queue.get()
    pill_detect.DB_backup('test', frame)
    # while True:
    #     try:   
           
    #         # pull from IoTtalk
    #         pill_detect_check = DAN.pull('Pill_Detect-O')
    #         print(pill_detect_check)

    #         pill_detect.detect(pill_detect_check, device, frame_queue)
            

    #         print(frame_queue.qsize(), pill_detect.predictions.qsize())
            







            # clear queue

        # except Exception as e:
        #     print(e)
        #     if str(e).find('mac_addr not found:') != -1:
        #         print('Reg_addr is not found. Try to re-register...')
        #         DAN.device_registration_with_retry(ServerURL, Reg_addr)
        #     else:
        #         print('Connection failed due to unknow reasons.')
        #         time.sleep(1)

        # time.sleep(0.5)


                    
           
















