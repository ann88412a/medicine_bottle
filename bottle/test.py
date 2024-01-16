import cv2
import numpy as np
###
# 讀取中文路徑圖檔(圖片讀取為BGR)
def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img

# 點擊欲判定HSV值的圖片位置(以滑鼠左鍵單擊)
def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("BGR:", img[y, x])
        print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])
        print('='*30)


def auto_canny(image, sigma=0.2):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def prewitt(image):
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    img_prewittx = cv2.filter2D(image, -1, kernelx)
    img_prewitty = cv2.filter2D(image, -1, kernely)
    return img_prewittx + img_prewitty

if __name__ == '__main__':
    # 讀取圖檔
    img = cv_imread(r'C:\Users\ken88\Downloads\test1.jpg')
    # img = cv2.resize(img, (320, 240))
    # 轉換成gray與HSV
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bilateralFilter_img = cv2.bilateralFilter(img, 9, 41, 41)
    from cv2.ximgproc import guidedFilter
    guidedFilter_img = guidedFilter(bilateralFilter_img, img, 9, 0.1**2)

    # guidedFilter_img = auto_canny(cv2.cvtColor(guidedFilter_img, cv2.COLOR_BGR2GRAY))
    # bilateralFilter_img = auto_canny(cv2.cvtColor(bilateralFilter_img, cv2.COLOR_BGR2GRAY))
    # img = auto_canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    guidedFilter_img = prewitt(cv2.cvtColor(guidedFilter_img, cv2.COLOR_BGR2GRAY))
    bilateralFilter_img = prewitt(cv2.cvtColor(bilateralFilter_img, cv2.COLOR_BGR2GRAY))
    img = prewitt(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.namedWindow("img")
    # cv2.setMouseCallback("img", mouse_click)
    while True:
        # cv2.imshow('org_img', img)
        cv2.imshow('bilateralFilter_img, org_img, guidedFilter_img', np.concatenate((bilateralFilter_img, img, guidedFilter_img), axis=0))
        # cv2.imshow('bilateralFilter_img', bilateralFilter_img)
        # cv2.imshow('guidedFilter_img', guidedFilter_img)
        if cv2.waitKey() == ord('q'):
            break
    cv2.destroyAllWindows()