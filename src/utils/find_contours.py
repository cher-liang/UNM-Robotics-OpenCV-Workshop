import cv2 as cv

def find_cnt(img,mask,show_bool=True):
    ROI=img.copy()
    contours,_=cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnt=max(contours,key=cv.contourArea)
    cv.drawContours(ROI,[cnt],-1,(0,0,255),5)

    if show_bool:
        cv.imshow("ROI",ROI)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return cnt