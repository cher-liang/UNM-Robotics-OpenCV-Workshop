import cv2 as cv
import numpy as np


def middle_bar_remove(image,show_bool=True):

    cnts,_ = cv.findContours(image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # filter using aspect ratio (as texts are horizontal rectangular in shape)
    for c in cnts:
        x, y, w, h = cv.boundingRect(c)
        ar = w / float(h)

        if ar > 4:
            # Fill the middle long bar with black colour to "remove" it
            cv.drawContours(image, contours=[c], contourIdx=-1, color=(0, 0, 0), thickness=-1)
            
            break
    if show_bool:
        cv.imshow("threshold (with bar removed)", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

def get_text_bars(threshold):
    # Create horizontal kernel and dilate to connect text characters
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 3))
    dilate = cv.dilate(threshold, kernel, iterations=4)

    cnts,_ = cv.findContours(dilate, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    
    height = dilate.shape[0]
    width = dilate.shape[1]

    # Create a black image with the same height and width of the image
    black_mask = np.zeros((height, width, 1), dtype="uint8")

    # filter using aspect ratio (as texts are horizontal rectangular in shape)
    for c in cnts:
        x, y, w, h = cv.boundingRect(c)
        ar = w / float(h)

        if ar > 5:
            # Draw the text contours onto the black mask created
            cv.drawContours(image=black_mask, contours=[c], contourIdx=-1, color=(255, 255, 255), thickness=-1)
            
    result = cv.bitwise_not(cv.bitwise_and(black_mask, threshold))
    
    cv.imshow("Dilated image",dilate)
    cv.imshow("Black Mask",black_mask)
    cv.imshow("Threshold",threshold)
    cv.imshow("Bitwise NOT(AND)",result)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return result