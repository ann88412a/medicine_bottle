import cv2
import matplotlib.pyplot as plt
import os
files = os.listdir('/home/fritingo/Documents/教案四')
print(files)

for file in files:
    f = file.split('.')

    if len(f) > 1 and f[1] == 'png':
        print(f[0])

        img = cv2.imread('/home/fritingo/Documents/教案四/'+f[0]+'.png')
        dh, dw, _ = img.shape

        fl = open('/home/fritingo/Documents/教案四/'+f[0]+'.txt', 'r')
        data = fl.readlines()
        fl.close()

        # img = cv2.imread('/home/fritingo/Documents/教案四/07_14_04_04.png')
        # dh, dw, _ = img.shape

        # fl = open('/home/fritingo/Documents/教案四/07_14_04_04.txt', 'r')
        # data = fl.readlines()
        # fl.close()

        for dt in data:

            # Split string to float
            _, x, y, w, h = map(float, dt.split(' '))

            # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
            # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
            l = int((x - w / 2) * dw)
            r = int((x + w / 2) * dw)
            t = int((y - h / 2) * dh)
            b = int((y + h / 2) * dh)
            
            if l < 0:
                l = 0
            if r > dw - 1:
                r = dw - 1
            if t < 0:
                t = 0
            if b > dh - 1:
                b = dh - 1

            cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(im_rgb)
        # plt.show()
        plt.savefig('/home/fritingo/Documents/教案四/check/'+f[0]+'.png')