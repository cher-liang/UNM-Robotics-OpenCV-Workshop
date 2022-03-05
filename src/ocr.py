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
from utils.contour_remove import middle_bar_remove,get_text_bars

def ocr(img_path):
    img_name = os.path.split(img_path)[-1]

    img=cv.imread(img_path)

    mask=color_seg(img,img_name)

    cnt=find_cnt(img,mask)
    
    warp=persp_trans(img,cnt)

    threshold=thresh(warp,img_name)

    # mask2=color_seg(warp,img_name)

    middle_bar_remove(threshold)

    result = get_text_bars(threshold)


    custom_config = r'-l eng --psm 6' 
    text = pytesseract.image_to_string(result,config=custom_config)
    text2 = pytesseract.image_to_string(img,config=custom_config)
    
    print(f"With Pre-Processing:\n{text}")
    print(f"Original image:\n{text2}")

    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='OCR')
    parser.add_argument(
        '--image', help='Path to the input image.', default="book.jpg")
    args = parser.parse_args()

    ocr(os.path.join("data/test images/", args.image))