
import cv2
import os

cap = cv2.VideoCapture(0)
# cap.set(15, 10)
# cap.set(cv2.CAP_PROP_EXPOSURE, 40) 


while(True):
    ret, frame = cap.read()
    
    # frame = cv2.addWeighted(frame, 4, cv2.blur(frame, (80, 80)), -4, 128)   
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        cv2.imwrite('./pictures/orignal_input.png',frame)
        break

cap.release()
cv2.destroyAllWindows()

