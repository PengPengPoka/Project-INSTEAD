import cv2 as cv
import numpy as np
import os
import math
from matplotlib import pyplot as plt

def on_trackbar():
    # print(f"Trackbar value: {value}")
    pass

def getHist(image):
    non_black_mask = np.any(image != [0, 0, 0], axis=2).astype(np.uint8)

    color = ['b','g','r']
    for channel, col in enumerate(color):
        histogram = cv.calcHist([image], [channel], mask=non_black_mask, histSize=[256], ranges=[0,256])
        plt.plot(histogram, color=col)
        plt.xlim(0,256)

    plt.xlabel("RGB values")
    plt.ylabel("Pixel Frequency")
    plt.title("RGB values")
    plt.show()

def crop_trackbar(height, width, px, py, radius, src):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    img = src.copy()

    cv.circle(canvas, (px,py), radius, [255,255,255], cv.FILLED)

    cropped = cv.bitwise_and(img, canvas,mask=None)

    # cv.imshow("canvas", canvas)
    # cv.imshow("crop", cropped)
    return cropped

def crop_mouse(event, x, y, img):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Left mouse button clicked at ({x}, {y})")
        cx, cy = x, y
    elif event == cv.EVENT_RBUTTONDOWN:
        print(f"Right mouse button clicked at ({x}, {y})")
        px, py = x, y

    canvas = np.zeros((img[0], img[1], img[2]), dtype=np.uint8)
    radius = math.sqrt((px - cx)^2 + (py - cy)^2)
    cv.circle()

def main():
    home = os.path.expanduser("~")
    img_path = home + "\\Repositories 2\\Project-INSTEAD\\Data_21-09-2023[1]\\Warna\\DUST_1-1.jpg"
    img = cv.imread(img_path)

    height = img.shape[0]
    width = img.shape[1]
    channel = img.shape[2]

    cv.namedWindow("crop trackbar")
    cv.createTrackbar("x space", "crop trackbar", 0, width-1, on_trackbar)
    cv.createTrackbar("y space", "crop trackbar", 0, height-1, on_trackbar)
    cv.createTrackbar("radius", "crop trackbar", 0, 450, on_trackbar)

    cv.setTrackbarPos("x space", "crop trackbar", 324)
    cv.setTrackbarPos("y space", "crop trackbar", 238)
    cv.setTrackbarPos("radius", "crop trackbar", 100)
    
    while True:
        x = cv.getTrackbarPos("x space", "crop trackbar")
        y = cv.getTrackbarPos("y space", "crop trackbar")
        radius = cv.getTrackbarPos("radius", "crop trackbar")

        img_copy = img.copy()
        cv.circle(img_copy, (x,y), radius, [0,0,255], 2)
        
        crop_img = crop_trackbar(height, width, x, y, radius, img)


        cv.imshow("crop trackbar", img_copy)
        cv.imshow("crop",crop_img)
        key = cv.waitKey(3)

        if key == 27:
            break
        elif key == ord('c'):
            getHist(crop_img)

    


if __name__ == "__main__":
    main()
    cv.destroyAllWindows()