import numpy as np
import cv2
from numpy.core.fromnumeric import shape
from scipy.spatial import distance
import statistics

img = cv2.imread('/home/medical/medicine_bottle/pictures/orignal_input.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5),0)
# _, thrash = cv2.threshold(gray,100, 250, cv2.THRESH_BINARY)
# cv2.imshow("thrash", thrash)
# cv2.imshow("a", blurred)
cannied = cv2.Canny(np.asarray(blurred), 150, 200)
cv2.imshow("b", cannied)
cv2.imwrite('./pictures/all_shape.png',cannied)

#--------------------detect circle--------------------------
circles = cv2.HoughCircles(cannied, cv2.HOUGH_GRADIENT, 1, 100,
                                param1=100, param2=20, minRadius=10, maxRadius=60)
# circles = cv2.HoughCircles(cannied, cv2.HOUGH_GRADIENT, 1, 100,
#                               param1=350, param2=30, minRadius=20, maxRadius=60)
circle_coordinate = []
if len(circles) != 0:
    for i in circles[0,:]:
        # draw the outer circle
        image1 = cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        print('圓心座標:', i[0], i[1])
        circle_coordinate.append([i[0],i[1]])
        print('圓心半徑:', i[2])
        # draw the center of the circle
        cv2.putText(img, "circle", (i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
        images = cv2.circle(image1, (i[0], i[1]), 2, (0, 255,0), 3)
# cv2.imshow("circles", images)
#--------------------detect circle--------------------------

#--------------------detect muti side shape----------------------
# _,contours, h = cv2.findContours(gray, 1, 2)
_,contours, _ = cv2.findContours(cannied, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

avgArray = []
for cnt in contours:
    #--------------------detect triangle----------------------
    approx_a = cv2.approxPolyDP(cnt,22,True)
    x = approx_a.ravel()[0]
    y = approx_a.ravel()[1] - 5
    if len(approx_a) == 3:
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
        cv2.drawContours(img, [approx_a], 0, (0,0, 255), 5)
    # cv2.imshow("triangle", img)
    #--------------------detect triangle----------------------
    
    #--------------------detect ellipses--------------------------
    approx = cv2.approxPolyDP(cnt, 0.0001 * cv2.arcLength(cnt, True), True)
    
    x_e = approx.ravel()[0]
    y_e = approx.ravel()[1] - 5
    ellipse_coordinate = [x_e,y_e]
    if len(approx) >= 35 :
        distance_list = [distance.euclidean(ellipse_coordinate, circle_c) for circle_c in circle_coordinate]
        distance_list = [True for item in distance_list if item <= 60]
        if True not in distance_list:
            cv2.putText(img, "ellipses"+str(len(approx)), (x_e, y_e), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
            cv2.drawContours(img, [approx], 0, (0,0,0), 5)
    #--------------------detect ellipses--------------------------

    #--------------------detect square--------------------------

    if len(approx_a) == 4:
        square_coordinate = [x,y]
        distance_list = [distance.euclidean(square_coordinate, circle_c) for circle_c in circle_coordinate]
        distance_list = [True for item in distance_list if item <= 50]
        if True not in distance_list and len(approx) < 35:
            cv2.putText(img, "4_side_shape"+str(x)+','+str(y), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))
            cv2.drawContours(img, [approx_a], 0, (255,0,0), 5)
    # cv2.imshow("square", img)

    #--------------------detect square--------------------------


   

# print((avgArray))
# edges = statistics.median(avgArray)
# print(edges)

# if edges < 15:
#     shape = "OVAL"
#     # cv2.drawContours(photo, [cnt], 0, 255, -1)
# # elif edges == 3:
# #     print("triangle")
# #     cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
# # elif edges == 4:
# #     print("square")
# #     cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
# # elif edges == 9:
# #     print("half-circle")
# #     cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
# elif edges > 15:
#     shape = "CIRCLE"
    
# print(shape)

cv2.imshow("shapes", img)


cv2.waitKey(0)
cv2.imwrite('./pictures/detect_all.png',img)
cv2.destroyAllWindows()