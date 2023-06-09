# import the opencv library
import cv2

import datetime
# urllib3
import urllib.request




def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False



# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# font
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (15, 50)

# fontScale
fontScale = 2

# Blue color in BGR
color = (0, 0, 255)

# Line thickness of 2 px
thickness = 2

def take_pic(event, x, y, flags, param):
    
    if event == 1:
        now = datetime.datetime.now()
        now = now.strftime('%d_%H_%M_%S')
        print('hi', now, x, y)
        if (x <= 80 and y <= 80):
            # After the loop release the cap object
            vid.release()
            # Destroy all the windows
            cv2.destroyAllWindows()


# 0AGEblZO1RZrkUk9PVA
flag = 0
is_connect = 0

if connect():
    is_connect = 1

if __name__ == '__main__':

    # opencv
    while(True):
        global frame
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        
        
        # Using cv2.putText() method
        show = cv2.putText(frame, 'X', org, font, fontScale, color, thickness, cv2.LINE_AA)
        
        if flag == 1500:
            flag = 0
            if connect():
                is_connect = 1
            else:
                is_connect = 0
        flag = flag + 1

        if is_connect:
            show = cv2.putText(frame, 'connect', (500, 20), font, 1, (0, 255, 0), thickness, cv2.LINE_AA)
        else:
            show = cv2.putText(frame, 'no connect', (450, 20), font, 1, (0, 0, 255), thickness, cv2.LINE_AA)
        

        # Display the resulting frame
        cv2.imshow('frame', show)
        cv2.setMouseCallback('frame', take_pic)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


# import cv2
# import numpy as np
 
# # Create point matrix get coordinates of mouse click on image
# point_matrix = np.zeros((2,2),np.int)
 
# counter = 0
# def mousePoints(event,x,y,flags,params):
#     global counter
#     # Left button mouse click event opencv
#     if event == cv2.EVENT_LBUTTONDOWN:
#         point_matrix[counter] = x,y
#         counter = counter + 1
 
# # Read image
# img = cv2.imread('pill/cyho/chart_yolov4-tiny-custom.png')
 
# while True:
#     for x in range (0,2):
#         cv2.circle(img,(point_matrix[x][0],point_matrix[x][1]),3,(0,255,0),cv2.FILLED)
 
#     if counter == 2:
#         starting_x = point_matrix[0][0]
#         starting_y = point_matrix[0][1]
 
#         ending_x = point_matrix[1][0]
#         ending_y = point_matrix[1][1]
#         # Draw rectangle for area of interest
#         cv2.rectangle(img, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), 3)
 
#         # Cropping image
#         img_cropped = img[starting_y:ending_y, starting_x:ending_x]
#         cv2.imshow("ROI", img_cropped)
 
#     # Showing original image
#     cv2.imshow("Original Image ", img)
#     # Mouse click event on original image
#     cv2.setMouseCallback("Original Image ", mousePoints)
#     # Printing updated point matrix
#     print(point_matrix)
#     # Refreshing window all time
#     cv2.waitKey(1)