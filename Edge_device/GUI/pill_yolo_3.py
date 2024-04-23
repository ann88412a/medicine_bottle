import time
import cv2
from . import DAN, csmapi #, darknet, yolo_darknet
from threading import Thread
from queue import Queue
import datetime
import json
import datetime
import onnxruntime as ort
import random
import numpy as np

# google Drive API
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from . import auth
import os
from os import environ
from psutil import cpu_count

class pill_yolo_3:
    def __init__(self):
        # google drive
        SCOPES = 'https://www.googleapis.com/auth/drive'
        # your google drive API OAuth
        CLIENT_SECRET_FILE = './config_files/client_secret.json'
        APPLICATION_NAME = 'Drive API'
        authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
        self.creds = authInst.getCredentials()
        
        # yolo pill detect

        # load model
        # onnx version
        environ["OMP_NUM_THREADS"] = str(cpu_count(logical=True))
        environ["OMP_WAIT_POLICY"] = 'ACTIVE'
        w = './config_files/lesson_plan_three_nms.onnx'
        providers = ['CPUExecutionProvider']
        print('using', ort.get_device())
        sess_opt = ort.SessionOptions() 
        sess_opt.intra_op_num_threads = 4
        self.session = ort.InferenceSession(w, sess_opt, providers=providers)
        print('Lesson three onnx model loading done')
        
        
        # darknet version
        # self.network, self.class_names, class_colors = darknet.load_network(
            # './config_files/yolov7-tiny.cfg',
            # './config_files/obj.data',
            # './config_files/yolov7-tiny_final.weights',
            # batch_size=1
        # )

        # self.darknet_width = darknet.network_width(self.network)
        # self.darknet_height = darknet.network_height(self.network)
        # self.thr = 0.5

        # init  
        # class name
        names = ['Apno 30mg/tab', 'Sennoside', 'Paramol', 'Primperan'

               , 'Peace', 'Lanpo 30mg/tab']

               
        # set bbox
        self.colors = {name:[random.randint(0, 255) for _ in range(3)] for i,name in enumerate(names)}
        self.outname = [i.name for i in self.session.get_outputs()]
        self.inname = [i.name for i in self.session.get_inputs()]
        
        
        self.raw_prediction = []
        self.predictions = Queue()
        self.candidate_index = []
        self.vote = []
        self.pills = {'Apno 30mg/tab': 0,
                    'Sennoside': 0,
                    'Paramol': 0,
                    'Primperan': 0,
                    'Peace': 0,
                    'Lanpo 30mg/tab': 0,}
        self.pill_name = list(self.pills)
        
        self.barcode_ans = '--------------'
        self.rep_pill_check = False
        self.user_id = 'user'
        
    # onnx preprocessing
    def letterbox(self, im, new_shape=(320, 320), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
            
        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)
        
        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
            
        dw /= 2  # divide padding into 2 side
        dh /= 2
        
        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
            
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        
        return im, r, (dw, dh)

    def preprocess(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        image = img.copy()
        image, ratio, dwdh = self.letterbox(image, auto=False)
        image = image.transpose((2, 0, 1))
        image = np.expand_dims(image, 0)
        image = np.ascontiguousarray(image)

        im = image.astype(np.float32)
        im /= 255

        return im, ratio, dwdh

    def plot_bbox(self, image, names, ratio, dwdh, outputs):
        for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(outputs):
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()
            cls_id = int(cls_id)
			# score = round(float(score),3)
            name = names[cls_id]
            colors = {'Apno 30mg/tab': [45, 73, 219], 'Sennoside': [218, 115, 74], 'Paramol': [99, 135, 62], 'Primperan': [52, 230, 38], 'Peace': [163, 189, 183], 'Lanpo 30mg/tab': [220, 125, 9]}
            color = colors[name] # name += ' '+str(score)
            cv2.rectangle(image,box[:2],box[2:],color,2)
            cv2.putText(image,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2)
        return image
    
    # inference 
    def inference(self, frame_queue):
        frame = frame_queue.get()
        
        # Data Augmentation
        for tta_i in range(9):
            o_img = frame.copy()
            
            (h, w) = o_img.shape[:2]
            center = (w/2, h/2)
            
            if tta_i == 1:
                o_img = cv2.flip(o_img, 0)
            elif tta_i == 2:
                o_img = cv2.flip(o_img, 1)
            elif tta_i == 3:
                o_img = cv2.flip(o_img, -1)
            elif tta_i ==4:
                M = cv2.getRotationMatrix2D(center, 3, 1.0)
                o_img = cv2.warpAffine(o_img, M, (w, h))
            elif tta_i ==5:
                M = cv2.getRotationMatrix2D(center, -3, 1.0)
                o_img = cv2.warpAffine(o_img, M, (w, h))
            elif tta_i ==6:
                M = cv2.getRotationMatrix2D(center, 5, 1.0)
                o_img = cv2.warpAffine(o_img, M, (w, h))
            elif tta_i ==7:
                M = cv2.getRotationMatrix2D(center, -5, 1.0)
                o_img = cv2.warpAffine(o_img, M, (w, h))
            elif tta_i ==8:
                M = cv2.getRotationMatrix2D(center, 1, 1.0)
                o_img = cv2.warpAffine(o_img, M, (w, h))
                
            # preprocess
            im, ratio, dwdh = self.preprocess(o_img)
            
            inp = {self.inname[0]:im}
            
            # model predict
            outputs = self.session.run(self.outname, inp)[0]
            
            # check predict
            # frame_predict = self.plot_bbox(o_img.copy(), self.pill_name, ratio, dwdh, outputs)
            # self.image_backup('check'+self.user_id, frame_predict)
            
            # collect prediction
            self.raw_prediction.append(outputs)
            prediction = []
            print(outputs.shape)
            #print(len(outputs[i]))
            for i in range(len(outputs)):
                #print((outputs[i][5]))
                print(outputs[i].shape)
                prediction.append(int(outputs[i][5]))
                
            self.predictions.put(sorted(prediction))
            
            
        
        #yolo_darknet.pill_detect(frame, self.darknet_width, self.darknet_height, self.network, self.class_names, self.thr, self.predictions)


    # google drive upload
    def image_backup(self, name, frame):
        try:
            now = datetime.datetime.now()
            now = now.strftime('%m_%d_%H_%M_%S')
            # save picture]
            cv2.imwrite(name + '_' + now + '.jpg', frame)

            # connect Google Drive
            service = build('drive', 'v3', credentials=self.creds)

            file_metadata = {'name': name + '_' + now + '.jpg',
                            'parents': ['1ujH56sEnVDuq2tnwk241GIOjkMUxp3S4']}

            # Upload
            media = MediaFileUpload(name + '_' + now + '.jpg', mimetype='image/jpeg')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(F'File ID: {file.get("id")}')

            # remove local picture
            os.remove(name + '_' + now + '.jpg')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None


    # # pill algorithm
    def pill_voting(self, frame_queue):
        if self.rep_pill_check == False and self.predictions.qsize() >= 9:
            self.rep_pill_check = True
            candidate = []

            for i in range(3):
                # each frame prediction 
                frame_prediction = self.predictions.get()

                # Calculate prediction combinations.
                if  frame_prediction not in candidate:
                    candidate.append(frame_prediction)
                    self.candidate_index.append(i)
                    self.vote.append(1)

                else:
                    self.vote[candidate.index(frame_prediction)] += 1
                
            print(self.vote, candidate)
            
            for pill in candidate[self.vote.index(max(self.vote))]:
                self.pills[self.pill_name[pill]] += 1


            for item in self.pills:
                print(item, self.pills[item])

            # push to IoTtalk
            print(self.pills)
            DAN.push ('Pill_Detect_Result-I',  self.user_id,
                                                    self.pills['Apno 30mg/tab'],
                                                    self.pills['Sennoside'],
                                                    self.pills['Paramol'],
                                                    self.pills['Primperan'],
                                                    self.pills['Peace'],
                                                    self.pills['Lanpo 30mg/tab'], 
                                                    0,0,0)
            frame = frame_queue.get()
            self.image_backup(self.user_id, frame)

    def pill_processing(self, frame_queue):
        self.inference(frame_queue)
        self.pill_voting(frame_queue)

    # # pill detect check
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


            
        
