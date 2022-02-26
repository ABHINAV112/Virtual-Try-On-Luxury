"""
Make updated body shape from updated segmentation
"""
from config import UPLOAD_PATH


import os
import numpy as np
import cv2
from PIL import Image
import sys


(cv_major, _, _) = cv2.__version__.split(".")
if cv_major != '4' and cv_major != '3':
    print('doesnot support opencv version')
    sys.exit()


# @TODO this is too simple and pixel based algorithm
def body_detection(image, seg_mask):
    # binary thresholding by blue ?
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 0, 120])
    upper_blue = np.array([180, 38, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(image, image, mask=mask)

    # binary threshold by green ?
    b, g, r = cv2.split(result)
    filter = g.copy()
    ret, mask = cv2.threshold(filter, 10, 255, 1)

    # at least original segmentation is FG
    mask[seg_mask] = 1

    return mask


def make_body_mask():
    img_path = f"{UPLOAD_PATH}/image/human.jpg"
    seg_path = f"{UPLOAD_PATH}/image-parse-new/human.png"
    img = cv2.imread(img_path)
    gray = cv2.imread(seg_path, cv2.IMREAD_GRAYSCALE)
    _, seg_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    body_mask = body_detection(img, seg_mask)
    body_mask = body_mask + seg_mask
    body_mask[seg_mask] = 1
    cv2.imwrite(f"{UPLOAD_PATH}/image-mask/human.png", body_mask)



if __name__ == '__main__':
    make_body_mask()