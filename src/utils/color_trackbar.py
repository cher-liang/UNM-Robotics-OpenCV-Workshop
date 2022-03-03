import cv2 as cv
import argparse

import os

from cv2 import WINDOW_AUTOSIZE

slider_max=255
title_window="Threshold Values"

class Trackbar:
    def __init__(self,img) -> None:
        self.img=img

        self.H_l, self.S_l, self.V_l =0,0,0
        self.H_h, self.S_h, self.V_h =255,255,255

    def in_range(self):
        color_low = (self.H_l, self.S_l, self.V_l)
        color_high = (self.H_h, self.S_h, self.V_h)

        #Apply the value obtained from trackbar and apply to the thresholding
        mask =cv.inRange(self.img, color_low,color_high)

        cv.imshow('Mask', mask)

    def H_l_change(self,val:int):
        self.H_l=val
        self.in_range()
    
    def S_l_change(self,val:int):
        self.S_l=val
        self.in_range()
   
    def V_l_change(self,val:int):
        self.V_l=val
        self.in_range()
    
    def H_h_change(self,val:int):
        self.H_h=val
        self.in_range()
    
    def S_h_change(self,val:int):
        self.S_h=val
        self.in_range()
    
    def V_h_change(self,val:int):
        self.V_h=val
        self.in_range()
    

def color_trackbar(img_path):  
    img = cv.imread(img_path)
    cv.imshow('Figure', img)
    t=Trackbar(img)

    #Create a window for the trackbars
    cv.namedWindow(title_window,WINDOW_AUTOSIZE)
    cv.resizeWindow(title_window,600,400)

    cv.createTrackbar('H_l',title_window,0,slider_max,t.H_l_change)
    cv.createTrackbar('S_l',title_window,0,slider_max,t.S_l_change)
    cv.createTrackbar('V_l',title_window,0,slider_max,t.V_l_change)
    cv.createTrackbar('H_h',title_window,slider_max,slider_max,t.H_h_change)
    cv.createTrackbar('S_h',title_window,slider_max,slider_max,t.S_h_change)
    cv.createTrackbar('V_h',title_window,slider_max,slider_max,t.V_h_change)

    cv.waitKey()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Code for Adjusting Color Threshold using cv.trackbar and cv.inRange')
    parser.add_argument('--input1', help='Path to the first input image.', default='book.jpg')
    args=parser.parse_args()

    color_trackbar(os.path.join("data/test images/",args.input1))
