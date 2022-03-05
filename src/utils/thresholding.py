import cv2 as cv

import json
from logging import error
import sys

def thresh(warp,img_name,show_bool=True):
    with open("config.json","r") as f:
        config = json.load(f)
        try:
            c = config[img_name]["threshold"]
            thresh_method, thresh_val, block_size,C_val = c["method"], c["value"], c["block size"],c["C"]

        except KeyError:
            error(f"{img_name} threshold values does not exists, pls configure in config.json")
            sys.exit()
        except Exception as e:
            error(f"Error, {e}")
            sys.exit()

    # From the warp_original, convert it to grayscale again
    gray = cv.cvtColor(warp, cv.COLOR_BGR2GRAY)
    
    if thresh_method==0:
        # Using Threshold to turn the grayscale image into binary image, either 0 or 255
        _, threshold = cv.threshold(gray,thresh_val, 255, cv.THRESH_BINARY_INV)
    elif thresh_method==1:
        threshold= cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY_INV,block_size,C_val)
    elif thresh_method == 2:
        threshold= cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY_INV,block_size,C_val)

    if show_bool:
        cv.imshow("warp gray", gray)
        cv.imshow("threshold", threshold)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return threshold