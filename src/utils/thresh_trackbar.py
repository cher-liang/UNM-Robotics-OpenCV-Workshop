import cv2 as cv
from cv2 import WINDOW_AUTOSIZE

import argparse
import os
import json
from logging import error
import sys

slider_max = 255
title_window = "Threshold Method"


class Thresh_Trackbar:
    def __init__(self, img_path,warp) -> None:
        self.img_name = os.path.split(img_path)[-1]

        self.img = warp
        self.gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        cv.imshow('Figure', self.img)
        cv.imshow('Gray',self.gray)

        self.__thresh_method = 0 # 0 - Global Threshold, 1 - Adaptive Mean Threshold, 2 - Adaptive Gaussian Threshold
        self.__thresh_val = 127 # only for global threshold
        self.__block_size = 11
        self.__C_val = 2 #constant that is subtracted from the mean or weighted sum of the neighbourhood pixels.

    def GUI(self):
        cv.namedWindow(title_window,WINDOW_AUTOSIZE)
        cv.resizeWindow(title_window, 600, 400)

        cv.createTrackbar("Threshold method",title_window,self.__thresh_method,2,self.__method_change)
        cv.createTrackbar("Threshold value",title_window,self.__thresh_val,255,self.__val_change)
        cv.createTrackbar("Block size (Odd number)",title_window,self.__block_size,55,self.__block_change)
        cv.createTrackbar("C",title_window,self.__C_val,55,self.__C_change)

    def thresholding(self):
        if self.__thresh_method==0:
            # Using Threshold to turn the grayscale image into binary image, either 0 or 255
            _, threshold = cv.threshold(self.gray, self.__thresh_val, 255, cv.THRESH_BINARY_INV)
        elif self.__thresh_method==1:
            threshold= cv.adaptiveThreshold(self.gray,255,cv.ADAPTIVE_THRESH_MEAN_C,\
                cv.THRESH_BINARY_INV,self.__block_size,self.__C_val)
        elif self.__thresh_method == 2:
            threshold= cv.adaptiveThreshold(self.gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv.THRESH_BINARY_INV,self.__block_size,self.__C_val)
        
        cv.imshow("Threshold",threshold)

    def __method_change(self,val:int):
        self.__thresh_method=val
    
    def __val_change(self, val:int):
        self.__thresh_val=val
        self.thresholding()
    
    def __block_change(self,val:int):
        self.__block_size=val
        self.thresholding()
    
    def __C_change(self,val:int):
        self.__C_val=val
        self.thresholding()
    

    def load_values(self) -> bool:
        with open("config.json", "r") as f:
            config = json.load(f)

        if self.img_name in config and "method" in config[self.img_name]["threshold"]:
            c = config[self.img_name]["threshold"]
            self.__thresh_method, self.__thresh_val, self.__block_size,self.__C_val = c["method"], c["value"], c["block size"],c["C"]

            return True
        else:
            return False

    def save_values(self):

        with open("config.json", "r") as f:
            config = json.load(f)

        config[self.img_name] = {
            "color":config[self.img_name]["color"],
            "threshold":
            {
                "method":self.__thresh_method,"value":self.__thresh_val,"block size":self.__block_size,"C":self.__C_val
            }
        }
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)


def thresh_trackbar(img_path):
    img_name = os.path.split(img_path)[-1]
    img=cv.imread(img_path)

    mask=color_seg(img,img_name,show_bool=False)

    cnt=find_cnt(img,mask,show_bool=False)
    
    warp=persp_trans(img,cnt,show_bool=False)

    t = Thresh_Trackbar(img_path,warp)

    t.load_values()
    t.GUI()

    while True:
        k = cv.waitKey(0)

        if k == ord('s'):
            t.save_values()
        elif k == 27:
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Code for Adjusting Threshold using cv.trackbar')
    parser.add_argument(
        '--image', help='Path to the input image.', default='book.jpg')
    args = parser.parse_args()
    
    from color_segmentation import color_seg
    from find_contours import find_cnt
    from perspective_transform import persp_trans

    thresh_trackbar(os.path.join("data/test images/", args.image))
else:
    from utils.color_segmentation import color_seg
    from utils.find_contours import find_cnt
    from utils.perspective_transform import persp_trans
