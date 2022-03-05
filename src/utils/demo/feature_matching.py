from re import template
import cv2 as cv

import argparse
import os

def feature_matching(src_path='data/test images/facemask_edited.jpg',template_path='data/test images/facemask.jpg'):
    src_img=cv.imread(src_path)
    template_img=cv.imread(template_path)

    gray=cv.cvtColor(src_img,cv.COLOR_BGR2GRAY)

    orb = cv.ORB_create(nfeatures=15000,WTA_K=4) #create ORB detector object

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True) #create Brute-force (BF) Matcher object

    kp1, des1 = orb.detectAndCompute(template_img, None) #find the keypoints and descriptors with ORB
    kp2, des2 = orb.detectAndCompute(gray, None) 

    if len(kp1) != 0 and len(kp2) != 0:
        match = bf.match(des1, des2) # match the points using Brute Force
        match = sorted(match, key=lambda x: x.distance) # sort the matches by its "distance"
        ans=cv.drawMatches(template_img,kp1,src_img,kp2,match[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    cv.imshow("answer",ans)
    k = cv.waitKey(0) & 0xFF
    if k == 27:
        # if esc is pressed, close all windows.
        cv.destroyAllWindows()
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Feature Matching Demonstration')
    parser.add_argument(
        '--src', help='Path to the source image.', default="facemask_edited.jpg")
    parser.add_argument(
        '--template',help='Path to the template image.',default="facemask.jpg")
    args = parser.parse_args()

    feature_matching(src_path=os.path.join("data/test images/", args.src),template_path=os.path.join("data/test images/", args.template))