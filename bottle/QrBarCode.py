try:
    from cv2 import cv2
except:
    import cv2
import numpy as np
from pyzbar import pyzbar

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    barcodes = pyzbar.decode(gray)
    barcodeData = ''
    # 迴圈檢測到的條形碼
    for barcode in barcodes:
        # 提取條形碼的邊界框的位置 畫出影象中條形碼的邊界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # 條形碼資料為位元組物件，所以如果我們想在輸出影象上
        # 畫出來，就需要先將它轉換成字串
        barcodeData = barcode.data.decode("utf-8")

        # 繪出影象上條形碼的資料和條形碼型別
        text = "{} ({})".format(barcodeData, barcode.type)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

        #   # 向終端列印條形碼資料和條形碼型別
        #   print("[INFO] Found {} barcode: {}".format(barcode.type, barcodeData))
        # print(barcodeData)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
