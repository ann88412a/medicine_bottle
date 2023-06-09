try:
    # fix opencv open webcam slowly bug in WIN10
    import os
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    # call cv2 in WIN10
    from cv2 import cv2
except:
    import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode as dm_decode




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
                # print('bar_type:', bar_type)
                # print('points:', points)
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

                text = "{}".format(bar_info[0])
                cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 1)
        else:
            # pharmacode
            if (show_type == 'print'):
                print('bar_info: Unknown')
                print("\n")
            elif (show_type == 'draw'):
                # draw bbox
                for pos in points:
                    color = (0, 0, 255)
                    thick = 3
                    for p in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                        start = int(pos[p[0]][0]), int(pos[p[0]][1])
                        end = int(pos[p[1]][0]), int(pos[p[1]][1])
                        cv2.line(frame, start, end, color, thick)

                text = "{}".format("Unknown")
                cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 1)
    return frame, bar_info[0]

def data_matrix_decode(frame, show_type=None):
    dm_info = None
    height, width = frame.shape[:2]
    decode_info = dm_decode(frame, timeout=35, max_count=1)
    if len(decode_info) != 0:
        dm_info = decode_info[0][0].decode()
        if (show_type == 'print'):
            print('dm_info:', dm_info)
            print("\n")
        elif (show_type == 'draw'):
            # draw bbox
            x = decode_info[0][1][0]
            y = height - decode_info[0][1][1]
            w = decode_info[0][1][2]
            h = decode_info[0][1][3]
            cv2.rectangle(frame, (x, y), (x + w, y - h), (0, 0, 255), 2)
            text = "{}".format(dm_info)
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 1)
    return frame, dm_info





cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    # print("fps", cap.get(cv2.CAP_PROP_FPS))

    frame, bar_info = barcode_decoder(frame, show_type='draw')
    frame, dm_info = data_matrix_decode(frame, show_type='draw')
    # print("bar_info", bar_info)
    # print("dm_info", dm_info)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
