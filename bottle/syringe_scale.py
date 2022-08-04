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

class syringe_scale:
    def __init__(self):
        pass
    def img_thresholding(self, img):
        img = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 5)
        ret, th1 = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
        # th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        # th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return th1

    def hsv_thresholding(self, img, threshold=15):
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, threshold])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, lower_black, upper_black)
        # mask_inv = cv2.bitwise_not(mask)
        return mask

    def get_scall_raw(self, img):
        bin_img = self.hsv_thresholding(img, 40)
        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(bin_img, kernel, iterations=1)
        # kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(erosion, kernel, iterations=1)

        #
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)>0:
            x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
            # cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            # cv2.drawContours(img, contours, 0, (0, 255, 255), 3)
            return cv2.line(img, (0, y), (img.shape[1], y), (0, 0, 255), 2)
        else:
            return img

# img = cv2.imread("../pictures/syringe_scale_test1.png")
# # cv2.imshow("test", img)
# img = img_thresholding(img)
# cv2.imshow('frame', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


if(__name__ == "__main__"):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    sc = syringe_scale()
    while(True):
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # height, width, channels = frame.shape
        # print("fps", cap.`get(cv2.CAP_PROP_FPS))
        # print(frame.shape) # (640, 480, 3)

        # frame_thresholding = img_thresholding(frame)
        # frame_thresholding = hsv_thresholding(frame)
        frame_scall = sc.get_scall_raw(frame)




        # cv2.imshow('org', frame)
        # cv2.imshow('thread', frame_thresholding)
        # cv2.imshow('erode', erosion)
        # cv2.imshow('dilate', dilation)
        cv2.imshow("frame_scall", frame_scall)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
