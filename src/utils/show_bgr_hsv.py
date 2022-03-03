"""
    Explanation:
    
    When left click of the mouse is pressed, RGB value of the pixel will be shown
    in the output.
    When right click of the mouse is pressed, HSV value of the pixel will be shown
    in the output.
"""

import cv2 as cv
import argparse
import os

from cv2 import EVENT_LBUTTONDOWN, EVENT_RBUTTONDOWN

def getPixelValue(event, x, y, flags, param):
    if event == EVENT_LBUTTONDOWN :  # checks whether left click is pressed

        # Get the value of the pixel for that coordinate from the RGB image
        colorsBGR = param[y, x]
        
        #Reversing the OpenCV BGR format to RGB format
        colorsRGB = tuple(reversed(colorsBGR))
        
        print(f"RGB Value at ({x},{y}): R:{colorsRGB[0]}, G:{colorsRGB[1]}, B:{colorsRGB[2]}\n")

    elif event == EVENT_RBUTTONDOWN :  # checks whether right click is pressed
        # Get the value of the pixel for that coordinate from the HSV image
        colorsHSV = param[y, x]
        print(f"HSV Value at ({x},{y}): H:{colorsHSV[0]}, S:{colorsHSV[1]}, V:{colorsHSV[2]}\n")


def show_bgr_hsv(img_path):
    # Read the RGB image and convert it to HSV colour space
    rgb = cv.imread(img_path)
    hsv = cv.cvtColor(rgb,cv.COLOR_BGR2HSV)

    # Create a window and set Mousecallback to a function for that window
    cv.namedWindow('RGB')  
    cv.setMouseCallback('RGB', getPixelValue,rgb)

    # Create another window and set Mousecallback to a function for that window
    cv.namedWindow('HSV')
    cv.setMouseCallback('HSV', getPixelValue,hsv)

    # Execute until esc is pressed
    while (1):
        cv.imshow('RGB', rgb)
        cv.imshow('HSV', hsv)

        #When ESC is pressed, the program will terminate
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
        
    # if esc is pressed, close all windows.
    cv.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Show RGB or HSV value of Where You Click')
    parser.add_argument(
        '--image', help='Path to the input image.', default="Rubiks.jpg")
    args = parser.parse_args()

    show_bgr_hsv(os.path.join("data/test images/", args.image))