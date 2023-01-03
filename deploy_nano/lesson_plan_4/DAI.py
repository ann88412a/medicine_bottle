import time
import cv2
import DAN, csmapi, darknet, yolo_detect
from threading import Thread
from queue import Queue
from pytimedinput import timedInput
from datetime import datetime
import json



# ================ iottalk ===============
ServerURL = 'https://1.iottalk.tw'      #with non-secure connection
Reg_addr = 'BAC0B21FDC32' #if None, Reg_addr = MAC address

csmapi.ENDPOINT = ServerURL

# =============== yolo ================
frame_queue = Queue()
darknet_image_queue = Queue(maxsize=1)
detections_queue = Queue(maxsize=1)
fps_queue = Queue(maxsize=1)


network, class_names, class_colors = darknet.load_network(
       './yolov7-tiny.cfg',
        './obj.data',
        './yolov7-tiny_final.weights',
        batch_size=1
    )
darknet_width = darknet.network_width(network)
darknet_height = darknet.network_height(network)
input_path = yolo_detect.str2int(0)
cap = cv2.VideoCapture(input_path)

Thread(target=yolo_detect.video_capture, args=(cap, frame_queue, darknet_image_queue, darknet_width, darknet_height)).start()
predictions = Queue()
Thread(target=yolo_detect.inference, args=(cap, darknet_image_queue, detections_queue, fps_queue, network, class_names, 0.5, predictions)).start()
Thread(target=yolo_detect.drawing, args=(cap, frame_queue, detections_queue, fps_queue)).start()


pills = { 'Dilatrend 25mg/tab' : 0, 
                'Requip F.C 0.25mg/tab': 0, 
                'Repaglinide 1mg/tab': 0, 
                'Transamin 250mg/tab': 0,
                'Bokey 100mg/tab': 0,
                'Zocor 20 mg/tab': 0,
                'FLU-D (Fluconazole) 50mg/tab': 0,
                'Dilantin': 0,
                'Requip F.C 1 mg': 0}
barcode_ans = '--------------'
rep_pill_check = False
while True:
    try:
        # ============= barcode ===============
        barcode_check = DAN.pull('patient_barcode_sign')
        
        if barcode_check:
            
            barcode_ans, timedOut = timedInput("Please, do enter something: ", timeout= 10)
            # print(barcode_ans, timedOut)
            if barcode_ans == "":
                barcode_ans = 'barcode not read'
            DAN.push ('patient_barcode_r', barcode_ans) 

        # ============= pill yolo ===============
        pill_detect_check = DAN.pull('pill_sign')
        
        if pill_detect_check:
            rep_pill_check = False
            # clear queue
            for i in range(predictions.qsize()):
                predictions.get()
            
            for item in pills.keys():
                pills[item] = 0
            # DAN.push ('pill_r', False)
        
        if rep_pill_check == False and predictions.qsize() >= 50:
            rep_pill_check = True
            candidate = []
            vote = []
            for i in range(50):
                frame_prediction = predictions.get()
                if  frame_prediction not in candidate:
                    candidate.append(frame_prediction)
                    vote.append(1)
                else:
                    vote[candidate.index(frame_prediction)] += 1
            
            for pill in candidate[vote.index(max(vote))]:
                pills[pill] += 1

            print(candidate)
            print(vote)
            for item in pills:
                print(item, pills[item])
            DAN.push ('pill_r',  pills['Dilatrend 25mg/tab'],
                                                    pills[ 'Requip F.C 0.25mg/tab'],
                                                    pills['Repaglinide 1mg/tab'],
                                                    pills['Transamin 250mg/tab'],
                                                    pills[ 'Bokey 100mg/tab'],
                                                    pills['Zocor 20 mg/tab'], 
                                                    pills['FLU-D (Fluconazole) 50mg/tab'],
                                                    pills['Dilantin'],
                                                    pills['Requip F.C 1 mg'])
        # print('return',predictions.qsize())
        # =========== confirm ==========
        # confirm_check = DAN.pull('id_check') 
        
        # if confirm_check:
        #     pills_json = json.dumps(pills)
        #     print(pills)
        #     DAN.push ('backup', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), confirm_check[1], barcode_ans, pills_json) 

        #     time.sleep(0.5)
        #     DAN.push ('barcode_ans', '____________') 
        #     DAN.push ('pill_detect_done', False)
            



    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    
    time.sleep(0.5)
    