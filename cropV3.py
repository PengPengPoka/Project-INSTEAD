import numpy as np
import cv2 as cv
from pathlib import Path

def adaptiveCanny(src, sigma=0.33):
    src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    median = np.median(src)
    lower = max(0, (1 - sigma * median))
    upper = min(255, (1 + sigma) * median)
    edge = cv.Canny(src, lower, upper)
    
    return edge

def morphologicalClosing(src, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilation = cv.dilate(src, kernel)
    erosion = cv.erode(dilation, kernel)

    return erosion

# returns circle center coordinate or 0 if no circles detected
# dimension = [x, y, r]
def getCircles(src, param1 = 100, param2 = 50, minRadius = 0, maxRadius = 0):
    center_coor = np.array([])
    circles = cv.HoughCircles(src, cv.HOUGH_GRADIENT, 1, 100,
                              param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            center_coor = np.array([i[0], i[1], i[2]])
            # # draw the outer circle
            # cv.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
            # # draw the center of the circle
            # cv.circle(image,(i[0],i[1]),2,(0,0,255),3)
    
    else:
        center_coor = 0
    
    return center_coor

def main():
    image_path = Path(__file__).absolute().parent / "BOPF_001.jpg"
    image = cv.imread(image_path)
    
    edge_image = adaptiveCanny(image, 0.90)
    closed_edges = morphologicalClosing(edge_image, 11)
    reversed_edge = cv.bitwise_not(closed_edges)
    
    detected_circles = getCircles(closed_edges)
    print(f"circle center: {detected_circles}")
    
    mask = np.zeros(shape=(image.shape[0], image.shape[1]), dtype=np.uint8)
    cv.circle(mask, (detected_circles[0], detected_circles[1]), 100, (255,255,255), cv.FILLED)
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)    

    cropped_image = cv.bitwise_and(image, mask)
    
    cv.imshow("edge", edge_image)
    cv.imshow("closed edges", closed_edges)
    # cv.imshow("reversed edge", reversed_edge)
    cv.imshow("mask", mask)
    cv.imshow("cropped image", cropped_image)
    key = cv.waitKey()
    
    if key == ord('q'):
        exit()
    
if __name__ == "__main__":
    main()