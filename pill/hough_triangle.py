# import cv2
# import numpy as np

# image_obj = cv2.imread('/home/medical/medicine_bottle/pictures/test.png')
# cv2.imshow('My Image', image_obj)
    
# gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)

# kernel = np.ones((4, 4), np.uint8)
# dilation = cv2.dilate(gray, kernel, iterations=1)

# blur = cv2.GaussianBlur(dilation, (5, 5), 0)


# thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

# # Now finding Contours         ###################
# _, contours, _ = cv2.findContours(
#     thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# coordinates = []
# for cnt in contours:
#         # [point_x, point_y, width, height] = cv2.boundingRect(cnt)
#     approx = cv2.approxPolyDP(
#         cnt, 0.07 * cv2.arcLength(cnt, True), True)
#     if len(approx) == 3:
#         coordinates.append([cnt])
#         cv2.drawContours(image_obj, [cnt], 0, (0, 0, 255), 3)

# cv2.imwrite("result.png", image_obj)

import numpy as np
import cv2
from numpy.core.fromnumeric import shape

img = cv2.imread('/home/medical/medicine_bottle/pictures/test.png')
# cv2.imshow("1", img)
print(np.array(img).shape)
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('2',imgGrey)
print('hi',np.array(imgGrey).shape)
_, thrash = cv2.threshold(imgGrey,200, 190, cv2.THRESH_BINARY)
_,contours, _ = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

print(np.array(contours).shape)

for contour in contours:
    # approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    approx = cv2.approxPolyDP(contour,20,True)
    # cv2.drawContours(img, [approx], 0, (255,0, 0), 5)
    # print(approx)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
        cv2.drawContours(img, [approx], 0, (0,0, 255), 5)
    # elif len(approx) == 4:
    #     x1 ,y1, w, h = cv2.boundingRect(approx)
    #     aspectRatio = float(w)/h
    #     # print(aspectRatio)
    #     if aspectRatio >= 0.95 and aspectRatio <= 1.05:
    #       cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    #     else:
    #       cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    # elif len(approx) == 5:
    #     cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    # elif len(approx) == 10:
    #     cv2.putText(img, "Star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    # else:
    #     cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))


cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.imwrite('./pictures/triangle_detect.png',img)
cv2.destroyAllWindows()


