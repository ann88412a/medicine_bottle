from cv2 import cv2
import numpy as np
from PIL import Image
import pytesseract

# a= np.array()
cap = cv2.VideoCapture(0)

while(True):
  ret, frame = cap.read()
  frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
  cv2.imshow('frame', frame)
  text = pytesseract.image_to_string(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), lang='eng')  # 讀英文
  print(text)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
