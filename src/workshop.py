from utils.show_bgr_hsv import show_bgr_hsv
from utils.color_trackbar import color_trackbar
from demo.face_detection import face_detection

import os
import argparse

import cv2 as cv

def main(args):

    img_path=os.path.join("data/test images/", args.image)
    
    if args.module[0]=="all":
        pass
    elif args.module[0]=="hsv":
        show_bgr_hsv(img_path)
    elif args.module[0]=="trackbar":
        color_trackbar(img_path)
    elif args.module[0]=="face_detection":
        face_detection()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='UNM Robotics OpenCV Workshop')
    parser.add_argument("-m","--module",dest="module",nargs=1,choices=["hsv","trackbar","face_detection","all"],default=["all"])
    parser.add_argument(
        '--image', help='Path to the input image.', default="book.jpg")
    args = parser.parse_args()

    main(args)



