try:
    # fix opencv open webcam slowly bug in WIN10
    import os
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    # call cv2 in WIN10
    from cv2 import cv2
except:
    import cv2
import numpy as np
from pyzbar import pyzbar



def barcode_decoder(frame, show_type=None):
    bar_info = [None]
    detect_obj = cv2.barcode_BarcodeDetector()
    is_barcode, points = detect_obj.detect(frame)
    # is_ok, bar_info, bar_type, points = detect_obj.detectAndDecode(frame)

    if(is_barcode):
        is_ok, bar_info, bar_type = detect_obj.decode(frame, points)
        if (is_ok):
            if(show_type == 'print'):
                print('bar_info:', bar_info)
                print('bar_type:', bar_type)
                print('points:', points)
                print("\n")
            elif(show_type == 'draw'):
                # draw bbox
                for pos in points:
                    color = (0, 0, 255)
                    thick = 3
                    for p in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                        start = int(pos[p[0]][0]), int(pos[p[0]][1])
                        end = int(pos[p[1]][0]), int(pos[p[1]][1])
                        cv2.line(frame, start, end, color, thick)

                text = "{} ({})".format(bar_info[0], bar_type[0])
                cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)
        else:
            pass
            # phmacode
    return frame, bar_info[0]



cap = cv2.VideoCapture(0)

from pylibdmtx.pylibdmtx import decode as dm_decode


while(True):
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
    # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    # print(width, height, fps)


    # print(dm_decode(frame, timeout=30, max_count=1))




    frame, bar_info = barcode_decoder(frame, show_type='draw')


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
