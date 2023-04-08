import time
import cv2
import DAN, csmapi, darknet, yolo_detect
from threading import Thread
from queue import Queue
import datetime

# google Drive API
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import auth
import os

# google drive
SCOPES = 'https://www.googleapis.com/auth/drive'

# your google drive API OAuth
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
creds = authInst.getCredentials()


# ================ iottalk ===============
ServerURL = 'https://1.iottalk.tw'      #with non-secure connection

# set Device dummy device
Reg_addr = 'Device_Demo' #if None, Reg_addr = MAC address
DAN.profile['d_name'] = 'Device_Demo'
DAN.device_registration_with_retry(ServerURL, Reg_addr)

csmapi.ENDPOINT = ServerURL

# =============== yolo ================
network, class_names, class_colors = darknet.load_network(
    './yolov7-tiny.cfg',
        './obj.data',
        './yolov7-tiny_final.weights',
        batch_size=1
    )

darknet_width = darknet.network_width(network)
darknet_height = darknet.network_height(network)
input_path = yolo_detect.str2int(0)

# webcam
cap = cv2.VideoCapture(input_path)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Queue for threading
row_frame_queue = Queue()
pill_frame_queue = Queue(maxsize=1)
predictions = Queue()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # row frame for save picture and syringe
#     row_frame_queue.put(frame)
#     print(row_frame_queue.qsize())
#     if(row_frame_queue.qsize()>100):
#         for i in range(row_frame_queue.qsize()):
#             row_frame_queue.get()
# cap.release()

# webcam stream
Thread(target=yolo_detect.get_frame, args=(cap, row_frame_queue, pill_frame_queue, darknet_width, darknet_height)).start()

# pill detect
Thread(target=yolo_detect.darknet_pill_detect, args=(cap, pill_frame_queue, network, class_names, 0.5, predictions)).start()

# init
pills = {   'Dilatrend 25mg/tab' : 0, 
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
user_id = 'user'

# loop connect with IoTtalk
while True:
    try:
        # ============= pill yolo ===============
        # pull from IoTtalk
        pill_detect_check = DAN.pull('Pill_Detect-O')
        print(pill_detect_check)

        if pill_detect_check != None and pill_detect_check[1] == Reg_addr and pill_detect_check[2]:
            
            user_id = pill_detect_check[0]
            rep_pill_check = False

            # clear queue
            for i in range(predictions.qsize()):
                predictions.get()
            
            # clear value
            for item in pills.keys():
                pills[item] = 0
        
        
        # voting processing
        if rep_pill_check == False and predictions.qsize() >= 50:
            rep_pill_check = True
            candidate = []
            vote = []

            for i in range(50):
                # each frame prediction 
                frame_prediction = predictions.get()

                # Calculate prediction combinations.
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

            # push to IoTtalk
            DAN.push ('Pill_Detect_Result-I',  user_id,
                                                    pills['Dilatrend 25mg/tab'],
                                                    pills[ 'Requip F.C 0.25mg/tab'],
                                                    pills['Repaglinide 1mg/tab'],
                                                    pills['Transamin 250mg/tab'],
                                                    pills[ 'Bokey 100mg/tab'],
                                                    pills['Zocor 20 mg/tab'], 
                                                    pills['FLU-D (Fluconazole) 50mg/tab'],
                                                    pills['Dilantin'],
                                                    pills['Requip F.C 1 mg'])

            now = datetime.datetime.now()
            now = now.strftime('%m_%d_%H_%M_%S')

            # save picture
            cv2.imwrite(user_id + '_' + now + '.jpg', row_frame_queue.get())

            try:
                # connect Google Drive
                service = build('drive', 'v3', credentials=creds)

                file_metadata = {'name': user_id + '_' + now + '.jpg',
                                'parents': ['1ujH56sEnVDuq2tnwk241GIOjkMUxp3S4']}

                # Upload
                media = MediaFileUpload(user_id + '_' + now + '.jpg', mimetype='image/jpeg')
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(F'File ID: {file.get("id")}')

                # remove local picture
                os.remove(user_id + '_' + now + '.jpg')

            except HttpError as error:
                print(F'An error occurred: {error}')
                file = None

        # clear queue
        if (row_frame_queue.qsize() > 100):
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
            for i in range(row_frame_queue.qsize()):
                row_frame_queue.get()
           
        if (predictions.qsize() > 100 and rep_pill_check == True):
            for i in range(predictions.qsize()):
                predictions.get()

            
        # ============= pill yolo ===============

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    
    time.sleep(0.5)
    