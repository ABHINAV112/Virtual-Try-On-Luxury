import cv2
import os
from config import UPLOAD_PATH

def generate_clothe_mask(clothe_path):
    img = cv2.imread(clothe_path)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, blackAndWhiteImage = cv2.threshold(grayImage, 128, 255, cv2.THRESH_BINARY)

    blackAndWhiteImage = cv2.bitwise_not(blackAndWhiteImage)
    blackAndWhiteImage = cv2.resize(blackAndWhiteImage, ((192, 256)))

    cv2.imwrite(f"{UPLOAD_PATH}/cloth-mask/cloth.jpg",blackAndWhiteImage)
