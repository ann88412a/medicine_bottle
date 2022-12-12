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
        print("BGR:", frame[y, x])
        print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])
        print('='*30)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    while (True):
        ret, frame = cap.read()
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.namedWindow("frame")
        cv2.setMouseCallback("frame", mouse_click)

        img_ratio = 1
        cv2.imshow("frame", cv2.resize(frame, None, fx=img_ratio, fy=img_ratio))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



