import numpy as np
import cv2

pills = {'Sennoside':[121,209,255],'Apresoline':[0,0,0]}

img = cv2.imread('/home/medical/medicine_bottle/pictures/test.png')
print(len(img),len(img[0]))
correct_bgr_location = [(399,369),(370,295),(341,399)]
bgr_color = [img[correct_bgr_location[0]],img[correct_bgr_location[1]],img[correct_bgr_location[2]]]
print(img[correct_bgr_location[0]],img[correct_bgr_location[1]],img[correct_bgr_location[2]])

# img[250:450] = img[151,393]
# img[50:100] =  img[correct_bgr_location[1]]
# img[100:150] =  img[correct_bgr_location[2]]
print(bgr_color)
d_arr = img[:250]


def circle(image):


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5),0)

    cannied = cv2.Canny(np.asarray(blurred), 150, 200)
    cv2.imshow("can", cannied)

    circles = cv2.HoughCircles(cannied, cv2.HOUGH_GRADIENT, 1, 100,
                                param1=100, param2=20, minRadius=10, maxRadius=60)
 
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

    return images,circles[0,:]

def mse(arr1,arr2):
    temp = arr1.copy()
    temp = temp.tolist()
    
    for i,item in enumerate(arr2):
        temp[i] = (temp[i]-item)**2
        
    return sum(temp)

def detect_pill(img_t,pos0,pos1):
    # print(img_t[pos1,pos0],pills['Sennoside'])
    print( mse(img_t[pos1,pos0],pills['Sennoside']))
    if mse(img_t[pos1,pos0],pills['Sennoside']) < 2500:
        d_circle = cv2.putText(img_t, "Sennoside", (pos0,pos1), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))

print(len(d_arr),len(d_arr[0]))
d_circle,d_pos =circle(d_arr)
print(d_pos[0][0],d_pos[0][1])
# img[50:100] = d_circle[int(d_pos[0][1])+int(d_pos[0][2]/2),int(d_pos[0][0])+int(d_pos[0][2]/2)]
print(d_circle[int(d_pos[0][1])+int(d_pos[0][2]/2),int(d_pos[0][0])+int(d_pos[0][2]/2)])
# print(int(d_pos[0][1])+int(d_pos[0][2]/2),int(d_pos[0][0])+int(d_pos[0][2]/2))

detect_pill(d_circle,int(d_pos[0][0])+int(d_pos[0][2]/2),int(d_pos[0][1])+int(d_pos[0][2]/2))

# print(int(d_pos[0][1])+int(d_pos[0][2]/2),int(d_pos[0][0])+int(d_pos[0][2]/2))
# d_circle = cv2.circle(d_circle, (5,5), 2, (0, 0, 255), 3)

cv2.imshow("a",d_circle)

cv2.waitKey(0)




# while(True):
    
#     print(len(d_arr),len(d_arr[0]))
#     d_circle =circle(d_arr)
    
#     # cv2.imshow("a",d_circle)
    

#     if cv2.waitKey(1) & 0xFF == ord('q'):
        
#         cv2.imwrite('./pictures/color_correct.png',img)
#         break


# cv2.destroyAllWindows()



