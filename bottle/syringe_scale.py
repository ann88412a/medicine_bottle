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

    def auto_canny(self, img, sigma=0.2):
        # compute the median of the single channel pixel intensities
        v = np.median(img)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(img, lower, upper)
        return edged

    def get_plunger_tip_dist(self, img):
        img[self.hsv_thresholding(img) == 0] = [255, 255, 255]  # only save the target color
        bilateralFilter_img = cv2.bilateralFilter(img, 9, 50, 50)  # blur
        auto_canny_img = self.auto_canny(bilateralFilter_img)

        dilation = cv2.dilate(auto_canny_img, np.ones((3, 3), np.uint8), iterations=3)
        erosion = cv2.erode(dilation, np.ones((5, 5), np.uint8), iterations=1)

        contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)  # max Area contour
            # cv2.drawContours(img, contour, -1, (255,0,0), 5)
            ## find the centroid of this contour
            M = cv2.moments(contour)
            X, Y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            return X, Y
        return None

    def hsv_thresholding(self, img, threshold=70):
        lower_black = np.array([107, 225, 40], np.uint8)
        upper_black = np.array([115, 252, 40+threshold], np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, lower_black, upper_black)
        # mask_inv = cv2.bitwise_not(mask)
        return mask

    # def get_plunger_tip_value(self, img):
    #     bin_img = self.hsv_thresholding(img)
    #     kernel = np.ones((5, 5), np.uint8)
    #     erosion = cv2.erode(bin_img, kernel, iterations=1)
    #     # kernel = np.ones((5, 5), np.uint8)
    #     dilation = cv2.dilate(erosion, kernel, iterations=1)
    #     contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #     if len(contours)>0:
    #         x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
    #         cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
    #         # cv2.drawContours(img, contours, 0, (0, 255, 255), 3)
    #         return y
    #     else:
    #         return None

    def get_scale(self, img):  # draw
        plunger_tip_dist = self.get_plunger_tip_dist(img.copy())
        if plunger_tip_dist is not None:
            # cv2.line(img, (0, plunger_tip_value), (img.shape[1], plunger_tip_value), (0, 0, 255), 2)
            cv2.circle(img, (plunger_tip_dist), 7, (0, 255, 0), -1)
            cv2.line(img, (0, plunger_tip_dist[1]), (img.shape[1], plunger_tip_dist[1]), (0, 0, 255), 2)
        return img

        # return self.get_plunger_tip_dist(img)


if(__name__ == "__main__"):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    sc = syringe_scale()
    x, y, w, h = 390, 850, 300, 1000

    while(True):
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = frame[y:y+h, x:x+w]
        # height, width, channels = frame.shape
        # print("fps", cap.`get(cv2.CAP_PROP_FPS))
        # print(frame.shape)

        # frame_thresholding = img_thresholding(frame)
        # frame_thresholding = hsv_thresholding(frame)
        frame_scall = sc.get_scale(frame)

        # cv2.imshow('org', frame)
        # cv2.imshow('thread', frame_thresholding)
        # cv2.imshow('erode', erosion)
        # cv2.imshow('dilate', dilation)

        img_ratio = 0.8
        cv2.imshow("frame_scall", cv2.resize(frame_scall, None, fx=img_ratio, fy=img_ratio))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
