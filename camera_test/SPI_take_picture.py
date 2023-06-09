import cv2
import numpy as np

#SPI

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

sharpen_kernel = np.array([[0,-1,0],
                         [-1,5,-1],
                         [0,-1,0]])

edge_kernel = np.array([[-1,-1,-1],
                         [-1,9,-1],
                        [-1,-1,-1]])

def  take_picture():
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER) #RGB 
    
    ret,frame = cap.read()
    # cv2.imshow('take_picture',frame)
    # sharpen_img = cv2.filter2D(src=frame,ddepth=-1,kernel=kernel)
    # edge_img = cv2.filter2D(src=frame,ddepth=-1,kernel=edge_kernel)
    frame = cv2.addWeighted(frame, 4, cv2.blur(frame, (80, 80)), -4, 128)
    canny = cv2.Canny(frame,100,250)
    
    cv2.imwrite('./pictures/test.png',canny)

    
if __name__ == "__main__":
    take_picture()