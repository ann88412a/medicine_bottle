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

# 讀取中文路徑圖檔(圖片讀取為BGR)
def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img

# 點擊欲判定HSV值的圖片位置(以滑鼠左鍵單擊)
def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("x,y: {}, {}".format(x,y))
        # print("BGR:", frame[y, x])
        # print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])
        print('='*30)

def image_homography(img):  # (1080, 1920, 3) -> (1000, 250, 3)
    # w, h = 1020, 260
    w, h = 1200, 260
    pts1 = np.float32([[684, 387], [1897, 370], [680, 675], [1902, 695]])
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    H, _ = cv2.findHomography(pts1, pts2, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    img = cv2.warpPerspective(img, H, (w, h), flags=cv2.INTER_LINEAR)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    # return img[450:1450, 5:-5]
    # print(img.shape)
    return img[150:w-50, 5:-5]

def image_preprocessing(last_frame, cur_frame):
    frame1 = image_homography(last_frame)
    frame2 = image_homography(cur_frame)
    img = np.mean([frame1, frame2], axis=0).astype(np.uint8)  # get 2 frame mean
    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    _, last_frame = cap.read()

    while (True):
        # ret, frame = cap.read()
        ret, cur_frame = cap.read()
        frame = image_preprocessing(last_frame, cur_frame)
        last_frame = cur_frame


        # print(frame.shape)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.namedWindow("frame")
        cv2.setMouseCallback("frame", mouse_click)

        # print(frame.shape)

        img_ratio = 0.8
        cv2.imshow("frame", cv2.resize(frame, None, fx=img_ratio, fy=img_ratio))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



