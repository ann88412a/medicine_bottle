# Using usb webcam on Jetson Nano had to install opencv with apt-get
# sudo apt-get update
# sudo apt-get upgrade -y
# sudo apt-get install build-essential nano
# sudo apt-get install python3-opencv

import cv2

cap = cv2.VideoCapture(0)

while(True):
  ret, frame = cap.read()
  cv2.imshow('frame', frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
