import cv2

# 假设图像为test.jpg
img = cv2.imread(r'C:\Users\AnnA\Desktop\medicTalk_new\medicine_bottle\pill\onnx\07_01_00_44_30_454.jpg')
h, w, _ = img.shape


# yolo标注数据文件名为786_rgb_0616.txt
with open(r'C:\Users\AnnA\Desktop\medicTalk_new\medicine_bottle\pill\onnx\07_01_00_44_30_454.txt', 'r') as f:
	temp = f.read()
	temp = temp.split()
	# ['1', '0.43906', '0.52083', '0.34687', '0.15']

# 根据第1部分公式进行转换
x_, y_, w_, h_ = eval(temp[1]), eval(temp[2]), eval(temp[3]), eval(temp[4])

x1 = w * x_ - 0.5 * w * w_
x2 = w * x_ + 0.5 * w * w_
y1 = h * y_ - 0.5 * h * h_
y2 = h * y_ + 0.5* h * h_

# 画图验证，注意画图坐标要转换成int格式
cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0))

cv2.imshow('windows', img)
cv2.waitKey(0)
