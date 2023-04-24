import cv2
import time
import requests
import random
import numpy as np
import onnxruntime as ort
from PIL import Image
from pathlib import Path
from collections import OrderedDict,namedtuple
import argparse
from threading import Thread
from queue import Queue

parser = argparse.ArgumentParser()
parser.add_argument('--weights', type=str, default='./yolov6/yolov6n.onnx', help='weights path')
parser.add_argument('--source', type=str, default='./pill.png')  # height, width
parser.add_argument('--size', type=int, default=320)
parser.add_argument('--dataset', type=str, default='pill')
opt = parser.parse_args()
print(opt)

# init model
cuda = True
w = opt.weights
print(ort.get_available_providers())
# providers = ['TensorrtExecutionProvider']
providers = ['CUDAExecutionProvider']
# providers = ['CPUExecutionProvider']
print(ort.get_device())

session = ort.InferenceSession(w, providers=providers)


# preprocess
def letterbox(im, new_shape=(opt.size, opt.size), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
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

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)

names = ['Dilatrend 25mg/tab', 'Requip F.C 0.25mg/tab', 'Repaglinide 1mg/tab', 'Transamin 250mg/tab'
       , 'Bokey 100mg/tab', 'Zocor 20 mg/tab', 'FLU-D (Fluconazole) 50mg/tab', 'Dilantin'
       , 'Requip F.C 1 mg']
    
colors = {name:[random.randint(0, 255) for _ in range(3)] for i,name in enumerate(names)}
outname = [i.name for i in session.get_outputs()]
inname = [i.name for i in session.get_inputs()]

# img process
def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    image = img.copy()
    image, ratio, dwdh = letterbox(image, auto=False)
    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)

    im = image.astype(np.float32)
    im /= 255

    return im, ratio, dwdh

def plot_bbox(img, predication, ratio, dwdh):
    for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(predication):
        img = img[int(batch_id)]
        # box = np.array([x0,y0,x1,y1])
        # box -= np.array(dwdh*2)
        # box /= ratio
        # box = box.round().astype(np.int32).tolist()
        # cls_id = int(cls_id)
        # score = round(float(score),3)
        # name = names[cls_id]
        # color = colors[name]
        # name += ' '+str(score)
        # cv2.rectangle(img,box[:2],box[2:],color,2)
        # cv2.putText(img,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2) 
    return img 

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

if __name__ == '__main__':
    # get frame 
    frame_queue = Queue()
    Thread(target=get_frame, args=(cap, frame_queue)).start()
    while(True):
        frame = frame_queue.get()
        prev_time = time.time()
        # print(frame)
        im, ratio, dwdh = preprocess(frame)
        inp = {inname[0]:im}
        # inference
        outputs = session.run(outname, inp)[0]
        # print(outputs)
        image = frame.copy()
        print(outputs)

        for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(outputs):
            image = image
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()
            cls_id = int(cls_id)
            score = round(float(score),3)
            name = names[cls_id]
            color = colors[name]
            name += ' '+str(score)
            cv2.rectangle(image,box[:2],box[2:],color,2)
            cv2.putText(image,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2)
       

        print('fps:', int(1/(time.time() - prev_time)))
        cv2.imshow('frame', cv2.resize(image, None, fx=0.3, fy=0.3))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
   