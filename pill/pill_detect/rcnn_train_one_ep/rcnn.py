import os
import random
import numpy as np
import cv2

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import torch
import torchvision
from torchvision import transforms as torchtrans  
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

from engine import train_one_epoch, evaluate
import utils

import xml.etree.ElementTree as ET


#==============check one data======================
# data_dir = os.path.abspath(os.getcwd()) + '/pill/pillsPicture/images/'
# print(data_dir)
# filenames = sorted([name for name in os.listdir(data_dir) if os.path.splitext(name)[-1] == '.jpg' or os.path.splitext(name)[-1] == '.jpeg' or os.path.splitext(name)[-1] == '.png'])
# print(len(filenames))


# img =  cv2.imread(data_dir+filenames[0])
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)


# bbox_dir = os.path.abspath(os.getcwd()) + '/pill/pillsPicture/annotations/'
# bboxes_list = sorted([name for name in os.listdir(bbox_dir) if os.path.splitext(name)[-1] == '.xml'])
# # print(bboxs)
# root = ET.parse(bbox_dir + bboxes_list[0]).getroot()
# print(root)

# bboxes = []
# temp = [0,0,0,0]
# for item in root.iter():

#     # print(item.tag,item.text)
#     if item.tag == 'xmin':
#         temp[0] = int(item.text)
#     elif item.tag == 'ymin':
#         temp[1] = int(item.text)
#     elif item.tag == 'xmax':
#         temp[2] = int(item.text)
#     elif item.tag == 'ymax':
#         temp[3] = int(item.text)
#         bboxes.append(temp.copy())

#==============check one data======================

#------------check bbox-----------
# for bbox in bboxes:
#     print(bbox)
#     cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[2],bbox[3]), (0, 255, 0), 2)

# cv2.imshow('d',img)
# cv2.waitKey(0)
imgs_dir = os.path.abspath(os.getcwd()) + '/pill/pillsPicture/images/'
annotations_dir = os.path.abspath(os.getcwd()) + '/pill/pillsPicture/annotations/'
#----------------pillDataset-----------------------
class PillDataset(torch.utils.data.Dataset):
    def __init__(self, imgs_dir,annotations_dir,height,width,transforms=None):
        self.transforms = transforms
        self.imgs_dir = imgs_dir
        self.annotations_dir = annotations_dir
        self.height = height
        self.width = width

        self.imgs = sorted([name for name in os.listdir(self.imgs_dir) if os.path.splitext(name)[-1] == '.jpg' or os.path.splitext(name)[-1] == '.jpeg' or os.path.splitext(name)[-1] == '.png'])
        self.classes = ['pill']
        self.xmls = sorted([name for name in os.listdir(self.annotations_dir) if os.path.splitext(name)[-1] == '.xml'])


    def __getitem__(self, idx):
        img_name = self.imgs[idx]
        image_path = os.path.join(self.imgs_dir, img_name)
        img = cv2.imread(image_path)
    
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
        img_res = cv2.resize(img_rgb, (self.width, self.height), cv2.INTER_AREA)

        # diving by 255
        img_res /= 255.0
        img_res = np.moveaxis(img_res, -1, 0)


        annotation = self.xmls[idx]
        annotation_path = os.path.join(self.annotations_dir, annotation)

        boxes = []
        labels = []
        tree = ET.parse(annotation_path)
        root = tree.getroot()
        
        wt = img.shape[1] # get img shape
        ht = img.shape[0]

        
        temp = [0,0,0,0]
        for item in root.iter():
            
            # print(item.tag,item.text)
            if item.tag == 'xmin':
                temp[0] = (int(item.text)/wt)*self.width
            elif item.tag == 'ymin':
                temp[1] = (int(item.text)/ht)*self.height
            elif item.tag == 'xmax':
                temp[2] = (int(item.text)/wt)*self.width
            elif item.tag == 'ymax':
                temp[3] = (int(item.text)/ht)*self.height
                boxes.append(temp.copy())
                labels.append(0) # append pill
        
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        iscrowd = torch.zeros((boxes.shape[0],), dtype=torch.int64)
        labels = torch.as_tensor(labels, dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["area"] = area
        target["iscrowd"] = iscrowd
        # image_id
        image_id = torch.tensor([idx])
        target["image_id"] = image_id

        if self.transforms:
            
            sample = self.transforms(image = img_res,
                                    bboxes = target['boxes'],
                                    labels = labels)
            
            img_res = sample['image']
            target['boxes'] = torch.Tensor(sample['bboxes'])
            

        return img_res, target

    def __len__(self):
        return len(self.imgs)


dataset = PillDataset(imgs_dir,annotations_dir,225,225)
print('length of dataset = ', len(dataset), '\n')

# getting the image and target for a test index.  Feel free to change the index.
img, target = dataset[0]
print(type(img),img.shape, '\n',target)


# ------------------show-----------------------
# def plot_img_bbox(img, target):
#     # plot the image and bboxes
#     # Bounding boxes are defined as follows: x-min y-min width height
#     fig, a = plt.subplots(1,1)
#     fig.set_size_inches(5,5)
#     a.imshow(img)
#     for box in (target['boxes']):
#         x, y, width, height  = box[0], box[1], box[2]-box[0], box[3]-box[1]
#         rect = patches.Rectangle((x, y),
#                                  width, height,
#                                  linewidth = 2,
#                                  edgecolor = 'r',
#                                  facecolor = 'none')

#         # Draw the bounding box on top of the image
#         a.add_patch(rect)
#     plt.show()
    
# # plotting the image with bboxes. Feel free to change the index
# img, target = dataset[95]
# plot_img_bbox(img, target)

#-------------------data_loader--------------
train_set, test_set =  torch.utils.data.random_split(dataset,[int(len(dataset)*0.8),len(dataset)-int(len(dataset)*0.8)])
train_dataloader = torch.utils.data.DataLoader(train_set, batch_size=5, num_workers=4, shuffle=True,collate_fn=utils.collate_fn)
test_dataloader = torch.utils.data.DataLoader(test_set, batch_size=5, num_workers=4, shuffle=True,collate_fn=utils.collate_fn)

#------------------model-----------------------
def get_object_detection_model(num_classes):

    # load a model pre-trained pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    
    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes) 

    return model



#------------------training-----------------------
# to train on gpu if selected.
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


num_classes = 1

# get the model using our helper function
model = get_object_detection_model(num_classes)

# move model to the right device
model.to(device)

# construct an optimizer
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.01,
                            momentum=0.9, weight_decay=0.0005)

# and a learning rate scheduler which decreases the learning rate by
# 10x every 3 epochs
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                               step_size=3,
                                               gamma=0.1)

#---------------training for 10 epoches------------
num_epochs = 100

for epoch in range(num_epochs):
    # print(model)
    # training for one epoch
    train_one_epoch(model, optimizer, train_dataloader, device, epoch, print_freq=10)
    # update the learning rate
    lr_scheduler.step()
    # evaluate on the test dataset
    evaluate(model, test_dataloader, device=device)


img, target = dataset[5]
# put the model in evaluation mode
model.eval()
with torch.no_grad():
    prediction = model([torch.from_numpy(img).to(device)])[0]
    
print('predicted #boxes: ', len(prediction['labels']))
print('real #boxes: ', len(target['labels']))



