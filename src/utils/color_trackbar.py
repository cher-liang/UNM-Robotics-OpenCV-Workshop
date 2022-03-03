import cv2 as cv

import argparse
import os
import json

from cv2 import WINDOW_AUTOSIZE

slider_max = 255
title_window = "Threshold Values"


class Trackbar:
    def __init__(self, img) -> None:
        self.img = img

        self.H_l, self.S_l, self.V_l = 0, 0, 0
        self.H_h, self.S_h, self.V_h = 255, 255, 255

    def in_range(self):
        self.color_low = (self.H_l, self.S_l, self.V_l)
        self.color_high = (self.H_h, self.S_h, self.V_h)

        # Apply the value obtained from trackbar and apply to the thresholding
        mask = cv.inRange(self.img, self.color_low, self.color_high)

        cv.imshow('Mask', mask)

    def H_l_change(self, val: int):
        self.H_l = val
        self.in_range()

    def S_l_change(self, val: int):
        self.S_l = val
        self.in_range()

    def V_l_change(self, val: int):
        self.V_l = val
        self.in_range()

    def H_h_change(self, val: int):
        self.H_h = val
        self.in_range()

    def S_h_change(self, val: int):
        self.S_h = val
        self.in_range()

    def V_h_change(self, val: int):
        self.V_h = val
        self.in_range()


def save_values(color_low, color_high):
    with open("config.json","r") as f:
        config=json.load(f)
    config["color"]["low"]={"H": color_low[0], "S": color_low[1], "V": color_low[2]}
    config["color"]["high"]={"H": color_high[0], "S": color_high[1], "V": color_high[2]}
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def color_trackbar(img_path):
    img = cv.imread(img_path)
    cv.imshow('Figure', img)
    t = Trackbar(img)

    # Create a window for the trackbars
    cv.namedWindow(title_window, WINDOW_AUTOSIZE)
    cv.resizeWindow(title_window, 600, 400)

    cv.createTrackbar('H_l', title_window, 0, slider_max, t.H_l_change)
    cv.createTrackbar('S_l', title_window, 0, slider_max, t.S_l_change)
    cv.createTrackbar('V_l', title_window, 0, slider_max, t.V_l_change)
    cv.createTrackbar('H_h', title_window, slider_max,
                      slider_max, t.H_h_change)
    cv.createTrackbar('S_h', title_window, slider_max,
                      slider_max, t.S_h_change)
    cv.createTrackbar('V_h', title_window, slider_max,
                      slider_max, t.V_h_change)

    while True:
        k = cv.waitKey(0)

        if k == ord('s'):
            save_values(t.color_low, t.color_high)
        elif k==27:
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Code for Adjusting Color Threshold using cv.trackbar and cv.inRange')
    parser.add_argument(
        '--input1', help='Path to the first input image.', default='book.jpg')
    args = parser.parse_args()

    color_trackbar(os.path.join("data/test images/", args.input1))
