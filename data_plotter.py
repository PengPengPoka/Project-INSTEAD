import pandas as pd
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os

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
    plt.savefig(filename + "_plot.png")

    # Save the DataFrame to an Excel file
    if save_to_excel:
        save_df_to_excel(df, filename)

    # plt.show()

def save_mask(filename, mask):
    cv.imwrite(filename + "_mask.jpg", img=mask)

def save_df_to_excel(data, filename):
    with pd.ExcelWriter(filename + '.xlsx', engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Histograms', index=False)

def crop_trackbar(height, width, px, py, radius, src):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    img = src.copy()

    cv.circle(canvas, (px, py), radius, [255, 255, 255], cv.FILLED)

    cropped = cv.bitwise_and(img, canvas, mask=None)
    return cropped

def main():
    home = os.path.expanduser("~")
    i = 1
    j = 1
    variants = ("DUST", "DUST2", "DUST3", "BOHEA", "BOP", "BOPF", "BOPF1", "FI", "F2", "PF", "PF2", "PF3", "BP")

    # default param
    x = 324
    y = 238
    r = 100

    # # DUST 2 param
    # x = 316
    # y = 243
    # r = 93

    while i < 7:
        sample = str(variants[12]) + "_" + str(i) + "_" + str(j)
        img_path = home + "\\Repositories 2\\Project-INSTEAD\\Data_08-11-2023[11]\\Warna\\" + sample + ".jpg"
        print(img_path)
        img = cv.imread(img_path)

        height = img.shape[0]
        width = img.shape[1]
        channel = img.shape[2]

        # img_copy = img.copy()
        # cv.circle(img_copy, center=(x,y), radius=r, color=[0,0,255], thickness=2)
        crop_img = crop_trackbar(height, width, x, y, r, img)
        getHist(crop_img, sample, save_to_excel=True)
        save_mask(sample, crop_img)

        j += 1
        cv.imshow(sample,img)
        cv.imshow(sample + "_crop",crop_img)
        cv.waitKey(30)

        if j > 10:
            i += 1
            j = 1
        
    j = 1

if __name__ == "__main__":
    main()
    cv.destroyAllWindows()