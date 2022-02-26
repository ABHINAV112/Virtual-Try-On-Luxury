import os
import argparse
import logging
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torchvision import transforms
import cv2
import pixellib
from pixellib.torchbackend.instance import instanceSegmentation
from config import HUMAN_PARSING_MODELS_PATH,UPLOAD_PATH

from pipeline.net.pspnet import PSPNet

models = {
    'squeezenet': lambda: PSPNet(sizes=(1, 2, 3, 6), psp_size=512, deep_features_size=256, backend='squeezenet'),
    'densenet': lambda: PSPNet(sizes=(1, 2, 3, 6), psp_size=1024, deep_features_size=512, backend='densenet'),
    'resnet18': lambda: PSPNet(sizes=(1, 2, 3, 6), psp_size=512, deep_features_size=256, backend='resnet18'),
    'resnet34': lambda: PSPNet(sizes=(1, 2, 3, 6), psp_size=512, deep_features_size=256, backend='resnet34'),
    'resnet50': lambda: PSPNet(sizes=(1, 2, 3, 6), psp_size=2048, deep_features_size=1024, backend='resnet50'),
    'resnet101': lambda: PSPNet(sizes=(1, 2, 3, 6), psp_size=2048, deep_features_size=1024, backend='resnet101'),
    'resnet152': lambda: PSPNet(sizes=(1, 2, 3, 6), psp_size=2048, deep_features_size=1024, backend='resnet152')
}

backend = "squeezenet"

# def segmentation(image_path):
#     ins = instanceSegmentation()
#     ins.load_model(SEGMENT_PATH)
#     output_path = f'{UPLOAD_PATH}/image-mask/human.png'
#     ins.segmentImage(image_path, output_image_name=output_path)

#     img = cv2.imread(output_path)
#     rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
#     light_blue = (90, 70, 50)
#     dark_blue = (128, 255, 255)

#     mask = cv2.inRange(hsv_img, light_blue, dark_blue)
#     result = cv2.bitwise_and(img, img, mask=mask)
#     result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
#     for i,val in enumerate(result):
#         for j,val_ in enumerate(val):
#             if result[i][j]!=0:
#                 result[i][j]=255
#     cv2.imwrite(output_path, result)

def build_network(snapshot, backend):
    epoch = 0
    backend = backend.lower()
    net = models[backend]()
    net = nn.DataParallel(net)
    if snapshot is not None:
        _, epoch = os.path.basename(snapshot).split('_')
        if not epoch == 'last':
            epoch = int(epoch)
        net.load_state_dict(torch.load(snapshot, map_location=torch.device('cpu')))
        logging.info("Snapshot for epoch {} loaded from {}".format(epoch, snapshot))
    #net = net.cuda()
    return net, epoch


def get_transform():
    transform_image_list = [
        transforms.Resize((256, 256), 3),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
    return transforms.Compose(transform_image_list)


def show_image(img, pred):

    h, w, _ = pred.shape

    def denormalize(img, mean, std):
        c, _, _ = img.shape
        for idx in range(c):
            img[idx, :, :] = img[idx, :, :] * std[idx] + mean[idx]
        return img

    img = denormalize(img.cpu().numpy(), [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    img = img.transpose(1, 2, 0).reshape((h, w, 3))
    pred = pred.reshape((h, w))

    # pred = cv2.rotate(pred, cv2.cv2.ROTATE_90_CLOCKWISE)
    
    pred = cv2.resize(pred, ((192, 256)))
    cv2.imwrite(f'{UPLOAD_PATH}/image-parse-new/human.png', pred)    
    print(pred.shape)
    
    # # TODO: make better
    # pred_mask = pred*255
    # for i,val in enumerate(pred_mask):
    #     for j,val_j in enumerate(val):
    #         pred_mask[i][j] = 0 if val_j==0 else 255
    # cv2.imwrite(f'{UPLOAD_PATH}/image-mask/human.png', pred_mask)    

def human_parser(image_path):
    snapshot = os.path.join(HUMAN_PARSING_MODELS_PATH, backend, 'PSPNet_last')
    net, starting_epoch = build_network(snapshot, backend)
    net.eval()

    data_transform = get_transform()
    img = Image.open(image_path)
    img = data_transform(img)

    with torch.no_grad():
        pred, _ = net(img.unsqueeze(dim=0))
        pred = pred.squeeze(dim=0)
        pred = pred.cpu().numpy().transpose(1, 2, 0)
        pred = np.asarray(np.argmax(pred, axis=2), dtype=np.uint8).reshape((256, 256, 1))
        show_image(img, pred)

    # segmentation(image_path)
    

