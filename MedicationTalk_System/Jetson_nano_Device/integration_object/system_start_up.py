import cv2
from threading import Thread
from queue import Queue

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


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
    frame_queue= Queue()
    Thread(target=get_frame, args=(cap, frame_queue)).start()
    
    from GUI.DAI import pill_yolo
    pill_detect = pill_yolo()

    Thread(pill_detect.inference(frame_queue)).start()

    while(1):
        print(pill_detect.predictions.get())



















