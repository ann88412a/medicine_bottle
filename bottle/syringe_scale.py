try:
    # fix opencv open webcam slowly bug in WIN10
    import os
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    # call cv2 in WIN10
    from cv2 import cv2
except:
    # call cv2 in jetson nano
    import cv2

import numpy as np
from matplotlib import pyplot as plt

def img_thresholding(img):
    img = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 5)
    ret, th1 = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return th1

def hsv_thresholding(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame, lower_black, upper_black)
    # mask_inv = cv2.bitwise_not(mask)
    return mask




# img = cv2.imread("../pictures/syringe_scale_test1.png")
# # cv2.imshow("test", img)
# img = img_thresholding(img)
# cv2.imshow('frame', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

lower_black = np.array([0,0,0])
upper_black = np.array([180,255,5])

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # print("fps", cap.get(cv2.CAP_PROP_FPS))
    # print(frame.shape)

    # frame_thresholding = img_thresholding(frame)
    frame_thresholding = hsv_thresholding(frame)

    cv2.imshow('org', frame)
    cv2.imshow('thread', frame_thresholding)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
