import cv2 as cv
from cv2 import perspectiveTransform
import numpy as np
import pytesseract

import argparse
import os
from logging import error

from utils.color_segmentation import color_seg
from utils.find_contours import find_cnt
from utils.perspective_transform import persp_trans
from utils.thresholding import thresh

def ocr(img_path):
    img_name = os.path.split(img_path)[-1]

    img=cv.imread(img_path)

    mask=color_seg(img,img_name)

    cnt=find_cnt(img,mask)
    
    warp=persp_trans(img,cnt)

    threshold=thresh(warp,img_name)

    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='OCR')
    parser.add_argument(
        '--image', help='Path to the input image.', default="book.jpg")
    args = parser.parse_args()

    ocr(os.path.join("data/test images/", args.image))