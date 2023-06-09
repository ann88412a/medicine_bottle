
import imp
import cv2
import os
import time

cap = cv2.VideoCapture(0)
# cap.set(15, 10)
# cap.set(cv2.CAP_PROP_EXPOSURE, 40) 

# ---------------local version------------
# while(True):
#     ret, frame = cap.read()
    
#     # frame = cv2.addWeighted(frame, 4, cv2.blur(frame, (80, 80)), -4, 128)   
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
        
#         cv2.imwrite('./pictures/orignal_input.png',frame)
#         break

# ---------------remote version-----------
# for i in range(5):

#     ret, frame = cap.read()
#     time.sleep(1)
# cv2.imwrite('./pictures/orignal_input.png',frame)
# print('save done!!')

# ---------------recoding data-------------
i = 0
while(True):
    ret, frame = cap.read()
    
    # frame = cv2.addWeighted(frame, 4, cv2.blur(frame, (80, 80)), -4, 128)   
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('r'):
        i = i+1
        cv2.imwrite('/Users/zhuangdongsheng/Documents/medicine_bottle/camera_test/data/Sennoside_2/Sennoside_'+str(i)+'.png',frame)
        print('save '+str(i))
        # cv2.imwrite('/home/medical/medicine_bottle/pill/yolov4/darknet/test.png',frame)
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

