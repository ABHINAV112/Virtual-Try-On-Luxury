import cv2

def generate_clothe_mask(clothe_path):
    img = cv2.imread(clothe_path)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, blackAndWhiteImage = cv2.threshold(grayImage, 128, 255, cv2.THRESH_BINARY)

    blackAndWhiteImage = cv2.bitwise_not(blackAndWhiteImage)
    cv2.imwrite(f"./data/clothe_mask.jpg",blackAndWhiteImage)
