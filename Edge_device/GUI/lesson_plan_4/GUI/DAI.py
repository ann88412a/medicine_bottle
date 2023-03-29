import time
import cv2
from . import DAN, csmapi, darknet, yolo_detect
from threading import Thread
from queue import Queue
from datetime import datetime
import json
import datetime

# google Drive API
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from . import auth
import os

class pill_yolo:
    def __init__(self):
        # google drive
        SCOPES = 'https://www.googleapis.com/auth/drive'
        # your google drive API OAuth
        CLIENT_SECRET_FILE = './config_files/client_secret.json'
        APPLICATION_NAME = 'Drive API'
        authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
        self.creds = authInst.getCredentials()
        self.predictions = Queue()
        # webcam
        self.cap = cv2.VideoCapture(yolo_detect.str2int(0))
        # =============== yolo ================
        self.frame_queue = Queue()
        self.darknet_image_queue = Queue(maxsize=1)
        self.detections_queue = Queue(maxsize=1)
        self.fps_queue = Queue(maxsize=1)

        self.network, self.class_names, class_colors = darknet.load_network(
            './config_files/yolov7-tiny.cfg',
            './config_files/obj.data',
            './config_files/yolov7-tiny_final.weights',
            batch_size=1
        )

        darknet_width = darknet.network_width(self.network)
        darknet_height = darknet.network_height(self.network)

        # threading
        Thread(target=yolo_detect.video_capture, args=(self.cap, self.frame_queue, self.darknet_image_queue, darknet_width, darknet_height)).start()
        Thread(target=yolo_detect.inference, args=(self.cap, self.darknet_image_queue, self.detections_queue, self.fps_queue, self.network, self.class_names, 0.5, self.predictions)).start()
        Thread(target=yolo_detect.drawing, args=(self.cap, self.frame_queue, self.detections_queue, self.fps_queue)).start()

        Thread(target=self.iottalk_loop).start()


    # loop connect with IoTtalk
    def iottalk_loop(self):
        # ================ iottalk ===============
        ServerURL = 'https://1.iottalk.tw'  # with non-secure connection
        Reg_addr = 'BAC0B21FDC32'  # if None, Reg_addr = MAC address

        csmapi.ENDPOINT = ServerURL

        # lesson plan 4

        # init
        pills = {'Dilatrend 25mg/tab': 0,
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
        while True:
            try:
                # ============= pill yolo ===============
                # pull from IoTtalk
                pill_detect_check = DAN.pull('Pill_Detect-O')
                print(pill_detect_check)

                if pill_detect_check != None and pill_detect_check[1]:
                    user_id = pill_detect_check[0]
                    rep_pill_check = False

                    # clear queue
                    for i in range(self.predictions.qsize()):
                        self.predictions.get()

                    # clear value
                    for item in pills.keys():
                        pills[item] = 0

                print(self.cap.isOpened(), self.predictions.qsize())

                # voting processing
                if rep_pill_check == False and self.predictions.qsize() >= 50:
                    rep_pill_check = True
                    candidate = []
                    vote = []

                    for i in range(50):
                        # each frame prediction
                        frame_prediction = self.predictions.get()

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
                    cv2.imwrite(user_id + '_' + now + '.jpg', self.frame_queue.get())

                    try:
                        # connect Google Drive
                        service = build('drive', 'v3', credentials=self.creds)

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
                if (self.predictions.qsize() > 2000):
                    print('clear image queue!!')
                    DAN.device_registration_with_retry(ServerURL, Reg_addr)
                    for i in range(self.predictions.qsize()):
                        self.predictions.get()
                    # Thread(target=yolo_detect.video_capture, args=(cap, frame_queue, darknet_image_queue, darknet_width, darknet_height)).start()
                    # Thread(target=yolo_detect.inference, args=(cap, darknet_image_queue, detections_queue, fps_queue, network, class_names, 0.5, predictions)).start()
                    # Thread(target=yolo_detect.drawing, args=(cap, frame_queue, detections_queue, fps_queue)).start()

                    Thread(target=yolo_detect.inference, args=(self.cap, self.darknet_image_queue, self.detections_queue, self.fps_queue, self.network, self.class_names, 0.5, self.predictions)).start()


            except Exception as e:
                print(e)
                if str(e).find('mac_addr not found:') != -1:
                    print('Reg_addr is not found. Try to re-register...')
                    DAN.device_registration_with_retry(ServerURL, Reg_addr)
                else:
                    print('Connection failed due to unknow reasons.')
                    time.sleep(1)

            time.sleep(0.5)
    