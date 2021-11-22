import numpy as np
import cv2
from numpy.core.fromnumeric import shape

# img = cv2.imread('/home/medical/medicine_bottle/pictures/test.png')
# # cv2.imshow("1", img)
# print(np.array(img).shape)
# imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # cv2.imshow('2',imgGrey)
# print('hi',np.array(imgGrey).shape)
# _, thrash = cv2.threshold(imgGrey,170, 180, cv2.THRESH_BINARY)
# _,contours, _ = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

# print(np.array(contours).shape)

# for contour in contours:
#     approx = cv2.approxPolyDP(contour, 0.005* cv2.arcLength(contour, True), True)
#     # approx = cv2.approxPolyDP(contour,20,True)
#     # cv2.drawContours(img, [approx], 0, (255,0, 0), 5)
#     # print(approx)
#     x = approx.ravel()[0]
#     y = approx.ravel()[1] - 5
#     # if len(approx) == 3:
#     #     cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
#     #     cv2.drawContours(img, [approx], 0, (0,0, 255), 5)
#     # elif len(approx) == 4:
#     #     x1 ,y1, w, h = cv2.boundingRect(approx)
#     #     aspectRatio = float(w)/h
#     #     # print(aspectRatio)
#     #     if aspectRatio >= 0.95 and aspectRatio <= 1.05:
#     #       cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
#     #     else:
#     #       cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
#     if len(approx) > 10:
#         cv2.drawContours(img, [approx], 0, (0,0, 255), 5)
#         cv2.putText(img, "similar_circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    
# cv2.imshow("shapes", img)
# cv2.waitKey(0)
# cv2.imwrite('./pictures/triangle_detect.png',img)
# cv2.destroyAllWindows()

import statistics

img = cv2.imread('/home/medical/medicine_bottle/pictures/test.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5),0)
# _, thrash = cv2.threshold(gray,100, 250, cv2.THRESH_BINARY)
# cv2.imshow("thrash", thrash)
# cv2.imshow("a", blurred)
cannied = cv2.Canny(np.asarray(blurred), 150, 200)
cv2.imshow("b", cannied)

# _,contours, h = cv2.findContours(gray, 1, 2)
_,contours, _ = cv2.findContours(cannied, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

avgArray = []
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    avgArray.append(len(approx))

    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5

    cv2.putText(img, "test"+str(cnt), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))
    cv2.drawContours(img, [approx], 0, (255,0,0), 5)

print((avgArray))
edges = statistics.median(avgArray)
print(edges)

if edges < 15:
    shape = "OVAL"
    # cv2.drawContours(photo, [cnt], 0, 255, -1)
# elif edges == 3:
#     print("triangle")
#     cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
# elif edges == 4:
#     print("square")
#     cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
# elif edges == 9:
#     print("half-circle")
#     cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
elif edges > 15:
    shape = "CIRCLE"
    
print(shape)

cv2.imshow("shapes", img)


cv2.waitKey(0)
# cv2.imwrite('./pictures/4_side_shape_detect.png',img)
cv2.destroyAllWindows()