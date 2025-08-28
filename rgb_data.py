import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

image_path = 'utils/chai_tea.jpg'
image = cv.imread(image_path)

cv.imshow("image",image)
crop = image[100:400,50:600]
cv.imshow("crop",crop)

key = cv.waitKey()
if key == 27:
    exit()

color = ['b','g','r']
for channel, col in enumerate(color):
    histogram = cv.calcHist([crop],[channel],mask=None,histSize=[256],ranges=[0,256])
    plt.plot(histogram,color = col)
    plt.xlim(0,256)
plt.title("Graph of RGB values")
plt.show()
