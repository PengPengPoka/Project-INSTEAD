import cv2 as cv
import numpy as np
import os
import math
from matplotlib import pyplot as plt
import pandas as pd

i = 1
j = 1
variants = ("DUST", "DUST2", "DUST3", "BOHEA", "BOP", "BOPF", "BOPF1", "F1", "F2", "PF", "PF2", "PF3", "BP")
sample = str(variants[1]) + "_" + str(i) + "_" + str(j)

def save_mask(mask):
    cv.imwrite(sample + "_mask.jpg" , img=mask)

def on_trackbar(value):
    pass

def getHist(image, filename, save_to_excel=False):
    non_black_mask = np.any(image != [0, 0, 0], axis=2).astype(np.uint8)

    color = ['b', 'g', 'r']
    plt.figure(figsize=(10, 5))
    plt.title(filename)

    df = pd.DataFrame()

    for channel, col in enumerate(color):
        plt.subplot(1, 3, channel + 1)
        histogram = cv.calcHist([image], [channel], mask=non_black_mask, histSize=[256], ranges=[0, 256])
        plt.plot(histogram, color=col[0])
        plt.title(col.upper() + " channel")
        plt.xlim(0, 256)

        # Save histogram data to DataFrame
        df[col] = histogram.flatten()

    plt.xlabel("RGB values")
    plt.ylabel("Pixel Frequency")
    plt.tight_layout()

    # Save the Matplotlib graph to an image file (optional)
    plt.savefig(sample + "_plot.png")

    # Save the DataFrame to an Excel file
    if save_to_excel:
        save_df_to_excel(df)

    # Plot the graph from the DataFrame
    plot_from_excel()

    plt.show()


def save_df_to_excel(data):
    filename = sample
    with pd.ExcelWriter(filename + '.xlsx', engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Histograms', index=False)

def plot_from_excel():
    # Read data from Excel
    filename = sample
    df = pd.read_excel(filename + '.xlsx', sheet_name='Histograms')

    color = ['b', 'g', 'r']
    plt.figure(figsize=(10, 5))
    plt.title(filename + ' from Excel')

    for channel, col in enumerate(color):
        plt.subplot(1, 3, channel + 1)
        plt.plot(df[col], color=col[0])
        plt.title(col.upper() + " channel")
        plt.xlim(0, 256)

    plt.xlabel("RGB values")
    plt.ylabel("Pixel Frequency")
    plt.tight_layout()
    plt.show()

def crop_trackbar(height, width, px, py, radius, src):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    img = src.copy()

    cv.circle(canvas, (px, py), radius, [255, 255, 255], cv.FILLED)

    cropped = cv.bitwise_and(img, canvas, mask=None)
    return cropped

def main():
    home = os.path.expanduser("~")
    img_path = home + "\\Repositories 2\\Project-INSTEAD\\Data_31-10-2023[7]\\Warna\\" + sample + ".jpg"
    img = cv.imread(img_path)

    height = img.shape[0]
    width = img.shape[1]
    channel = img.shape[2]

    cv.namedWindow("crop trackbar")
    cv.createTrackbar("x space", "crop trackbar", 0, width - 1, on_trackbar)
    cv.createTrackbar("y space", "crop trackbar", 0, height - 1, on_trackbar)
    cv.createTrackbar("radius", "crop trackbar", 0, 450, on_trackbar)

    cv.setTrackbarPos("x space", "crop trackbar", 324)
    cv.setTrackbarPos("y space", "crop trackbar", 238)
    cv.setTrackbarPos("radius", "crop trackbar", 100)

    while True:
        x = cv.getTrackbarPos("x space", "crop trackbar")
        y = cv.getTrackbarPos("y space", "crop trackbar")
        radius = cv.getTrackbarPos("radius", "crop trackbar")

        img_copy = img.copy()
        cv.circle(img_copy, (x, y), radius, [0, 0, 255], 2)

        crop_img = crop_trackbar(height, width, x, y, radius, img)
        cv.imshow("crop trackbar", img_copy)
        cv.imshow(sample, crop_img)
        key = cv.waitKey(3)

        if key == 27:
            break
        elif key == ord('c'):
            getHist(crop_img, sample, save_to_excel=True)
            save_mask(crop_img)

if __name__ == "__main__":
    main()
    cv.destroyAllWindows()
