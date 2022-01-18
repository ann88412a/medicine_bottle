import os
from pydoc import text
import numpy as np
import torch
from PIL import Image
from engine import train_one_epoch, evaluate
import utils

import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from torchvision.transforms import ToTensor, ToPILImage

from engine import train_one_epoch, evaluate
import utils
import transforms as T

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
        # img.show()
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
                # temp[0] = (int(item.text)/wt)*self.width
                temp[0] = int(item.text)
            elif item.tag == 'ymin':
                # temp[1] = (int(item.text)/ht)*self.height
                temp[1] = int(item.text)
            elif item.tag == 'xmax':
                # temp[2] = (int(item.text)/wt)*self.width
                temp[2] = int(item.text)
            elif item.tag == 'ymax':
                temp[3] = int(item.text)
                # temp[3] = (int(item.text)/ht)*self.height
                boxes.append(temp.copy())
                labels.append(1) # append pill

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

    # # now get the number of input features for the mask classifier
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

def main():

    # train on the GPU or on the CPU, if a GPU is not available
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    # our dataset has two classes only - background and person
    num_classes = 2
    # use our dataset and defined transformations
    dataset = PillDataset(255,255,get_transform(train=True))
    dataset_test = PillDataset(255,255,get_transform(train=False))

    # split the dataset in train and test set
    indices = torch.randperm(len(dataset)).tolist()
    dataset = torch.utils.data.Subset(dataset, indices[:-50])
    dataset_test = torch.utils.data.Subset(dataset_test, indices[-50:])

    # define training and validation data loaders
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=1, shuffle=True, num_workers=4,
        collate_fn=utils.collate_fn)

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=4,
        collate_fn=utils.collate_fn)
 
    # get the model using our helper function
    model = get_model_instance_segmentation(num_classes)

    # move model to the right device
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005,
                                momentum=0.9, weight_decay=0.0005)
    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=3,
                                                   gamma=0.1)
    # let's train it for 10 epochs
    num_epochs = 10

    for epoch in range(int(num_epochs)):
        # train for one epoch, printing every 10 iterations
        train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=10)
        # update the learning rate
        lr_scheduler.step()

    print("That's it!")
    print("#### Saving the model ####")
    # path = "C:/Users/lucas/OneDrive/Área de Trabalho/TorchVisionObjectDetection/model/trainedModel.pth"
    torch.save(model.state_dict(), "pill_model.pth")
    print("#### Model saved! Now execute tv-evaluation-code.py to run it! ####")

if __name__ == "__main__":
    main()