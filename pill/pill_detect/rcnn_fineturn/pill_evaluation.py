from operator import mod
import os
import numpy as np
import torch
from PIL import Image

import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from torchvision.transforms import ToTensor, ToPILImage

from engine import train_one_epoch, evaluate
import utils
import transforms as T

import cv2
import xml.etree.ElementTree as ET

data_dir = os.path.abspath(os.getcwd()) + '/pill/pillsPicture/images/'
xml_dir = os.path.abspath(os.getcwd()) + '/pill/pillsPicture/annotations/'



# ------------------dataset------------------
class PillDataset(object):
    def __init__(self, height,width,transforms):
        self.transforms = transforms
        # load all image files, sorting them to ensure that they are aligned
        self.imgs = list(sorted(os.listdir(data_dir)))
        self.masks = list(sorted(os.listdir(xml_dir)))
        self.height = height
        self.width = width

    def __getitem__(self, idx):
        # load images and bbox
        img_path = os.path.join(data_dir, self.imgs[idx])
        img = Image.open(img_path).convert("RGB")
        # print('get',np.array(img).shape)
        
        box_path = os.path.join(xml_dir, self.masks[idx])

        boxes = []
        labels = []
        tree = ET.parse(box_path)
        root = tree.getroot()

        wt = np.array(img).shape[1] # get img shape
        ht = np.array(img).shape[0]

        temp = [0,0,0,0]
        for item in root.iter():
            
            # print(item.tag,item.text)
            if item.tag == 'xmin':
                temp[0] = (int(item.text)/wt)*self.width
                # temp[0] = int(item.text)
            elif item.tag == 'ymin':
                temp[1] = (int(item.text)/ht)*self.height
                # temp[1] = int(item.text)
            elif item.tag == 'xmax':
                temp[2] = (int(item.text)/wt)*self.width
                # temp[2] = int(item.text)
            elif item.tag == 'ymax':
                # temp[3] = int(item.text)
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
        image_id = torch.tensor([idx])
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd
        # print(target)

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)



def get_model_instance_segmentation(num_classes):
    # load an instance segmentation model pre-trained pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # now get the number of input features for the mask classifier
    # in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    # hidden_layer = 256
    # # and replace the mask predictor with a new one
    # model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
    #                                                    hidden_layer,
    #                                                    num_classes)

    return model


def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)


def convert_tensor_to_RGB(network_output):
   
    converted_tensor = torch.squeeze(network_output)

    return converted_tensor

def main():
    
    # use our dataset and defined transformations
    dataset = PillDataset(255,255,get_transform(train=True))
    dataset_test = PillDataset(255,255,get_transform(train=False))

    # split the dataset in train and test set
    indices = torch.randperm(len(dataset)).tolist()
    dataset = torch.utils.data.Subset(dataset, indices[:-50])
    dataset_test = torch.utils.data.Subset(dataset_test, indices[-50:])

    # define data loader
    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=True, num_workers=4,
        collate_fn=utils.collate_fn)

    #This is the same path you stored your model
    path = os.path.abspath(os.getcwd()) + '/pill_model.pth'
    class_num = 2
    model = get_model_instance_segmentation(class_num)
    print(model)
    model.load_state_dict(torch.load(path))
    model.eval()

    print("###### Running the model ######")
    model.eval()
    model.cuda()
    image = next(iter(data_loader_test))

    #Here we create a list, because the model expects a list of Tensors
    lista = []
    #It is important to send the image to CUDA, otherwise it will try to execute in the CPU
    x = image[0][0].cuda()
    
    img = np.array(image[0][0])
    img = np.moveaxis(img,0,-1)
    # cv2.imshow('t',img)
    # cv2.waitKey(0)
    print('shape',img.shape)
    
    lista.append(x)
    print('x',x)
    
    output = model(lista)
    print('target',output )
    print(output[0]['boxes'])
    bboxes = output[0]['boxes']
    print(bboxes,bboxes[0],int(bboxes[0][0]))
    for bbox in bboxes:
        print(bbox)
        cv2.rectangle(img,(int(bbox[0]),int(bbox[1])),(int(bbox[2]),int(bbox[3])), (0, 255, 0), 2)
    print(img.shape,type(img))

    # output = convert_tensor_to_RGB(output[0])

    #Here, we pass the output to CPU in order to properly save the image
    # output_cpu = output.cpu()

    #Just a number to order your images
    number = 2

    #Saving the images
    # ToPILImage()(output_cpu).save('images/test_'+str(number)+'.png', mode='png')
    print("#### All Done! :) ####")
    cv2.imshow('t',img)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()