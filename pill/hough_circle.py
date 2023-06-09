import cv2
import numpy as np

def circle(image):

#   img = cv2.medianBlur(image, 5)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5),0)
    # _, thrash = cv2.threshold(gray,100, 250, cv2.THRESH_BINARY)
    # cv2.imshow("thrash", thrash)
    # cv2.imshow("a", blurred)
    cannied = cv2.Canny(np.asarray(blurred), 150, 200)
    cv2.imshow("can", cannied)
    #print('the shape of cimg: ', cannied.shape)
    # circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,
    #                             param1=100,param2=30,minRadius=40, maxRadius=70)
    circles = cv2.HoughCircles(cannied, cv2.HOUGH_GRADIENT, 1, 100,
                                param1=100, param2=20, minRadius=10, maxRadius=60)
    #param2 = 20
  # print('circles: ', circles)
    if circles is None:
        return image
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        image1 = cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        print('圓心座標:', i[0], i[1])
        print('圓心半徑:', i[2])
        # draw the center of the circle
        images = cv2.circle(image1, (i[0], i[1]), 2, (0, 0, 255), 3)

    return images



if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    # cap.set(3, 960)
    cap.set(4, 960)

    while(1):
        # get a frame
        ret, frame = cap.read()
        if not ret:
            print('video read error')

        #frame = cv2.addWeighted(frame, 4, cv2.blur(frame, (80, 80)), -4, 128)
        # frame = cv2.Canny(frame,100,250)
        frame = circle(frame)
        # show a frame
        cv2.imshow("capture", frame)
        # print('hi')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('./pictures/circle_detect.png',frame)
            break
    cap.release()
    cv2.destroyAllWindows()