import cv2 as cv

import json
from logging import error
import sys

def color_seg(img,img_name,show_bool=True):
    with open("config.json","r") as f:
        try:
            c=json.load(f)[img_name]["color"]
            color_low = (c["low"]["H"], c["low"]["S"], c["low"]["V"])
            color_high = (c["high"]["H"], c["high"]["S"], c["high"]["V"])

        except KeyError:
            error(f"{img_name} HSV values does not exists, pls configure in config.json")
            sys.exit()
        except Exception as e:
            error(f"Error, {e}")
            sys.exit()

    mask=cv.inRange(img,color_low,color_high)

    if show_bool:
        cv.imshow("RGB",img)
        cv.imshow("Mask",mask)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return mask