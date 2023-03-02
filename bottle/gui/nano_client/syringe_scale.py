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
    def __init__(self, homography):
        self.__homography = homography
        pass

    def image_homography(self, img):  # (1080, 1920, 3) -> (1000, 250, 3)
        # w, h = 1020, 260
        w, h = 1200, 260
        pts1 = np.float32(self.__homography)
        pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        H, _ = cv2.findHomography(pts1, pts2, method=cv2.RANSAC, ransacReprojThreshold=3.0)
        img = cv2.warpPerspective(img, H, (w, h), flags=cv2.INTER_LINEAR)
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        # print(img.shape)
        return img[150:w - 50, 5:-5]

    def image_preprocessing(self, last_frame, cur_frame, syringe_type):
        frame1 = self.image_homography(last_frame)
        frame2 = self.image_homography(cur_frame)
        img = np.mean([frame1, frame2], axis=0).astype(np.uint8)  # get 2 frame mean

        if syringe_type == "1 ml":
            img = img[230:-40, 70:-70]
        elif syringe_type == "3 ml":
            img = img[360:-30, 60:-60]
        elif syringe_type == "5 ml":
            img = img[290:, 45:-45]
        elif syringe_type == "10 ml":
            img = img[70:-10, 30:-30]
        elif syringe_type == "100 units":
            img = img[230:-20, 80:-80]
        elif syringe_type == "others":
            img = img[440:-110, 70:-70]
        else:
            print("Syringe type input error!! your input:", syringe_type)
        # img = cv2.resize(img, (250, 1000))
        # img_ratio = 1.5
        # img = cv2.resize(img, None, fx=img_ratio, fy=img_ratio)
        # print(img.shape)
        return img

    def hsv_thresholding(self, img, threshold=40):
        lower_black = np.array([100, 90, 40], np.uint8)
        upper_black = np.array([130, 230, 40+threshold], np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, lower_black, upper_black)
        # mask = cv2.bitwise_not(mask)
        # mask = cv2.dilate(mask, np.ones((3, 5), np.uint8), iterations=2)
        mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)
        mask = cv2.dilate(mask, np.ones((7, 7), np.uint8), iterations=1)
        # mask = cv2.erode(mask, np.ones((5, 5), np.uint8), iterations=2)
        return mask

    def auto_canny(self, img, sigma=0.3):
        # compute the median of the single channel pixel intensities
        v = np.median(img)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(img, lower, upper)
        return edged

    def find_plunger_tip(self, img, syringe_type, threshold=40, first_call=True):
        img = img.copy()
        img[self.hsv_thresholding(img, threshold) == 0] = [255, 255, 255]  # only save the target color
        bilateralFilter_img = cv2.bilateralFilter(img, 9, 50, 50)  # blur
        auto_canny_img = self.auto_canny(bilateralFilter_img)
        # auto_canny_img = cv2.bitwise_not(auto_canny_img)
        # auto_canny_img = cv2.erode(auto_canny_img, np.ones((3, 3), np.uint8), iterations=1)
        auto_canny_img = cv2.dilate(auto_canny_img, np.ones((3, 5), np.uint8), iterations=2)
        auto_canny_img = cv2.erode(auto_canny_img, np.ones((5, 7), np.uint8), iterations=1)

        contours, hierarchy = cv2.findContours(auto_canny_img, cv2.CHAIN_APPROX_SIMPLE, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            # (x, y), radius = cv2.minEnclosingCircle(contour)
            # center = (int(x), int(y))
            # radius = int(radius)
            # # cv2.circle(img, center, radius, (0, 255, 0), 2)
            # # cv2.drawContours(img, contour, -1, (255,0,0), cv2.FILLED)

            for c in range(len(contours)):
                if cv2.contourArea(contours[c]) > 1000:
                    # print(cv2.contourArea(contours[c]))
                    cv2.fillPoly(contours[c], [contours[c]], (0, 0, 255))

            contour = max(contours, key=cv2.contourArea)  # max Area contour
            # cv2.fillPoly(img, [contour], (255, 0, 0))
            # # print("arcLength", cv2.arcLength(contour, True))
            # img_ratio = 0.8
            # cv2.imshow("frame_scall", cv2.resize(img, None, fx=img_ratio, fy=img_ratio))
            return contour
        return None

    def get_plunger_tip_dist(self, img, syringe_type, threshold=40):
        contour = self.find_plunger_tip(img, syringe_type, threshold)
        if contour is not None:
            # (x, y), radius = cv2.minEnclosingCircle(contour)
            # center = (int(x), int(y))
            # radius = int(radius)
            # cv2.circle(img, center, radius, (0, 255, 0), 2)
            # cv2.drawContours(img, contour, -1, (255,0,0), cv2.FILLED)
            # cv2.fillPoly(img, [contour], (255, 0, 0))
            # print("arcLength", cv2.arcLength(contour, True))
            ## find the centroid of this contour
            M = cv2.moments(contour)
            X, Y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])


            return X, Y
        return None

    def syringe_pixel2unit(self, pixel_y, syringe_type):
        # def precision_0point2(num):
        #     if num % 0.2 > 0:
        #         return num+0.1
        #     else:
        #         return num
        return {
            "1 ml": (round(pixel_y/665, 2), pixel_y),
            "3 ml": (abs(round((pixel_y-58)/530*3, 1)), pixel_y),
            "5 ml": (abs(round((pixel_y-75)/512*5, 1)), pixel_y),
            "10 ml": (abs(round((pixel_y-68)/750*10, 1)), pixel_y),
            "100 units": (pixel_y/82, pixel_y),
            "others": (pixel_y/82, pixel_y)
        }[syringe_type]

    def get_scale(self, last_frame, cur_frame, syringe_type="others", threshold=40):  # draw
        img = self.image_preprocessing(last_frame.copy(), cur_frame.copy(), syringe_type)
        plunger_tip = self.get_plunger_tip_dist(img, syringe_type, threshold=threshold)  # get tip xy
        # plunger_tip = self.get_plunger_tip_dist(img.copy(), threshold=threshold)  # get tip xy

        scale = None
        # cv2.putText(img, "type: "+syringe_type, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
        # print("type: " + syringe_type)

        if plunger_tip is not None:
            scale, tip_y = self.syringe_pixel2unit(plunger_tip[1], syringe_type)
            # cv2.line(img, (0, plunger_tip_value), (img.shape[1], plunger_tip_value), (0, 0, 255), 2)
            # cv2.circle(img, plunger_tip, 7, (0, 255, 0), -1)
            cv2.line(img, (0, tip_y), (img.shape[1], tip_y), (0, 0, 255), 2)
            # cv2.putText(img, "scale: " + str(round(scale, 1)), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
            # print("scale: " + str(scale), str(plunger_tip[1]))
        else:
            # cv2.putText(img, "scale: Null", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
            # print("scale: Null")
            pass
        # print("\n\n\n\n\n")
        return img, scale


if(__name__ == "__main__"):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    sc = syringe_scale([[684, 387], [1897, 370], [680, 675], [1902, 695]])
    last_ret, last_frame = cap.read()
    while(True):
        ret, cur_frame = cap.read()
        # ret, frame = cap.read()
        # height, width, channels = frame.shape
        # print("fps", cap.`get(cv2.CAP_PROP_FPS))
        # print(frame.shape)
        frame_scall, scale_value = sc.get_scale(last_frame, cur_frame, syringe_type="10 ml")
        print(scale_value)
        img_ratio = 1000/frame_scall.shape[0]
        cv2.imshow("frame_scall", cv2.resize(frame_scall, None, fx=img_ratio, fy=img_ratio))



        last_frame = cur_frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


# 模板匹配