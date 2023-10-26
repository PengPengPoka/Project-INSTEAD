import cv2 as cv
import numpy as np
import os
import time

def main():
    home = os.path.expanduser("~")
    # img_path = home + "\\OneDrive\\Pictures\\INSTEAD Teh\\DUST_2-1.jpg"
    img_path = home + "\\Documents\\INSTEAD_DATA_21-9-2023\\Warna\\DUST_2-1.jpg"

    img = cv.imread(img_path)

    height = img.shape[0]
    width = img.shape[1]

    t1 = time.time()

    for y in range(height):
        for x in range(width):
            pixel = img[y,x]

            print(" pixel [{}] at {}, {}".format(pixel, x, y))

    t2 = time.time()

    Time = t2-t1
    print("Pixel iteration: {}".format(Time))

    cv.imshow("teh", img)
    key = cv.waitKey()

    if key == 27:
        exit()
    


if __name__ == "__main__":
    main()