import cv2
import numpy as np

def circle(image):

  img = cv2.medianBlur(image, 5)
  cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  print('the shape of cimg: ', cimg.shape)
  # circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,
  #                             param1=100,param2=30,minRadius=40, maxRadius=70)
  circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 100,
                              param1=100, param2=20, minRadius=20, maxRadius=60)

  # print('circles: ', circles)
  if circles is None:
      return image
  circles = np.uint16(np.around(circles))
  for i in circles[0,:]:
      # draw the outer circle
      image1 = cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
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

      frame = cv2.addWeighted(frame, 4, cv2.blur(frame, (80, 80)), -4, 128)
      # frame = cv2.Canny(frame,100,250)
      frame = circle(frame)
      # show a frame
      cv2.imshow("capture", frame)
      print('hi')

      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  cap.release()
  cv2.destroyAllWindows()