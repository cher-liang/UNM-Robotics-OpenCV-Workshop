import cv2 as cv
import numpy as np


def persp_trans(img,cnt,show_bool=True):
    # Get the 4 vertices of the book
    epsilon = 0.1*cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, epsilon, True)

    # Perspective transform (look at 4 point perspective transform)
    # now that we have our book contour, we need to determine
    # the top-left, top-right, bottom-right, and bottom-left points
    # so that we can later warp the image -- we'll start
    # by reshaping our contour and initializing
    # our output rectangle vertice points in top-left, top-right, bottom-right,
    # and bottom-left order
    pts = approx.reshape(4, 2)# reshape to 4 rows, 2 columns; where each row corresponding to (x, y) coordinates of a point

    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis=1)

    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # compute the difference between the points -- the top-right
    # will have the minimum difference and the bottom-left will
    # have the maximum difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # now that we have our rectangle of points, let's compute
    # the width of our new image
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # ...and now for the height of our new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # take the maximum of the width and height values to get
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    # construct our destination points which will be used to
    # map the book to a top-down, "birds eye" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    M = cv.getPerspectiveTransform(rect, dst)
    warp = cv.warpPerspective(img, M,(maxWidth, maxHeight))

    if show_bool:
        cv.imshow("warp original", warp)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return warp

    