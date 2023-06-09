# import the opencv library
import cv2

import datetime
# urllib3
import urllib.request

# google Drive API
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import auth

import os



def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False
    
def upload(img_name):
    SCOPES = 'https://www.googleapis.com/auth/drive'
    # your google drive API OAuth
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Drive API'
    authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
    creds = authInst.getCredentials()

    try:
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': img_name,
                         'parents': ['1alAFW3FNHh2NY1fFFMLNHIWg5P83ubdh']}

        media = MediaFileUpload(img_name, mimetype='image/jpeg')
        
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None



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


flag = 0

def take_pic(event, x, y, flags, param):
    
    if event == 1:
        now = datetime.datetime.now()
        now = now.strftime('%m_%d_%H_%M_%S')
        print('hi', now, x, y)
        cv2.imwrite(str(now) + str(flag) + '.jpg', frame)
        upload(str(now) + str(flag) + '.jpg')
        os.remove(str(now) + str(flag) + '.jpg')
        if (x <= 80 and y <= 80):
            # After the loop release the cap object
            vid.release()
            # Destroy all the windows
            cv2.destroyAllWindows()




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

        
        show = frame.copy()
        # Using cv2.putText() method
        show = cv2.putText(show, 'X', org, font, fontScale, color, thickness, cv2.LINE_AA)
        
        if flag == 1500:
            flag = 0
            if connect():
                is_connect = 1
            else:
                is_connect = 0
        flag = flag + 1

        if is_connect:
            show = cv2.putText(show, 'connect', (500, 20), font, 1, (0, 255, 0), thickness, cv2.LINE_AA)
        else:
            show = cv2.putText(show, 'no connect', (450, 20), font, 1, (0, 0, 255), thickness, cv2.LINE_AA)
        

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

