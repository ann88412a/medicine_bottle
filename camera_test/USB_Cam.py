# Using usb webcam on Jetson Nano had to install opencv with apt-get
# sudo apt-get update
# sudo apt-get upgrade -y
# sudo apt-get install build-essential nano
# sudo apt-get install python3-opencv

import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# cap.set(cv2.CAP_PROP_EXPOSURE,-10)

while(True):
  ret, frame = cap.read()
  print(ret,frame)
  cv2.imshow('frame', cv2.resize(frame, None, fx=0.3, fy=0.3))
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
