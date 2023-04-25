import time
import cv2
from . import DAN, csmapi, darknet, yolo_darknet
from threading import Thread
from queue import Queue
import datetime
import json
import datetime
import requests

# google Drive API
# import google.auth
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaFileUpload
# from . import auth
import os

class pill_yolo:
    def __init__(self):
        # google drive
        # SCOPES = 'https://www.googleapis.com/auth/drive'
        # # your google drive API OAuth
        # CLIENT_SECRET_FILE = './config_files/client_secret.json'
        # APPLICATION_NAME = 'Drive API'
        # authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
        # self.creds = authInst.getCredentials()
        
        # yolo pill detect

        # load model
        self.network, self.class_names, class_colors = darknet.load_network(
            './config_files/yolov7-tiny.cfg',
            './config_files/obj.data',
            './config_files/yolov7-tiny_final.weights',
            batch_size=1
        )

        self.darknet_width = darknet.network_width(self.network)
        self.darknet_height = darknet.network_height(self.network)
        self.thr = 0.5

        # init  
        self.predictions = Queue()
        self.pills = {'Dilatrend 25mg/tab': 0,
                 'Requip F.C 0.25mg/tab': 0,
                 'Repaglinide 1mg/tab': 0,
                 'Transamin 250mg/tab': 0,
                 'Bokey 100mg/tab': 0,
                 'Zocor 20 mg/tab': 0,
                 'FLU-D (Fluconazole) 50mg/tab': 0,
                 'Dilantin': 0,
                 'Requip F.C 1 mg': 0}
        self.barcode_ans = '--------------'
        self.rep_pill_check = False
        self.user_id = 'user'
        

    # inference 
    def inference(self, frame_queue):
        frame = frame_queue.get()
        yolo_darknet.pill_detect(frame, self.darknet_width, self.darknet_height, self.network, self.class_names, self.thr, self.predictions)


    # google drive upload
    # def image_backup(self, name, frame):
    #     try:
    #         now = datetime.datetime.now()
    #         now = now.strftime('%m_%d_%H_%M_%S')
    #         # save picture
    #         cv2.imwrite(name + '_' + now + '.jpg', frame)

    #         # connect Google Drive
    #         service = build('drive', 'v3', credentials=self.creds)

    #         file_metadata = {'name': name + '_' + now + '.jpg',
    #                         'parents': ['1ujH56sEnVDuq2tnwk241GIOjkMUxp3S4']}

    #         # Upload
    #         media = MediaFileUpload(name + '_' + now + '.jpg', mimetype='image/jpeg')
    #         file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    #         print(F'File ID: {file.get("id")}')

    #         # remove local picture
    #         os.remove(name + '_' + now + '.jpg')

    #     except HttpError as error:
    #         print(F'An error occurred: {error}')
    #         file = None

    # DB upload
    def DB_backup(self, name, frame):
        cv2.imwrite(name + '.jpg', frame)
        files = {'file': open(name + '.jpg','rb')}
        values = {'name': name}
        url = 'https://140.113.110.21:7777/api/_pic'
        r = requests.post(url, files=files, data=values, verify=False)
        os.remove(name + '.jpg')


    # pill algorithm
    def pill_voting(self, frame_queue):
        if self.rep_pill_check == False and self.predictions.qsize() >= 50:
            self.rep_pill_check = True
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
                self.pills[pill] += 1

            print(candidate)
            print(vote)

            for item in self.pills:
                print(item, self.pills[item])

            # push to IoTtalk
            DAN.push ('Pill_Detect_Result-I',  self.user_id,
                                                    self.pills['Dilatrend 25mg/tab'],
                                                    self.pills[ 'Requip F.C 0.25mg/tab'],
                                                    self.pills['Repaglinide 1mg/tab'],
                                                    self.pills['Transamin 250mg/tab'],
                                                    self.pills[ 'Bokey 100mg/tab'],
                                                    self.pills['Zocor 20 mg/tab'], 
                                                    self.pills['FLU-D (Fluconazole) 50mg/tab'],
                                                    self.pills['Dilantin'],
                                                    self.pills['Requip F.C 1 mg'])
            frame = frame_queue.get()
            self.DB_backup(self.user_id, frame)
            # self.image_backup(self.user_id, frame)

    def pill_processing(self, frame_queue):
        for i in range(51):
            self.inference(frame_queue)
        
        self.pill_voting(frame_queue)

    # pill detect check
    def detect(self, iottalk_pull, device, frame_queue):
        if iottalk_pull != None and iottalk_pull[1] == device and iottalk_pull[2]:
            self.user_id = iottalk_pull[0]
            self.rep_pill_check = False

            # clear queue
            for i in range(self.predictions.qsize()):
                self.predictions.get()
            
            # clear value
            for item in self.pills.keys():
                self.pills[item] = 0

            inference_loop = Thread(target=self.pill_processing, args=(frame_queue,))
            inference_loop.setDaemon(True)
            inference_loop.start()


            
        