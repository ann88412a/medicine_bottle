try:
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
cap.set(cv2.CAP_PROP_EXPOSURE, -6)

while(True):
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # detect_obj = cv2.QRCodeDetector()
    # # qr_info, points, qr_img = detect_obj.detectAndDecode(frame)
    # # print('qr_info:', qr_info)
    # is_ok, points = detect_obj.detect(frame)
    # if(is_ok):
    #     # print('is_ok:', is_ok)
    #     # print('points:', points)
    #     # print("\n")
    #     qr_info, qr_img = detect_obj.decode(frame, points)
    #     print('qr_info:', qr_info)
    #     print('qr_img.shape:', qr_img.shape)
    #     print('qr_img:', qr_img)


    # frame, bar_info = barcoder_decode(frame, show_type='draw')


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
